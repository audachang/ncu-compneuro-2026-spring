# DO NOT CHANGE THIS CELL
# !head -n 5 data/uk_pop.csv
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
import cudf
import cupy as cp
import numpy as np

from datetime import datetime
import random
import time
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
start=time.time()
df=cudf.read_csv('./data/uk_pop.csv')
print(f'Duration: {round(time.time()-start, 2)} seconds')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
df.info(memory_usage='deep')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
df.head()
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# get first cell
display(df.loc[0, 'age'])
print('-'*40)

# get multiple rows and columns
display(df.loc[[0, 1, 2], ['age', 'sex', 'county']])
print('-'*40)

# slice a range of rows and columns
display(df.loc[0:5, 'age':'county'])
print('-'*40)

# slice a range of rows and columns
display(df.loc[:10, :'name'])
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# get current year
current_year=datetime.now().year

# derive the birth year
display(current_year-df.loc[:, 'age'])

# get the age array (CuPy for cuDF)
age_ary=df.loc[:, 'age'].values

# derive the birth year
current_year-age_ary
# -------------------- Cell End --------------------

df['county'].str.<<<<FIXME>>>>
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
df['age']>=18
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
df[['lat', 'long']].mean()
# -------------------- Cell End --------------------

# DO NOT CHNAGE THIS CELL
# define a function to check if age is greater than or equal to 18
start=time.time()
def is_adult(row): 
    if row['age']>=18: 
        return 1
    else: 
        return 0

# derive the birth year
display(df.apply(is_adult, axis=1))
print(f'Duration: {round(time.time()-start, 2)} seconds')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# derive the birth year
start=time.time()
display(df.apply(lambda x: 1 if x['age']>=18 else 0, axis=1))
print(f'Duration: {round(time.time()-start, 2)} seconds')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# derive the birth year
start=time.time()
display((df['age']>=18).astype('int'))
print(f'Duration: {round(time.time()-start, 2)} seconds')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
df['name'].map(lambda x: len(x))
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
boolean_mask=df['name'].str.startswith('E')
df.loc[boolean_mask]
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
df[(df['age']>=18) | (df['name'].str.startswith('E'))]
# -------------------- Cell End --------------------

sunderland_residents=df.loc[<<<<FIXME>>>>]
northmost_sunderland_lat=sunderland_residents['lat'].max()
df.loc[df['lat'] > northmost_sunderland_lat]['county'].unique()
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# get current year
current_year=datetime.now().year

# numerical operations
df['birth_year']=current_year-df['age']

# string operations
df['sex_normalize']=df['sex'].str.upper()
df['county_normalize']=df['county'].str.title().str.replace(' ', '_')
df['name']=df['name'].str.title()

# preview
df.head()
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
import IPython
app = IPython.Application.instance()
app.kernel.do_shutdown(True)
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# %load_ext cudf.pandas
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
import pandas as pd
import time
from datetime import datetime
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile
# DO NOT CHANGE THIS CELL
start=time.time()

df=pd.read_csv('./data/uk_pop.csv')
current_year=datetime.now().year

df['birth_year']=current_year-df['age']

df['sex_normalize']=df['sex'].str.upper()
df['county_normalize']=df['county'].str.title().str.replace(' ', '_')
df['name']=df['name'].str.title()

print(f'Duration: {round(time.time()-start, 2)} seconds')

display(df.head())
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
import IPython
app = IPython.Application.instance()
app.kernel.do_shutdown(True)
# -------------------- Cell End --------------------

