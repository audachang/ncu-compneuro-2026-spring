from psychopy import visual, core

win = visual.Window()


ck = core.Clock()

t0 = ck.getTime()
# Test 1: Instantiating the object INSIDE the render loop
# Creating visual objects inside a high-frequency loop is computationally expensive
for i in range(3):
	rect = visual.Rect(win, fillColor =[1,1,1])	
	rect.draw()
	win.flip()
t1 = ck.getTime()

du = t1 - t0
#print("the duration was %f"%du)
print(f"the duration was {du}")

# Test 2: Instantiating the object OUTSIDE the render loop
# This approach is much more efficient because it only creates the object once
rect = visual.Rect(win, fillColor =[1,1,1])
t0 = ck.getTime()
for i in range(3):
		
	rect.draw()
	win.flip()
t1 = ck.getTime()

du = t1 - t0
#print("the duration was %f"%du)
print(f"the duration was {du}")

#core.wait(1)
win.close()
