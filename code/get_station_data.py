import requests
import pandas as pd
import json
from config import config

df = pd.read_csv(config['station_ids_fp'])
ids = list(df['id'])

points = []
stations = []

for id in ids:
    station_url = config['individual_station_url'].format(id)

    r = requests.get(station_url)

    if r.status_code != 200:
        raise Exception(f'Request returned an error: {r.status_code} {r.text} | station: {id}')

    try:
        data = r.json()
    except ValueError:
        print(f'Something went wrong decoding the JSON of {id}')

    if len(data) > 0:
        stations.append(data[0]['station'])
        station_id = data[0]['station']['id']

        for station_point in data[0]['points']:
            station_point['station_id'] = station_id
            points.append(station_point)

    else:
        print(f'No data for: {id}')

    if int(id) % 1000 == 0:
        print(f'Made it to: {id}')

with open(config['points_data_fp'], 'w', encoding='utf-8') as f:
    json.dump(points, f, ensure_ascii=False, indent=4)

with open(config['stations_data_fp'], 'w', encoding='utf-8') as f:
    json.dump(stations, f, ensure_ascii=False, indent=4)
