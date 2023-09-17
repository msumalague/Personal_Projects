import pandas as pd
import requests
from datetime import datetime

api_url = 'https://analytics.byrdup.com/index.php?module=API&method={method}&idSite={site_id}&period={period}&date={date}&format=json&token_auth={auth_token}&filter_limit=-1&flat=1&metrics={metric}'
api_method = 'VisitsSummary.get'
site_id = 2
period = 'month'
date = datetime.now().strftime('%Y-%m-%d')
metric = 'nb_uniq_visitors', 'nb_visits', 'nb_users', 'nb_actions', 'sum_visit_length', 'bounce_count', 'max_actions', 'nb_visits_converted','nb_conversions'


auth_token = 'MY_AUTH_TOKEN' #Replace your token here


params = {
    'module': 'API',
    'method': api_method,
    'idSite': site_id,
    'period': period,
    'date': date,
    'format': 'json',
    'token_auth': auth_token,
    'filter_limit': -1,
    'flat': 1,
    'metrics': metric
}

response = requests.get(api_url, params=params)
print(response)

json_data = response.json()

df = pd.DataFrame(json_data)
print(df.head())
df.to_csv('matomo_data.csv', index=False)

