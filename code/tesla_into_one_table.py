import requests
import pandas as pd
import json
from config import config

'''station columns to keep'''
station_columns = ['location_id', 'city', 'open_soon', 'postal_code',
       'longitude', 'latitude']

'''Get the destination charger points'''
dc_points = pd.read_csv(config['tesla_dc_points_fp'])
dc_points['charger_type'] = 'destination'

'''Get the destination charger stations'''
dc_points_fp = config['tesla_dc_data_fp']

with open(dc_points_fp) as f:
    dc_stations_dict = json.load(f)

dc_stations = pd.DataFrame.from_dict(dc_stations_dict)
dc_stations = dc_stations[station_columns]

'''Get the super charger points'''
sc_points = pd.read_csv(config['tesla_sc_points_fp'])
sc_points['charger_type'] = 'super'

'''Get the super charger stations'''
sc_points_fp = config['tesla_sc_data_fp']
with open(sc_points_fp) as f:
    sc_stations_dict = json.load(f)

sc_stations = pd.DataFrame.from_dict(sc_stations_dict)
sc_stations = sc_stations[station_columns]

'''merge everything into one table'''
stations = pd.concat([dc_stations, sc_stations])
points = pd.concat([dc_points, sc_points])

tesla = stations.merge(points, left_on='location_id', right_on='station_id', how='inner')

nominatim_url = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={}&lon={}'
def get_bundesland(lat, lon):
  temp_url = nominatim_url.format(lat, lon)
  response = requests.get(temp_url)
  bundesland = response.json()['address']['state']
  return bundesland

tesla['bundesland'] = tesla.apply(lambda x: get_bundesland(x['latitude'], x['longitude']), axis=1)

tesla.to_csv('../data/tesla.csv', index=None)
