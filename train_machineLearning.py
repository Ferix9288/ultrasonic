#Grab all files
import os
import sys
import glob
import random

import classifier

all_files = []
for f in glob.glob("*.txt"):
    opened_file = open(f, "r")
    all_files.append(opened_file)
print all_files

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
GESTURE_THRESHOLD = 2

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

def main():
    
    track_data = 0;
    sensor_data = [];
    
    sensor_state = 0;
    sensor0 = 0;
    sensor1 = 0;
    sensor2 = 0;

    cl = classifier.Classifier()

    while(True):
        try: 
            #f = open(all_files[0], 'r');
            f = random.choice(all_files)
            text = f.readline()
            if not(text):
                f.close()
                all_files.remove(f)
                if not(all_files):
                    sys.exit(1)
            data = text.split('], ')
            the_data = data[0:-1]
            sensor_data = []
            for d in the_data:
                #remove brackets
                d = d[1:]
                
                subarray = d.split(',')
                one_data = []
                
                for ele in subarray:
                    one_data.append(int(ele))
                sensor_data.append(one_data)

            print sensor_data

            gesture_type = data[-1].rstrip('\n')
            print gesture_type


            if gesture_type == "swipeUp":
                right_gesture = SWIPE_UP
            elif gesture_type == "swipeDown":
                right_gesture = SWIPE_DOWN
            elif gesture_type == "swipeRight":
                right_gesture = SWIPE_RIGHT
            elif gesture_type == "swipeLeft":
                right_gesture = SWIPE_LEFT
            elif gesture_type == "circles":
                right_gesture = CIRCLE
            elif gesture_type == "v":
                right_gesture = V
            elif gesture_type == "caret":
                right_gesture = CARET
            elif gesture_type == "triangle":
                right_gesture = TRIANGLE


            cl.learning(sensor_data, right_gesture);

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            raise

if __name__ == "__main__":
    main();
