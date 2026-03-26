"""
Demonstrate plotting a series of pictures
Creating the graph objects and present them in the
same loop. 

"""


from glob import glob
from psychopy import visual, core, event
import pandas as pd, numpy as np

try:
    # Find all gif files in the 'spinning_dancer' directory
    gifs = glob('spinning_dancer/*.gif')
    
    # Create the main window and a clock to measure total completion time
    win = visual.Window()
    c = core.Clock()

    i  = 0
    resp = []
    tstamps = pd.DataFrame() # Create an empty pandas DataFrame (not used in this script but initialized)
    t0  = c.getTime() # Record the start time
    
    # Loop through each frame of the GIF
    while i < len(gifs):
        # Create an ImageStim object for the current GIF frame
        gobj = visual.ImageStim(win, image = gifs[i])
        gobj.autoDraw = True
        
        # Present this frame for 5 screen refreshes (flips)
        # Assuming a 60Hz monitor, each frame will be shown for ~5/60 seconds
        for k in range(5):
            win.flip()

        i += 1
        # Check for any keyboard response
        resp = event.getKeys()
        if len(resp) > 0:
            # If the escape key is pressed, interrupt the animation immediately
            if resp[0] == 'escape':
                raise KeyboardInterrupt

        

    # Record the end time
    t1 = c.getTime()

    print("time of completing the loops: %.3f s" % (t1 - t0) )


finally:
    win.close()
