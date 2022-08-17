"""
Author: 何彥南 (yen-nan ho)
Github: https://github.com/aaron1aaron2
Email: aaron1aaron2@gmail.com
Create Date: 2022.08.16
Last Update: 2022.08.16
Describe: 設立對應的參考點。上下左右
"""
import os
import itertools
import pandas as pd

from geopy.distance import geodesic

output_folder = 'data/supplementary'
os.makedirs(output_folder, exist_ok=True)

df_tar = pd.read_csv('data/method_procces/0_target_land_group/group_list.csv')
df_tran = pd.read_csv('data/data_procces/8_time_range_select/transaction_all.csv')

tran_land = df_tran[['long', 'lat', 'land_id']].drop_duplicates()
tran_land['tran_land_center'] = tran_land['lat'].astype(str) + ',' +  tran_land['long'].astype(str)
tran_land.drop(['lat', 'long'], axis=1, inplace=True)
tran_land['land_id'] = tran_land['land_id'].astype(int)

two_point_df = pd.DataFrame()
for gp_id in df_tar['group_id'].to_list():
    tmp = tran_land.copy()
    tmp['group_id'] = gp_id
    two_point_df = pd.concat([two_point_df, tmp])

two_point_df = two_point_df.merge(df_tar, how='left')