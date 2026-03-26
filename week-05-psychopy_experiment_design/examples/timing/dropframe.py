from psychopy import visual, logging
import matplotlib.pyplot as plt


win = visual.Window([800,600])

# Enable recording of the interval between consecutive win.flip() calls
win.recordFrameIntervals = True

# By default, the threshold is set to 120% of the estimated refresh
# duration, but arbitrary values can be set.
#
# I've got 85Hz monitor and want to allow 4 ms tolerance; any refresh that
# takes longer than the specified period will be considered a "dropped"
# frame and increase the count of win.nDroppedFrames.
# Define what duration constitutes a "dropped frame"
win.refreshThreshold = 1/60 + 0.008

# Present 60 frames (1 second at 60Hz)
for i in range(60):
	win.flip()

# Set the log module to report warnings to the standard output window
# (default is errors only).
logging.console.setLevel(logging.WARNING)

print('Overall, %i frames were dropped.' % win.nDroppedFrames)
win.close()

# Plot the distribution/trajectory of the individual frame intervals
plt.plot(win.frameIntervals)
plt.show()

# Save the frame intervals to a text file for further analysis and clear them from memory
win.saveFrameIntervals(fileName='frameIntervals.txt', clear=True)
