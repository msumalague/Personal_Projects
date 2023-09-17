from datetime import datetime
import csv
import re
import pandas as pd
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
import time
from urllib.parse import urlparse
import pytz

start_time = time.time()

# Configure Undetected ChromeOptions
options = ChromeOptions()
options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
options.add_argument("--no-sandbox")  # Disable sandboxing for headless mode

# Create a new instance of Undetected ChromeDriver
driver = Chrome(options=options)

# List of URLs to scrape (read from "urls.csv" file)
with open("craiglist_urls.csv", "r", encoding="utf-8-sig") as url_file:
    urls = url_file.read().splitlines()

# Create a list to store data
data = []

# Track progress
total_urls = len(urls)
current_url = 0

for url in urls:
    current_url += 1
    print(f"Scraping URL {current_url}/{total_urls}: {url}")

    try:
        # Open the URL in the Chrome browser
        driver.get(url)

        # Wait for the page to load (you can adjust the sleep duration as needed)
        time.sleep(10)

        # Find and extract relevant data (titles, URLs, and dates) using XPath
        listings = driver.find_elements(By.XPATH, "//li[contains(@class, 'cl-search-result')]")

        # Limit the number of listings to the latest 100
        listings = listings[:100]

        # Initialize the ranking
        ranking = 0

        # Loop through the listings and store data in the list
        for listing in listings:
            title = listing.find_element(By.XPATH, ".//a[@class='cl-app-anchor text-only posting-title']/span").text
            listing_url = listing.find_element(By.XPATH, ".//a[@class='cl-app-anchor text-only posting-title']").get_attribute("href")
            date_str = listing.find_element(By.XPATH, ".//span[@title]").get_attribute("title")

            # Extract the date in the desired format using regular expression
            date_match = re.search(r'(\w{3} \w{3} \d{2} \d{4} \d{2}:\d{2}:\d{2})', date_str)
            if date_match:
                formatted_date = datetime.strptime(date_match.group(0), "%a %b %d %Y %H:%M:%S").strftime(
                    "%m/%d/%Y %H:%M:%S")
            else:
                formatted_date = ""

            # Extract the city from the URL
            parsed_url = urlparse(listing_url)
            city = parsed_url.netloc.split('.')[0]

            # Increment the ranking for the next listing
            ranking += 1

            # Append data to the list with the URL in the "Response From" column
            data.append([ranking, title, listing_url, formatted_date, city, url])

    except Exception as e:
        print(f"An error occurred while scraping the URL {current_url}/{total_urls}: {url}")
        print(str(e))

# Close the Chrome browser
driver.quit()

# Create a Pandas DataFrame from the data
df = pd.DataFrame(data, columns=["Ranking", "Title", "URL", "Date", "Neighborhood", "Response From"])

# Save the DataFrame to a CSV file
df.to_csv("craigslist_listings_combined.csv", index=False, encoding="utf-8")

print("Data has been saved to craigslist_listings_combined.csv.")
print("--- %s seconds ---" % (time.time() - start_time))
