from psychopy import visual


win = visual.Window(fullscr=False)



# Test 1: Simply flipping the window (takes 1 screen refresh cycle)
def testflip(win):
    win.flip()

# Test 2: Double flipping with color changes (takes 2 screen refresh cycles)
def testflip2(win):
    win.setColor([-1, -1, -1]) # Set background to black
    win.flip()
    win.setColor([1, 1, 1]) # Set background to white
    win.flip()

"""
After run this script, type

%timeit testflip(win)

or

%timeit testflip2(win)

to assess the timing information


type

win.close()

before ending your testing
"""
