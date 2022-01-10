import requests
import pandas as pd
import json
from config import config

stations_url = config['stations_url']

r = requests.get(stations_url)

if r.status_code != 200:
    raise Exception(f'Request returned an error: {r.status_code} {r.text}')

stations_df = pd.DataFrame.from_dict(r.json()['stations'])
stations_df.to_csv(config['station_ids_fp'], index=None)
