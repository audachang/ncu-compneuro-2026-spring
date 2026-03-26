# -*- coding:utf-8 -*-
# get time stamps of mouse clicks

from psychopy import visual, core, event
import numpy as np

# Create the main window
win = visual.Window()

# Create the mouse object
mou = event.Mouse()

# Create graphic objects (a yellow rectangle and a white circle)
rect = visual.Rect(win, pos = (-0.5, 0), fillColor=(1,1,0))
rect.setAutoDraw(True)
circle = visual.Circle(win, pos = (0.5, 0))
circle.setAutoDraw(True)

# Text stimulus for notifications
notice = visual.TextStim(win, text = '')
notice.autoDraw = True

buttons = mou.getPressed()
i = 1
# Reset mouse click timers
mou.clickReset()

while i < 6: # Loop for five clicks total
    buttons, times = mou.getPressed(getTime = True) # Check for mouse click and timestamps
    
    # Check if the left button (buttons=[0]) was pressed inside the 'rect' shape
    if mou.isPressedIn(rect, buttons=[0]): # Detecting left-click on a shape
        notice.text = "You pressed the rect at %.3f (click %d)." % (times[0], i)
        i += 1
    # Check if the left button (buttons=[0]) was pressed inside the 'circle' shape
    elif mou.isPressedIn(circle, buttons=[0]): # Detecting left-click on a shape
        notice.text = "You pressed the circle at %.3f (click %d)." % (times[0], i)
        i += 1
    win.flip()

    # Keep waiting if any button is still pressed to prevent multiple registrations from a single long click
    while np.any(buttons):
        buttons, times = mou.getPressed(getTime = True) # Re-check for mouse click


core.wait(1) #wait 1 second for final viewing


win.close()
