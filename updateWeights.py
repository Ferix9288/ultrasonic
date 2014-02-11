#Scripts to update the weights in classifer python file
#Too time consuming to manually change

f = open("updateWeights.txt", "r")
index = 0
for line in f:
	line = line.rstrip("\n")
	if index == 0: 
		print "weights_swipeRight = Vector(" + line + ", SWIPE_RIGHT)"
	elif index == 1:
		print "weights_swipeLeft = Vector(" + line + ", SWIPE_LEFT)"
	elif index == 2:
		print "weights_swipeUp = Vector(" + line + ", SWIPE_UP)"
	elif index == 3:
		print "weights_swipeDown = Vector(" + line + ", SWIPE_DOWN)"
	elif index == 4:
		print "weights_circle = Vector(" + line + ", CIRCLE)"
	elif index == 5:
		print "weights_v = Vector(" + line + ", V)"
	elif index == 6:
		print "weights_caret = Vector(" + line + ", CARET)"
	elif index == 7:
		print "weights_triangle = Vector(" + line + ", TRIANGLE)"

	index += 1
