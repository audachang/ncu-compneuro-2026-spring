# -*- coding:utf-8 -*-
# get time stamps of mouse clicks

from psychopy import visual, core, event
import numpy as np

# Create the main window (not full screen)
win = visual.Window(fullscr = False)

# Create the mouse object to track mouse events
mou = event.Mouse()

# Setup a text stimulus to display status
notice = visual.TextStim(win, text = 'Start waiting for a click...')
notice.setAutoDraw(True)

# Reset the mouse clock to start timing from 0
mou.clickReset() # start timing
win.flip()

while True:
    # Detect click and get both buttons array and their respective timestamps
    buttons, times = mou.getPressed(getTime = True)
    win.flip()

    # If any button was pressed, exit the polling loop
    if np.any(buttons):
        break

# Draw the button pressed and its corresponding timestamp
# np.where(buttons)[0][0] gets the index of the first pressed button
notice.text = "Got pressed on button %d at %.3f sec." % \
    (np.where(buttons)[0][0],times[np.where(buttons)[0][0]])
win.flip()
#core.wait(8)

# Wait for a keyboard press before closing
event.waitKeys()

# Close the window
win.close()
