import subprocess # we will use this to obtain our local IP using the following command
cmd = "hostname --all-ip-addresses"

process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
IPADDR = str(output.decode()).split()[0]
# -------------------- Cell End --------------------

from dask_cuda import LocalCUDACluster
cluster = LocalCUDACluster(ip=IPADDR)
# -------------------- Cell End --------------------

from dask.distributed import Client, progress

client = Client(cluster)
# -------------------- Cell End --------------------

# get the file size of `pop5x_1-07.csv` in GB
# !ls -sh data/uk_pop5x.csv
# -------------------- Cell End --------------------

import dask_cudf
# -------------------- Cell End --------------------

ddf = dask_cudf.read_csv('./data/uk_pop5x.csv', dtype=['float32', 'str', 'str', 'float32', 'float32', 'str'])
# -------------------- Cell End --------------------

ddf.dtypes
# -------------------- Cell End --------------------

# !nvidia-smi
# -------------------- Cell End --------------------

ddf.visualize(format='svg') # This visualization is very large, and using `format='svg'` will make it easier to view.
# -------------------- Cell End --------------------

ddf.npartitions
# -------------------- Cell End --------------------

mean_age = ddf['age'].sum()
mean_age.visualize(format='svg')
# -------------------- Cell End --------------------

mean_age.compute()
# -------------------- Cell End --------------------

# !nvidia-smi
# -------------------- Cell End --------------------

ddf = ddf.persist()
# -------------------- Cell End --------------------

# !nvidia-smi
# -------------------- Cell End --------------------

ddf.visualize(format='svg')
# -------------------- Cell End --------------------

ddf['age'].mean().compute()
# -------------------- Cell End --------------------

ddf.head() # As a convenience, no need to `.compute` the `head()` method
# -------------------- Cell End --------------------

ddf.count().compute()
# -------------------- Cell End --------------------

ddf.dtypes
# -------------------- Cell End --------------------

sunderland_residents = ddf.loc[<<<<FIXME>>>>]
northmost_sunderland_lat = sunderland_residents['lat'].max()
counties_with_pop_north_of = ddf.loc[ddf['lat'] > northmost_sunderland_lat]['county'].unique()
results=counties_with_pop_north_of.compute()
results.head()
# -------------------- Cell End --------------------

import IPython
app = IPython.Application.instance()
app.kernel.do_shutdown(True)
# -------------------- Cell End --------------------

