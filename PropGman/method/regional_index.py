# encoding: utf-8
"""
Author: 何彥南 (yen-nan ho)
Github: https://github.com/aaron1aaron2
Email: aaron1aaron2@gmail.com
Create Date: 2022.09.13
Last Update: 2022.09.13
Describe: 計算區域性指標
"""
import pandas as pd
from typing import Tuple

class RegionalIndex:
    def __init__(self, start_date:str, end_date:str, time_freq:str, dist_threshold:int):
        super(RegionalIndex, self).__init__()
        
        # 時間區間
        self.start_date = start_date
        self.end_date = end_date

        self.time_freq = time_freq

        # 距離範圍
        self.dist_threshold = dist_threshold

        self.date_table = self._get_date_table()
        self.total_time_step = self.date_table.shape[0]

    def _get_date_table(self):
        # 日期基準
        date_ls = pd.date_range(start=self.start_date, end=self.end_date, freq=self.time_freq)
        date_table = pd.DataFrame({
                'year': date_ls.year,
                'month': date_ls.month
            })

        return date_table

    def _fill_na(self, df, col, method):
        na_num = df[df[col].isna()].shape[0]

        if method=='front-back-avg':
            f_fill = df[col].fillna(method='ffill')
            b_fill = df[col].fillna(method='bfill')

            result  = (f_fill + b_fill)/2

            unable_fill_na_num = result[result.isna()].shape[0]

        elif method=='zero':
            result = df[col].fillna(0)
            unable_fill_na_num = 0

        record = {
            'column_name':col, 
            'na_num':na_num, 'unable_fill_na':unable_fill_na_num,
            'na_rate':round(na_num/self.total_time_step, 2), 
            'unable_fill_na_rate':round(unable_fill_na_num/self.total_time_step, 2)
        }

        return result, record

    def get_index(
            self, 
            df_distance:pd.DataFrame, 
            df_tran:pd.DataFrame, 
            method:str, 
            target_value_col:str, 
            dist_value_col:str, 
            id_col:str, 
            fillna_method:str
        ) -> Tuple[pd.DataFrame, dict]:

        id_select = df_distance.loc[df_distance[dist_value_col] <= self.dist_threshold, id_col].to_list()
        df_tran_select = df_tran[df_tran[id_col].astype(int).isin(id_select)].copy()

        df_tran_select[target_value_col] = df_tran_select[target_value_col].astype(float)
        df_tran_select['year'] = df_tran_select['year'].astype(int)
        df_tran_select['month'] = df_tran_select['month'].astype(int)

        if method=='mean':
            gb_result = df_tran_select.groupby(['year', 'month'])[target_value_col].mean()
        elif method=='count':
            gb_result = df_tran_select.groupby(['year', 'month'])[target_value_col].count()
        else:
            gb_result = df_tran_select.groupby(['year', 'month'])[target_value_col].mean()

        gb_result = self.date_table.merge(gb_result.reset_index(), how='left')

        result, record = self._fill_na(gb_result, target_value_col, fillna_method)

        return result, record