"""
2020-05-20
Created by Erik Chang

For showing how to record RT

"""
from psychopy import visual, event, core
from numpy import random

try:
	# Create a simple window, 400x400 pixels
	win = visual.Window([400,400])
	# Text stimulus to display the reaction time (RT)
	msg = visual.TextStim(win, text='', pos=(0, -.5))
	# Instructions stimulus
	sti = visual.TextStim(win, wrapWidth=2, text=
		'''
		\nPress left if the number is even.
		\nPress right if it is odd.\n\n
		\nHit <Esc> to quit.
		\nHit any key to continue...
		''')
	# Auto-draw ensures the RT message is always drawn without calling draw() explicitly
	msg.autoDraw = True
	# Draw the instructions and flip to screen
	sti.draw()
	win.flip()
	# Wait for the user to press any key before starting
	event.waitKeys()

	k = [''] # initialize the list containing key press
	count = 0
	# Create a clock to measure trial times and reaction times
	c = core.Clock()
	c.reset()
	# Loop until 'escape' is pressed or 5 trials are completed
	while k not in ['escape', 'esc'] and count < 5:
		# Set stimulus text to a random integer between 10 and 99
		sti.setText(random.randint(10,100))
		sti.draw()
		# Record the time right before the stimulus is shown
		t0 = c.getTime()
		win.flip()
		# Wait for specific keys and record their timestamps using the clock 'c'
		[[k, t1]] = event.getKeys(keyList=['left','right', 'escape'],\
		 			timeStamped=c)
		# Calculate reaction time (t1 - t0) and display it in milliseconds
		msg.setText(f"RT = {(t1-t0)*1000:4.0f} ms") # showing RT of last trial
		win.flip()
		# Wait for 1 second before the next trial
		core.wait(1)
		count += 1
finally:
	win.close()
