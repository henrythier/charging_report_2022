import requests
import pandas as pd
import json
from config import config

url = config["tesla_data_url"]

sc_df = pd.read_csv(config['tesla_sc_id_fp'])
sc_data_fp = config['tesla_sc_data_fp']

dc_df = pd.read_csv(config['tesla_dc_id_fp'])
dc_data_fp = config['tesla_dc_data_fp']

# get sc data
sc_ids = list(sc_df['id'])

sc_data = []

for sc_id in sc_ids:
    sc_url = url.format(sc_id)
    r = requests.get(sc_url)

    if r.status_code != 200:
        raise Exception(f'Request returned an error: {r.status_code} {r.text} | sc: {sc_id}')

    sc_data.append(r.json())

with open(sc_data_fp, 'w', encoding='utf-8') as f:
    json.dump(sc_data, f, ensure_ascii=False, indent=4)

# get dc data
dc_ids = list(dc_df['id'])

dc_data = []

for dc_id in dc_ids:
    dc_url = url.format(dc_id)
    r = requests.get(dc_url)

    if r.status_code != 200:
        raise Exception(f'Request returned an error: {r.status_code} {r.text} | dc: {dc_id}')

    dc_data.append(r.json())

with open(dc_data_fp, 'w', encoding='utf-8') as f:
    json.dump(dc_data, f, ensure_ascii=False, indent=4)
