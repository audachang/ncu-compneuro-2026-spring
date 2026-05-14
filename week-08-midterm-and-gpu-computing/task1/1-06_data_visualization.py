# %load_ext cudf.pandas
# DO NOT CHANGE THIS CELL
import pandas as pd
from IPython.display import display

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

# DO NOT CHANGE THIS CELL
df.groupby('county').size().sort_values(ascending=False).head().plot(kind='bar')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
df['age_bucket']=pd.cut(df['age'], bins=bins, right=True, include_lowest=True, labels=False)
df.groupby('age_bucket').size().plot(kind='bar')
# -------------------- Cell End --------------------

df.groupby('sex').size().plot(kind='bar')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# sample a very small percentage of the data
small_df=df.sample(1000)

small_df.plot(kind='scatter', x='lat', y='long')
# -------------------- Cell End --------------------

# import time
# import matplotlib.pyplot as plt

# fig, ax=plt.subplots()
# exec_times={}

# for size in (5*(10**i) for i in range(1, 8)): 
#     start=time.time()
#     df.sample(size).plot(kind='scatter', x='long', y='lat', ax=ax)
#     duration=time.time()-start
#     exec_times[size]=duration
#     ax.clear()

# ax.plot(exec_times.keys(), exec_times.values(), marker='o')
# ax.set_xscale('log')
# ax.set_xlabel('Data Size')
# ax.set_ylabel('Execution Time')
# ax.set_title("Scatter Plot Doesn't Scale Well With Data Size")
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
import IPython
app = IPython.Application.instance()
# app.kernel.do_shutdown(True)
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
import time
import matplotlib.pyplot as plt

import datashader as ds
import datashader.transfer_functions as tf
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
import pandas as pd

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

# DO NOT CHANGE THIS CELL
start=time.time()

# get points
ds_points_pandas=ds.Canvas().points(df,'long','lat')
display(ds_points_pandas)

# plot points
plt.imshow(tf.shade(ds_points_pandas))

print(f'Duration: {round(time.time()-start, 2)} seconds')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
import cudf

dtype_dict={
    'age': 'int8', 
    'sex': 'object', 
    'county': 'object', 
    'lat': 'float32', 
    'long': 'float32', 
    'name': 'object'
}
        
gdf=cudf.read_csv('./data/uk_pop.csv', dtype=dtype_dict)
gdf.head()
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
start=time.time()

# get points
ds_points_cudf=ds.Canvas().points(gdf,'long','lat')
display(ds_points_cudf)

# plot points
plt.imshow(tf.shade(ds_points_cudf))

print(f'Duration: {round(time.time()-start, 2)} seconds')
# -------------------- Cell End --------------------

import cuxfilter as cxf

# factorize county for multiselect widget
gdf['county'], county_names = gdf['county'].factorize()
county_map = dict(zip(list(range(len(county_names))), county_names.to_arrow()))
# -------------------- Cell End --------------------

# create cuxfilter DataFrame
cxf_data = cxf.DataFrame.from_dataframe(gdf)

# create Datashader scatter plot
scatter_chart = cxf.charts.scatter(x='long', y='lat')
# -------------------- Cell End --------------------

# create Bokeh bar charts
chart_3=cxf.charts.bar('age')
chart_2=cxf.charts.bar('sex')
# -------------------- Cell End --------------------

# define layout
layout_array=[[1, 2, 2], 
              [3, 2, 2]]
# -------------------- Cell End --------------------

# create multiselect widget
county_widget = cxf.charts.panel_widgets.multi_select('county', label_map=county_map)

# define layout
dash = cxf_data.dashboard(charts=[chart_2, scatter_chart, chart_3],sidebar=[county_widget], theme=cxf.themes.dark, data_size_widget=True, layout_array=layout_array)

# dash.app()
# -------------------- Cell End --------------------

import IPython
app = IPython.Application.instance()
# # app.kernel.do_shutdown(True)
# -------------------- Cell End --------------------

