# DO NOT CHANGE THIS CELL
# activate this cell by selecting it with the mouse or arrow keys then use the keyboard shortcut [Shift+Enter] to execute
print('This is just a simple print statement.')
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# !echo 'This is another simple print statement.'
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# !nvidia-smi
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
from time import sleep
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
# %time only times one line
# %time sleep(2) 
sleep(1)
# -------------------- Cell End --------------------

# %%time
# DO NOT CHANGE THIS CELL
# %%time will time the entire cell
sleep(1)
sleep(1)
# -------------------- Cell End --------------------

# DO NOT CHANGE THIS CELL
import IPython
app = IPython.Application.instance()
app.kernel.do_shutdown(True)
# -------------------- Cell End --------------------

