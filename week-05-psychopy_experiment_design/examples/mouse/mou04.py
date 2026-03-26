# -*- coding:utf-8 -*-
# plot the path of mouse movement

from psychopy import visual, core, event
import numpy as np

# Create the main window
win = visual.Window()

# Create the mouse object
mou = event.Mouse()

# Create a ShapeStim object to draw the path of the mouse movement
# Initially, the vertices contain just one point (0,0)
path = visual.ShapeStim(win, pos=[0,0],
                        vertices = [(0,0)],
                        closeShape = True)
path.setAutoDraw(True)

apos = []
buttons = mou.getPressed()
# Bring the cursor to the center
mou.setPos() 
pos = mou.getPos()
i = 0
mou.clickReset()

while True: # Loop continuously until a click happens
    buttons, times = mou.getPressed(getTime = True)
    # Get the current mouse position
    pos = mou.getPos()
    # Append the current position to the path list
    apos.append(pos)

    # Note: len(apos) > 1 is required because ShapeStim needs at least 2 vertices to draw a line
    if len(apos) > 1:
        path.vertices = apos

    # Break the loop if any button is clicked
    if np.any(buttons):
        break


    win.flip()




win.close()
