# encoding: utf-8
"""
Author: 何彥南 (yen-nan ho)
Github: https://github.com/aaron1aaron2
Email: aaron1aaron2@gmail.com
Create Date: 2022.08.09
Last Update: 2022.08.12
Describe: 觀察時間與交易量的分布
"""
import os
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# 基本設定
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']

output_folder = 'data/data_procces/8_time_range_select'
os.makedirs(output_folder, exist_ok=True)

df = pd.read_csv('data/data_procces/7_landuse_select/transaction_all.csv', dtype=str)

df.dropna(subset=['都市土地使用分區', '非都市土地使用分區', '非都市土地使用編定'], how='all', inplace=True)

df['year_TW'] = df['year']
df['year'] = df['year'].astype(int) + 1911
df['date'] = pd.to_datetime(df[["year", "month", "day"]].astype(int))

df = df[df['year_TW']!='100'] # 不應該存在 100 年的資料

# 每月份的交易量
tmp = df[["year", "month", "day"]].astype(int)
tmp['day'] = 1

month_ct = pd.to_datetime(tmp).value_counts()
month_ct = month_ct.reset_index()
month_ct.columns = ['year-month', 'count']
month_ct['year'] = pd.DatetimeIndex(month_ct['year-month']).year
# month_ct.plot(figsize=(10, 6))

plt.clf()
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b')) # define the formatting
# plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=12)) # show every 12th tick on x axes
# plt.xticks(rotation=40, fontweight='light', fontsize='x-small')
sns.lineplot(x='year-month', y='count', hue='year', data=month_ct.reset_index(), palette='Set2')

plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'transaction_plot(year-month).png'))

# 每個月在不同 ================================
gb_ct = df.groupby(['year', 'month', '使用分區']).count()['day'].reset_index()

tmp = gb_ct[["year", "month", "day"]].astype(int)
tmp['day'] = 1

gb_ct['year-month'] = pd.to_datetime(tmp)
gb_ct.rename(columns={'day': 'count'}, inplace=True)

plt.clf()
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
sns.lineplot(x='year-month', y='count', hue='使用分區', data=gb_ct, palette='Set2')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'transaction_landuse_plot(year-month).png'))


plt.clf()
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
sns.lineplot(x='year-month', y='count', hue='使用分區', data=gb_ct[gb_ct['使用分區'].isin(['住', '商'])], palette='Set2')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'transaction_landuse_plot(year-month)_house-business.png'))

# 資料篩選 ===================================\
year_month = pd.DatetimeIndex(month_ct[month_ct['count']<200]['year-month'])
remove_ls = (year_month.year.astype(str) + '-' + year_month.month.astype(str)).to_list()

tmp = df['year'].astype(str) + '-' + df['month'].astype(str)
df = df[~tmp.isin(remove_ls)]

df.to_csv(os.path.join(output_folder, 'transaction_all.csv'), index=False)