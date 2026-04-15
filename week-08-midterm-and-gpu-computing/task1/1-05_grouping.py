# DO NOT CHANGE THIS CELL
# %load_ext cudf.pandas
import pandas as pd
import time
from IPython.display import display
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
dtype_dict={
    'age': 'int8', 
    'sex': 'category', 
    'county': 'category', 
    'lat': 'float32', 
    'long': 'float32', 
    'name': 'category'
}
        
df=pd.read_csv('./data/uk_pop.csv', dtype=dtype_dict)
df.head()
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
df.groupby('county').size()
# -------------------- Cell End --------------------

# !nvidia-smi
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
df.groupby('name').size().sort_values()
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile
# DO NOT CHANGE THIS CELL

county_center_df=df[['county', 'lat', 'long']].groupby('county')[['lat', 'long']].mean()
display(county_center_df)
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
county_center_df.columns=['lat_county_center', 'long_county_center']
county_center_df.to_csv('county_centroid.csv')
# -------------------- Cell End --------------------

df[['county', 'age']].groupby('county')['age']\
                     .mean()\
                     .sort_values(ascending=False)\
                     .head()
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile
# DO NOT CHANGE THIS CELL

bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

df['age_bucket']=pd.cut(df['age'].values, bins=bins, right=True, include_lowest=True, labels=False)
display(df.groupby('age_bucket').size())
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile
# DO NOT CHANGE THIS CELL

df['age_bucket']=pd.cut(df['age'].values, bins=range(0, 100, 10), right=True, include_lowest=True, labels=False)
display(df.groupby('age_bucket').size())
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL

# define distance function
def distance(lat_1, long_1, lat_2, long_2): 
    return ((lat_2-lat_1)**2+(long_2-long_1)**2)**0.5
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile
# DO NOT CHANGE THIS CELL

distance_df=df.groupby('county')[['lat', 'long']].apply(lambda x: distance(x['lat'], x['long'], x['lat'].mean(), x['long'].mean()))
df['R_1']=distance_df.reset_index(level=0, drop=True)
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile
# DO NOT CHANGE THIS CELL

df['R_2']=df.groupby('county')[['lat', 'long']].apply(lambda x: ((x['lat'].mean()-x['lat'])**2+(x['long'].mean()-x['long'])**2)**0.5).reset_index(level=0, drop=True)
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# make data types more precise
df[['lat', 'long']]=df[['lat', 'long']].astype('float64')
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile
# DO NOT CHANGE THIS CELL

c=['lat', 'long']
df['R_3']=((df[c] - df.groupby('county')[c].transform('mean')) ** 2).sum(axis=1) ** 0.5
# -------------------- Cell End --------------------

df.head()
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile
# DO NOT CHANGE THIS CELL

pvt_tbl=df[['county', 'sex', 'name']].pivot_table(index=['county'], columns=['sex'], values='name', aggfunc='count')
pvt_tbl=pvt_tbl.apply(lambda x: x/sum(x), axis=1)
display(pvt_tbl)
# -------------------- Cell End --------------------

import IPython
app = IPython.Application.instance()
# app.kernel.do_shutdown(True)
# -------------------- Cell End --------------------

