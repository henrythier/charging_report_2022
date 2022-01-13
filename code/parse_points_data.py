import json
import re
from config import config
import pandas as pd

points_json_fp = config['points_data_fp']
points_csv_fp = config['points_data_table_fp']

with open(points_json_fp) as json_file:
    points = json.load(json_file)

parsed_points = []

for p in points:
    plug = p.pop('plugs', None)
    if not (plug is None):
        p['plug'] = plug[0]['backend_key']
    parsed_points.append(p)

df = pd.DataFrame.from_dict(parsed_points)
df.to_csv(points_csv_fp, index=None)
