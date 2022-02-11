import pandas as pd
from config import config

bnetzag = pd.read_csv(config['bnetzag_data_fp'], sep=";", decimal=',', skiprows=1, parse_dates=['Inbetriebnahmedatum'], dayfirst=True)

'''
Identify unique station based on Betreiber, Straße, Hausnummer, Ort, PLZ, Längengrad and Breitengrad
'''
station_identifiers = ['Betreiber', 'Straße', 'Hausnummer', 'Ort']
for s_id in station_identifiers:
  bnetzag[s_id] = bnetzag[s_id].apply(lambda x: x.strip())

station_identifiers.extend(['Postleitzahl', 'Längengrad', 'Breitengrad'])

stations = bnetzag[station_identifiers].drop_duplicates()

stations['station_id'] = stations.reset_index().index

'''
Merge back with stations
'''
bnetzag_merged = bnetzag.merge(stations, left_on=station_identifiers, right_on=station_identifiers, how='inner')

'''
split points into table with one row per point
'''
# function split points
points_columns = bnetzag_merged.columns[15:-1]

def stations_to_points(row):
  station_id = row['station_id']
  points = []
  i = 0

  while i < len(points_columns):
    p = points_columns[i]
    if not pd.isnull(row[p]):
      point = {
          'point_id': p[1],
          'station_id': station_id,
          'power': row[points_columns[i]],
          'public key': row[points_columns[i+1]],
          'steckertyp': row[points_columns[i-1]],
          'inbetriebnahme': row['Inbetriebnahmedatum']
      }
      points.append(point)
    i += 3

  return points

# apply to stations dataframe
points_series = bnetzag_merged.apply(lambda x: stations_to_points(x), axis=1)

# format into one points dataframe
points_unstacked = points_series.apply(pd.Series).stack().reset_index(drop = True)
points_unstacked

points_df = pd.DataFrame(list(points_unstacked))

# rearrange columns
rearranged_cols = points_df.columns[1::-1].append(points_df.columns[2:])
points_df = points_df[rearranged_cols]
bnetzag_points = points_df

# drop unnecessary columns and rearragne in stations table
bnetzag_merged = bnetzag_merged.drop(columns=points_columns)

bc = bnetzag_merged.columns
bc = bc[-1:].append(bc[:-6])
bnetzag_merged = bnetzag_merged[bc]

# only keep first entry for each station
bnetzag_merged = bnetzag_merged.groupby('station_id').nth(0)

# aggregate data for stations
points_by_station = points_df.groupby('station_id')['point_id'].count()
max_speed_station = points_df.groupby('station_id')['power'].max()
ibn_station = points_df.groupby('station_id')['inbetriebnahme'].min()

# add aggregated data to stations frame
points_agg = pd.concat([points_by_station, max_speed_station, ibn_station], axis=1)
points_agg.columns = ['number of points', 'max power', 'opened']
bnetzag_stations = bnetzag_merged.merge(points_agg, left_index=True, right_index=True)

'''
Save as csvs
'''
bnetzag_stations.to_csv(config['bnetzag_stations_data_fp'])
bnetzag_points.to_csv(config['bnetzag_points_data_fp'], index=None)
