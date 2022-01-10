import requests
import pandas as pd
import json
from config import config

df = pd.read_csv(config['station_ids_fp'])
ids = list(df['id'][12000:12002])

points = []
stations = []

id = ids[0]
for id in ids:
    station_url = config['individual_station_url'].format(id)

    r = requests.get(station_url)

    if r.status_code != 200:
        raise Exception(f'Request returned an error: {r.status_code} {r.text} | station: {id}')

    data = r.json()[0]
    stations.append(data['station'])
    points.extend(data['points'])

with open(config['points_data_fp'], 'w', encoding='utf-8') as f:
    json.dump(points, f, ensure_ascii=False, indent=4)

with open(config['stations_data_fp'], 'w', encoding='utf-8') as f:
    json.dump(stations, f, ensure_ascii=False, indent=4)
