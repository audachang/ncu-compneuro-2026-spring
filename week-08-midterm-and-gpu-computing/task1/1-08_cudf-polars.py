import polars as pl
import time

start_time = time.time()

polars_df = pl.read_csv('./data/uk_pop.csv')

polars_time = time.time() - start_time

print(f"Time Taken: {polars_time:.4f} seconds")
# -------------------- Cell End --------------------

polars_df.head()
# -------------------- Cell End --------------------

start_time = time.time()

#load data
polars_df = pl.read_csv('./data/uk_pop.csv')

# Filter for ages above 0
filtered_df = polars_df.filter(pl.col('age') > 0.0)

#Sort by name
sorted_df = filtered_df.sort('name', descending=True)

print(sorted_df.head())
polars_time = time.time() - start_time
print(f"Time Taken: {polars_time:.4f} seconds")
# -------------------- Cell End --------------------

import pandas as pd
import time
start_time = time.time()
pandas_df = pd.read_csv('./data/uk_pop.csv')

filtered_df = pandas_df[pandas_df['age'] > 0.0]

sorted_df = filtered_df.sort_values(by=['name'], ascending=False)

pandas_time = time.time() - start_time
print(f"Time Taken: {pandas_time:.4f} seconds\n")
# -------------------- Cell End --------------------

# Activate cuDF Pandas
# %load_ext cudf.pandas
import pandas as pd
# -------------------- Cell End --------------------

import pandas as pd
import time
start_time = time.time()
pandas_df = pd.read_csv('./data/uk_pop.csv')

filtered_df = pandas_df[pandas_df['age'] > 0.0]

sorted_df = filtered_df.sort_values(by=['name'], ascending=False)

pandas_time = time.time() - start_time
print(f"Time Taken for cuDF Pandas: {pandas_time:.4f} seconds\n")
# -------------------- Cell End --------------------


# -------------------- Cell End --------------------


# -------------------- Cell End --------------------


# -------------------- Cell End --------------------


# -------------------- Cell End --------------------

import polars as pl
import time

start_time = time.time()

# Create a lazy DataFrame
lazy_df = pl.scan_csv('./data/uk_pop.csv')

# Define the lazy operations
lazy_result = (
    lazy_df
    .filter(pl.col('age') > 0.0)
    .sort('name', descending=True)
)

# Execute the lazy query and collect the results
result = lazy_result.collect()

print(result.head())
polars_time = time.time() - start_time
print(f"Time Taken: {polars_time:.4f} seconds")
# -------------------- Cell End --------------------

# Show unoptimized Graph
lazy_result.show_graph(optimized=False, show=False)
# -------------------- Cell End --------------------

# Show optimized Graph
lazy_result.show_graph(optimized=True, show=False)
# -------------------- Cell End --------------------


# -------------------- Cell End --------------------


# -------------------- Cell End --------------------

lazy_df = pl.scan_csv('./data/uk_pop.csv').collect(engine="gpu")
# -------------------- Cell End --------------------

import polars as pl
import time

gpu_engine = pl.GPUEngine(
    device=0, # This is the default
    raise_on_fail=True, # Fail loudly if we can't run on the GPU.
)
# -------------------- Cell End --------------------

lazy_df = pl.scan_csv('./data/uk_pop.csv').collect(engine=gpu_engine)
# -------------------- Cell End --------------------

start_time = time.time()

# Create a lazy DataFrame
lazy_df = pl.scan_csv('./data/uk_pop.csv')

# Define the lazy operations
lazy_result = (
    lazy_df
    .filter(pl.col('age') > 0.0)
    .sort('name', descending=True)
)

# Switch to gpu_engine
result = lazy_result.collect(engine=gpu_engine)

print(result.head())
polars_time = time.time() - start_time
print(f"Time Taken: {polars_time:.4f} seconds")
# -------------------- Cell End --------------------

from polars.testing import assert_frame_equal

# Run on the CPU
result_cpu = lazy_result.collect()

# Run on the GPU
result_gpu = lazy_result.collect(engine="gpu")

# assert both result are equal - Will error if not equal, return None otherwise
if (assert_frame_equal(result_gpu, result_cpu) == None):
    print("The test frames are equal")
# -------------------- Cell End --------------------

result = (
    lazy_df
    .with_columns(pl.col('age').rolling_mean(window_size=7).alias('age_rolling_mean'))
    .filter(pl.col('age') > 0.0)  
    .collect(engine=gpu_engine)
)
print(result[::7])
# -------------------- Cell End --------------------

gpu_engine_with_fallback = pl.GPUEngine(
    device=0, # This is the default
    raise_on_fail=False, # Fallback to CPU if we can't run on the GPU (this is the default)
)
# -------------------- Cell End --------------------

result = (
    lazy_df
    .with_columns(pl.col('age').rolling_mean(window_size=7).alias('age_rolling_mean'))
    .filter(pl.col('age') > 0.0)  
    .collect(engine=gpu_engine_with_fallback)
)
print(result[::7])
# -------------------- Cell End --------------------

# Create the lazy query with column pruning
lazy_query = (
    lazy_df
    .select(["county", "lat", "long"])  # Column pruning: select only necessary columns
    .group_by("county")
    .agg([
        pl.col("lat").mean().alias("avg_latitude"),
        pl.col("long").mean().alias("avg_longitude")
    ])
    .sort("county")
)

# Execute the query
result = lazy_query.collect()

print("\nAverage latitude and longitude for each county:")
print(result.head())  # Display first few rows
# -------------------- Cell End --------------------

import IPython
app = IPython.Application.instance()
app.kernel.do_shutdown(True)
# -------------------- Cell End --------------------

