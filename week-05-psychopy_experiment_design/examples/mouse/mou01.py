# -*- coding:utf-8 -*-
# create a mouse object and detect which key is pressed

from psychopy import visual, core, event
import numpy as np

try:
    # Create the main window
    win = visual.Window()

    # Create the mouse object to track mouse events
    mou = event.Mouse()
    # Labels for the boolean list returned by mou.getPressed()
    moukeylab = ['right','middle', 'left']
    
    # Text stimulus to display status
    notice = visual.TextStim(win, text = 'Waiting for a click....')
    notice.setAutoDraw(True)

    # Get the initial state of the mouse buttons [left, middle, right]
    buttons = mou.getPressed()
    while True:
        # Continuously check for button presses
        buttons = mou.getPressed()
        print(buttons)
        # Check if any button is currently pressed
        if buttons.count(1) > 0:
            # Update the text with the name of the pressed button
            notice.text = f"Got pressed at {moukeylab[buttons.index(1)]}"
            # If the middle button (index 1) is pressed, raise an exception to break the loop
            if buttons.index(1)==1:
                raise
        # Render the updated text to the screen
        win.flip()



    event.waitKeys()

except RuntimeError:
    print("Middle button hit!")

    

finally:
    win.close()
