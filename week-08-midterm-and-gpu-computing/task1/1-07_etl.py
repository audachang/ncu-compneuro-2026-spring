# %load_ext cudf.pandas
# DO NOT CHANGE THIS CELL
import pandas as pd
import time
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
dtype_dict={
    'age': 'int8', 
    'sex': 'object', 
    'county': 'object', 
    'lat': 'float32', 
    'long': 'float32', 
    'name': 'object'
}
        
df=pd.read_csv('./data/uk_pop.csv', dtype=dtype_dict)
df.head()
# -------------------- Cell End --------------------

centroid_df=pd.read_csv('county_centroid.csv')
centroid_df.columns=['county', 'lat_county_center', 'long_county_center']
centroid_df.head()
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile
combined_df=df.merge(centroid_df, on='county')
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile
c=['lat', 'long']
combined_df['R']=((combined_df[c] - combined_df.groupby('county')[c].transform('mean')) ** 2).sum(axis=1) ** 0.5
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile

# read in centroid data
centroid_df=pd.read_csv('county_centroid.csv')

# merge 
combined_df=df.merge(centroid_df, on='county', suffixes=['', '_county_center'])

# calculate distance from county center
combined_df['R']=((combined_df['lat']-combined_df['lat_county_center'])**2+(combined_df['long']-combined_df['long_county_center'])**2)**0.5
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile

senior_df_filter=combined_df['age'] >= 60
senior_df=combined_df.loc[senior_df_filter]

display(senior_df.head())
# -------------------- Cell End --------------------

senior_df.head()
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
senior_df.to_csv('senior_df.csv', index=False)
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
senior_df=senior_df.sort_values('county')

senior_df.to_parquet('senior_df.parquet', index=False)
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
import IPython
app = IPython.Application.instance()
app.kernel.do_shutdown(True)
# -------------------- Cell End --------------------

# %load_ext cudf.pandas
import pandas as pd
import time
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile

sel=[('county', '=', 'BLACKPOOL')]
parquet_df=pd.read_parquet('senior_df.parquet', columns=['age', 'sex', 'county', 'lat', 'long', 'name', 'R'], filters=sel)
parquet_df=parquet_df.loc[parquet_df['county']=='BLACKPOOL']
# -------------------- Cell End --------------------

parquet_df['county'].unique()
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile

df=pd.read_csv('./senior_df.csv', usecols=['age', 'sex', 'county', 'lat', 'long', 'name', 'R'])
df=df.loc[df['county']=='BLACKPOOL']
# -------------------- Cell End --------------------

df['county'].unique()
# -------------------- Cell End --------------------

import IPython
app = IPython.Application.instance()
app.kernel.do_shutdown(True)
# -------------------- Cell End --------------------

