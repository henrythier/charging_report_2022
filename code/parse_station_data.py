import json
import re
from config import config
import pandas as pd

station_json_fp = config['stations_data_fp']
station_csv_fp = config['stations_data_table_fp']

terms_to_unpack = ['access','electricity_mix','charge_type','payment_mode']

with open(station_json_fp) as json_file:
    stations = json.load(json_file)

parsed_stations = []

for s in stations:
    s['operator'] = s.pop('m', None)['name']

    for t in terms_to_unpack:
        nested_entry = s.pop(t, None)
        if not (nested_entry is None):
            s[t] = nested_entry['backend_key']

    payment_types = s.pop('payment_types', None)

    if not(payment_types is None):
        for payment_type in payment_types:
            backend_key = payment_type.pop('backend_key')
            payment_string = f'payment_{backend_key}'
            s[payment_string] = 1

    parsed_stations.append(s)

df = pd.DataFrame.from_dict(parsed_stations)
df.to_csv(station_csv_fp, index=None)
