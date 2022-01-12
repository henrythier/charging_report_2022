import json
import re
from config import config
import pandas as pd

station_fp = config['tesla_sc_data_fp']
points_fp = config['tesla_sc_points_fp']

with open(station_fp) as json_file:
    stations = json.load(json_file)

points = []

for station in stations:
    id = station['location_id']
    charger_string = station['chargers']

    # parse charger string
    # lower case
    charger_string = charger_string.lower()

    # remove non alphanumeric
    charger_string = re.sub("[^0-9a-zA-Z/]+", " ", charger_string)
    charger_string = charger_string.replace('tesla connectors', 'supercharger')

    # split into tokens
    charger_tokens = charger_string.split()

    superchargers = []
    kw_values = []

    for i in range(len(charger_tokens)):
      t = charger_tokens[i]

      # find number of superchargers
      if 'supercharger' in t:
        ct = charger_tokens[i-1]
        if ct.isnumeric():
            superchargers.append(int(ct))
        continue

      # find power of superchargers
      if 'kw' in t and t[-2:] == 'kw':
        if len(t) > 2:
          kw_values.append(int(t[:-2]))

        else:
          kw_values.append(int(charger_tokens[i-1]))

    if len(kw_values) != len(superchargers):
      raise Exception(f'length does not match: {id}')

    else:
        for i in range(len(superchargers)):
            num_of_cp = superchargers[i]
            for sc in range(num_of_cp):
                p = {
                    'station_id': id,
                    'kw': kw_values[i]
                    }
                points.append(p)

df = pd.DataFrame.from_dict(points)
df.to_csv(points_fp, index=None)
