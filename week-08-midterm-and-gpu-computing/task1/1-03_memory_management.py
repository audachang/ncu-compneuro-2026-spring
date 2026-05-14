# DO NOT CHANGE THIS CELL
import pandas as pd
import random
import time
from IPython.display import display # Use IPython display if available, or mock it
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
df=pd.read_csv('./data/uk_pop.csv')

# preview
df.head()
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# pandas memory utilization
mem_usage_df=df.memory_usage(deep=True)
mem_usage_df
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
suffixes = ['B', 'kB', 'MB', 'GB', 'TB', 'PB']
def make_decimal(nbytes):
    i=0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes/=1024.
        i+=1
    f=('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])
# -------------------- Cell End --------------------

make_decimal(mem_usage_df.sum())
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# get number of rows
num_rows=len(df)

# 64-bit numbers uses 8 bytes of memory
print(f'Numerical columns use {num_rows*8} bytes of memory')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# check random string-typed column
string_cols=[col for col in df.columns if df[col].dtype=='object' ]
column_to_check=random.choice(string_cols)

overhead=49
pointer_size=8

# nan==nan when value is not a number
# nan uses 32 bytes of memory
string_col_mem_usage_df=df[column_to_check].map(lambda x: len(x)+overhead+pointer_size if x else 32)
string_col_mem_usage=string_col_mem_usage_df.sum()
print(f'{column_to_check} column uses {string_col_mem_usage} bytes of memory.')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
df['age']=df['age'].astype('int8')

df.dtypes
# -------------------- Cell End --------------------

df['lat']=df['lat'].astype('float32')
df['long']=df['long'].astype('float32')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
df.select_dtypes(include='object').nunique()
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
df['sex']=df['sex'].astype('category')
df['county']=df['county'].astype('category')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
display(df['county'].cat.categories)
print('-'*40)
display(df['county'].cat.codes)
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
start=time.time()
df=pd.read_csv('./data/uk_pop.csv')
duration=time.time()-start

mem_usage_df=df.memory_usage(deep=True)
display(mem_usage_df)

print(f'Loading {make_decimal(mem_usage_df.sum())} took {round(duration, 2)} seconds.')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# %load_ext cudf.pandas

import pandas as pd
import time
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
suffixes = ['B', 'kB', 'MB', 'GB', 'TB', 'PB']
def make_decimal(nbytes):
    i=0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes/=1024.
        i+=1
    f=('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])
# -------------------- Cell End --------------------

# %%cudf.pandas.line_profile
# DO NOT CHANGE THIS CELL
start=time.time()

# define data types for each column
dtype_dict={
    'age': 'int8', 
    'sex': 'category', 
    'county': 'category', 
    'lat': 'float64', 
    'long': 'float64', 
    'name': 'category'
}
        
efficient_df=pd.read_csv('./data/uk_pop.csv', dtype=dtype_dict)
duration=time.time()-start

mem_usage_df=efficient_df.memory_usage('deep')
display(mem_usage_df)

print(f'Loading {make_decimal(mem_usage_df.sum())} took {round(duration, 2)} seconds.')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# !nvidia-smi
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# 1 gigabytes = 1073741824 bytes
mem_capacity=16*1073741824

mem_per_record=mem_usage_df.sum()/len(efficient_df)

print(f'We can load {int(mem_capacity/2/mem_per_record)} rows.')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
import IPython
import IPython
app = IPython.Application.instance()
# app.kernel.do_shutdown(True) # Kernel shutdown disabled for script execution
# -------------------- Cell End --------------------

