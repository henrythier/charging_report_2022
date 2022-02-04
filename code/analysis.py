import pandas as pd
from config import config

stations_data_table_fp = config['stations_data_table_fp']
points_data_table_fp = config['points_data_table_fp']

stations_df = pd.read_csv(stations_data_table_fp)
points_df = pd.read_csv(points_data_table_fp)

all_df = pd.merge(stations_df, points_df, how='inner', left_on='id', right_on = 'station_id')

fast_chargers_df = all_df.loc[all_df['charge_type'] == 'HYPERCHARGE']

print(fast_chargers_df['operator'].value_counts().head(10))
