#CONFIG/SET-UP FILE - THE GO TO FILE TO TWEAK PARAMETERS

#SELECT WHICH FEATURES YOU WANT ON
FEATURE_ON = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

#Feature Vector
#Vector[0] = starting location? -1 = left, 0 = neutral, 1 = right
#Vector[1] = end location? -1 = left, 0 = neutral, 1 =  right
#Vector[2] = starting location? -1 = bottom, 0 = neutral, 1 = top
#Vector[3] = end location? -1 = bottom, 0 = neutral, 1 = top
#Vector[4] = Does gesture loop back on itself? (Based on states)
#Vector[5] = Same as above but calculated based on sensor values
#Vector[6] = Does gesture loop hit all sensors? (Based on values)
#Vector[7] = What's the overall directions of each sensor? 
#Vector[8] = overall direction of sensor with max value?
#Vector[9] = 1 if large range of motion, -1 otherwise
#Vector[10] = only look at range 


#Brainstorm features for classifying features (worth to implement?)
#Numbers for each sensor: is it increasing, decreasing, staying the same? (discusses up vs down)
#The average of all three sensors (if all of them are the same height and all active, most likely a line)
#Circle: did it go back to where it was

# What's being given? All three numbers at the same time
# What can I do? Plot numbers, calculate all the features

#STATES (FROM ARDUINO)
OUTSIDE = 0
LEFT_DOWN = 1
MIDDLE_DOWN = 2
RIGHT_DOWN = 3
LEFT_MIDDLE = 4
NEUTRAL = 5
RIGHT_MIDDLE = 6
LEFT_UP = 7
MIDDLE_UP = 8
RIGHT_UP = 9
# SPAN_ALL = 10
# SWIPE_RIGHT = 11
# SWIPE_LEFT = 12
# GESTURE = 13

#TYPES OF GESTURES
SWIPE_RIGHT = 0;
SWIPE_LEFT = 1;
SWIPE_UP = 2;
SWIPE_DOWN = 3;
CIRCLE = 4;
V = 5;
CARET = 6;
TRIANGLE = 7;

HEART = 8;
UNKNOWN = 9;
FEATURE = 10; #filler
GESTURE = UNKNOWN;

#Noise threshold for picking out the range (max/low)
NOISE_MAX_THRESHOLD = 3
NOISE_MIN_THRESHOLD = 3
RANGE_THRESHOLD = 8


class Vector:


    def __init__(self, init_data = [], gesture = UNKNOWN):
        self.data = init_data
        self.gesture = gesture

    def dot_product(self, other_vector):
        if (len(self.data) != len(other_vector.data)):
            raise "Dot product error! Vector not same size"
        result = 0;
        for i in range(0, len(self.data)):
            result += self.data[i] * other_vector.data[i]
        return result

    def get_data(self):
        return self.data

    def add_data(self, i):
        self.data.append(i)

#~~~~~~~WEIGHTS~~~~~~~~~~~

weights_swipeRight = Vector([-3, 0, 0, -2, 0, 3, 7, 4, -3, -30, 0], SWIPE_RIGHT)
weights_swipeLeft = Vector([4, -10, -3, 1, -1, 1, 1, 3, 2, -30, 0], SWIPE_LEFT)
weights_swipeUp = Vector([-3, 0, 2, 6, 2, -4, -8, 1, 1, -1, 0], SWIPE_UP)
weights_swipeDown = Vector([-2, 4, 0, -7, -1, -5, -1, -5, -2, 3, 0], SWIPE_DOWN)
weights_circle = Vector([1, 4, -3, -4, 0, 3, 2, 3, 0, 4, 0], CIRCLE)
weights_v = Vector([4, 4, 1, -1, 0, 1, 2, -2, -1, -1, 0], V)
weights_caret = Vector([0, 0, -1, -2, -3, -1, 8, 3, 1, 5, 0], CARET)
weights_triangle = Vector([0, -1, 3, 6, 4, 3, 5, -5, 3, 9, 0], TRIANGLE)

# weights_swipeRight = Vector([-2, -2, -1, -1, -1, 3, 7, 3, -2, -2], SWIPE_RIGHT)
# weights_swipeLeft = Vector([4, -9, -3, -2, 1, 0, 1, 1, 0, -2], SWIPE_LEFT)
# weights_swipeUp = Vector([-3, -1, 2, 7, 1, -4, -8, 2, 2, 0], SWIPE_UP)
# weights_swipeDown = Vector([-3, 5, 2, -7, -3, -5, -1, -3, -4, 5], SWIPE_DOWN)
# weights_circle = Vector([0, 1, -3, -3, 0, 4, 0, -1, 0, 0], CIRCLE)
# weights_v = Vector([5, 5, 1, -1, 1, 2, 3, -1, -2, 0], V)
# weights_caret = Vector([0, 0, -3, 0, 1, -2, 4, 1, 1, 1], CARET)
# weights_triangle = Vector([0, 2, 4, 4, 1, 3, 10, 0, 6, 14], TRIANGLE)

ALL_WEIGHTS = []
ALL_WEIGHTS.append(weights_swipeRight)
ALL_WEIGHTS.append(weights_swipeLeft)
ALL_WEIGHTS.append(weights_swipeUp)
ALL_WEIGHTS.append(weights_swipeDown)
ALL_WEIGHTS.append(weights_circle)
ALL_WEIGHTS.append(weights_v)
ALL_WEIGHTS.append(weights_caret)
ALL_WEIGHTS.append(weights_triangle)