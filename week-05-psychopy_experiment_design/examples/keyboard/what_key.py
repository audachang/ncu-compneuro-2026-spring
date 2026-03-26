"""
2020-05-20
Created by Erik Chang

For showing key press string
Quit when esc is hit

"""
from psychopy import visual, event, core
# Initialize a global clock to track time
ck = core.Clock()
try:
	# Create a simple window, 400x400 pixels
	win = visual.Window([400,400])
	# Text stimulus to display the pressed key
	msg = visual.TextStim(win, text='press a key')
	# Text stimulus to display the instructions to quit
	escmsg = visual.TextStim(win, text = '<esc> to quit',\
				pos = (0,-.5))
	
	# Enable autoDraw so these messages remain on screen without needing to call draw() repeatedly
	escmsg.autoDraw=True
	msg.autoDraw = True
	# Render the initial frame
	win.flip()

	# Initialize the list containing key press information [[key_name, timestamp]]
	k = [['','']] 
	#count = 0

	# Continue looping until the 'escape' key is pressed
	while k[0][0] not in ['escape', 'esc']: # and count < 5:
		# Record the baseline time before waiting for a key
		t0 = ck.getTime()
		# Wait for any key press and get its timestamp
		k = event.waitKeys(timeStamped=ck)
		print(k)
		# Update the message with the pressed key and the latency (time since t0)
		msg.setText(f"key={k[0][0]}, time={k[0][1]-t0}")
		# Refresh the screen to display the updated message
		win.flip()
		#count += 1

finally:
	win.close()
