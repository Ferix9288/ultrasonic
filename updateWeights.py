#Scripts to update the weights in classifer python file
#Too time consuming to manually change

f = open("updateWeights.txt", "r")
wf = open("copythis.txt", "w")
index = 0
for line in f:
	line = line.rstrip("\n")
	if index == 0: 
		wf.write("weights_swipeRight = Vector(" + line + ", SWIPE_RIGHT)")
		print "weights_swipeRight = Vector(" + line + ", SWIPE_RIGHT)"
	elif index == 1:
		wf.write("weights_swipeLeft = Vector(" + line + ", SWIPE_LEFT)")
		print "weights_swipeLeft = Vector(" + line + ", SWIPE_LEFT)"
	elif index == 2:
		wf.write("weights_swipeUp = Vector(" + line + ", SWIPE_UP)")
		print "weights_swipeUp = Vector(" + line + ", SWIPE_UP)"
	elif index == 3:
		wf.write("weights_swipeDown = Vector(" + line + ", SWIPE_DOWN)")
		print "weights_swipeDown = Vector(" + line + ", SWIPE_DOWN)"
	elif index == 4:
		wf.write("weights_circle = Vector(" + line + ", CIRCLE)")
		print "weights_circle = Vector(" + line + ", CIRCLE)"
	elif index == 5:
		wf.write("weights_v = Vector(" + line + ", V)")
		print "weights_v = Vector(" + line + ", V)"
	elif index == 6:
		wf.write("weights_caret = Vector(" + line + ", CARET)")
		print "weights_caret = Vector(" + line + ", CARET)"
	elif index == 7:
		wf.write("weights_triangle = Vector(" + line + ", TRIANGLE)")
		print "weights_triangle = Vector(" + line + ", TRIANGLE)"

	index += 1
