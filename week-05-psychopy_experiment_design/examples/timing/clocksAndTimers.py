#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo for clocks and count-down timers
"""

#from __future__ import division
#from __future__ import print_function

from psychopy import core
# Wait for 0.5s to allow the system to settle before timing starts
core.wait(0.5)  

# create a clock to keep track of continuous time
# A clock starts counting from 0 immediately
clock = core.Clock()
clock.reset()  # whenever you like

# to create a timer you can 'add' time to the zero point
# and wait to get back to zero
timer = core.Clock()
timer.add(3)

# there's also a countdown timer (just a flip of the clock)
countDown = core.CountdownTimer()
countDown.add(3)

another = core.Clock()

print("down       up          clock")
# countDown.getTime() will get closer to 0 over time
while countDown.getTime() > 0:
    msg = "%.4f   %.4f   %.4f"
    # Print the current state of three timers at each iteration
    print(msg % (countDown.getTime(), timer.getTime(), clock.getTime()))
    core.wait(0.2)  # this combined + print will allow a gradual timing 'slip' (inaccuracy accumulating over time)

# use the timer, rather than wait(), to prevent the slip
print("\ndown          clock")
timer.reset()
timer.add(0.2) # Set timer target 0.2s from now
countDown.add(3) # Add 3 more seconds to countdown
while countDown.getTime() > 0:
    print("%.4f   %.4f" %(countDown.getTime(), clock.getTime()))
    # Polling the timer is more precise than using wait(), as we avoid accumulating delay
    while timer.getTime() < 0:  # includes the time taken to print
        print('Hello!')
        #pass
    timer.add(0.2) # Continually bump the timer up by 0.2s as soon as it crosses 0
print("The last run should have been precise sub-millisecond")

core.quit()

# The contents of this file are in the public domain.
