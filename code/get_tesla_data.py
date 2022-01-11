import requests
import pandas as pd
import json
from config import config

url = config["tesla_data_url"]

df = pd.read_csv(config['tesla_sc_id_fp'])
ids = list(df['id'])

id = ids[0]

station_url = url.format(id)
r = requests.get(station_url)

if r.status_code != 200:
    raise Exception(f'Request returned an error: {r.status_code} {r.text} | station: {id}')

print(r.json())
