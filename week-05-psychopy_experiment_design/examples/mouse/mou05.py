# -*- coding:utf-8 -*-
"""
Check if mouse cursor moved more than a defined distance from coordinate (x,y)

"""

from psychopy import visual, core, event
import numpy as np

# Create window and clock
win = visual.Window()
c = core.Clock()

# Create the mouse object
mou = event.Mouse()

# Setup a text stimulus for instructions
txt = visual.TextStim(win, text = "")
txt.autoDraw = True

apos = []
buttons = mou.getPressed()
# Bring the cursor to the center
mou.setPos() 

# Define target position and draw a circle around it
tarposi = (-0.5, 0.75)
circle = visual.Circle(win, pos = tarposi, radius = 0.25, fillColor="gray")
circle.autoDraw = True

# Initial position set to the target position
mou.setPos(tarposi)
pos = mou.getPos()
mou.clickReset()
while not np.any(buttons): # Loop continuously until any button is pressed
    # Update the internal state of mouse pos
    mou.getPos()
    # Wait until the mouse has moved more than exactly 0.25 units away from `tarposi`
    while not mou.mouseMoved(distance = 0.25, reset = tarposi):
        txt.text = "Move the cursor to figure out the boundary"
        win.flip()

    # Reset mouse position to tarposi after it crossed the boundary
    mou.setPos(tarposi)
    txt.text = "Mouse moved! Press any button to quit..."
    win.flip()
    
    # Wait for up to 1 second holding this message, or until a button is clicked
    t0 = c.getTime()
    while (c.getTime() - t0) < 1 and (not np.any(buttons)):
        buttons = mou.getPressed()








win.close()
