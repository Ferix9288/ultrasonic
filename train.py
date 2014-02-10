#Serial connection
import serial
#COM_LIST = ['COM3', 'COM4', 'COM5']
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = 0
which_com = 0

for i in range(0, 16):
    try:
        com = 'COM' + str(i)
        ser = serial.Serial(com)
    except:
        pass
    else:
        which_com = com
        print "COM PORT:", which_com, " Found!"
        break;

if which_com == 0:
    print "No COM ports found!"

import win32api, win32con, win32gui
from time import sleep
# def click(x,y):
#     win32api.SetCursorPos((x,y))
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

import webbrowser
new = 2 # open in a new tab, if possible

# open a public URL, in this case, the webbrowser docs
url = "http://google.com"

import speech

def move(x,y):
    win32api.SetCursorPos((x,y))

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    #double click
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def get_pos():
    flags, hcursor, (x,y) = win32gui.GetCursorInfo()
    return x, y

movement = 12

# import win32com

# shell = win32com.client.Dispatch("WScript.Shell")
# shell.Run("notepad");
# win32api.Sleep(100)
# shell.AppActivate("myApp")
# win32api.Sleep(100)
# shell.SendKeys("%")
# win32api.Sleep(500)
# shell.SendKeys("t")
# win32api.Sleep(500)
# shell.SendKeys("r")
# win32api.Sleep(500)
# shell.SendKeys("name")
# win32api.Sleep(500)
# shell.SendKeys("{ENTER}")
# win32api.Sleep(2500)

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
UNKNOWN = 0;
SWIPE_RIGHT = 1;
SWIPE_LEFT = 2;
SWIPE_UP = 3;
SWIPE_DOWN = 4;
CIRCLE = 5;
HEART = 6;
TRIANGLE = 7;
FEATURE = 8; #filler

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

    while(True):
        #print current_x, current_y
        try:
            message = ser.read()
            current_x, current_y = get_pos()
            if message == 'A': #go up
                move(current_x, current_y-movement)
            elif message == 'a': #go down
                move(current_x, current_y+movement)
            elif message == 'R': #go upright
                move(current_x+movement, current_y-movement)
            elif message == 'r': #go downright
                move(current_x+movement, current_y+movement)
            elif message == 'b': #go right
                move(current_x+movement, current_y)
            elif message == 'L': #go upleft
                move(current_x-movement, current_y-movement)
            elif message == 'l': #go downleft
                move(current_x-movement, current_y+movement)
            elif message == 'c': #go left
                move(current_x-movement, current_y)
            elif message == 'C': #click
                click(current_x, current_y)
            elif message == 'x':
                webbrowser.open(url,new=new)
            elif message == 'y':
                speech.say("You're Awesome!")
            elif message == 'd':
                #speech.say("Processing!")
                print "Processing!"
                process_data(sensor_data);
                sensor_data = []
            else:
                #print "Track data: " + str(track_data)
                message = ord(message)
                if track_data == 0: 
                    sensor_state = message;
                    track_data += 1;
                elif track_data == 1:
                    sensor0_data = message;
                    track_data += 1;
                elif track_data == 2:
                    sensor1_data = message;
                    track_data += 1;
                elif track_data == 3:
                    sensor2_data = message;
                    new_array = [sensor_state, sensor0_data, sensor1_data, sensor2_data]
                    sensor_data.append(new_array)
                    track_data = 0;
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            raise


#Brainstorm features for classifying features (worth to implement?)
#Numbers for each sensor: is it increasing, decreasing, staying the same? (discusses up vs down)
#The average of all three sensors (if all of them are the same height and all active, most likely a line)
#Circle: did it go back to where it was

# What's being given? All three numbers at the same time
# What can I do? Plot numbers, calculate all the features

#Feature Vector
#Vector[0] = starting location? -1 = left, 0 = middle, 1 = right
#Vector[1] = Does gesture loop back on itself? (Based on states)
#Vector[2] = Same as above but calculated based on sensor values
#Vector[3] = Does gesture loop hit all sensors? (Based on values)
#Vector[4] = What's the overall directions of each sensor? 
#Vector[5] = overall direction of sensor with max value?

#Works with swipe up, right, down, left, circle
# weights_unknown = Vector([0, 0, 0, 0, 0], UNKNOWN)
# weights_swipeRight = Vector([-3, -3, -4, 1, 0], SWIPE_RIGHT)
# weights_swipeLeft = Vector([3, -2, 1, 4, 2], SWIPE_LEFT)
# weights_swipeUp = Vector([-1, -1, -2, 3, 1], SWIPE_UP)
# weights_swipeDown = Vector([0, 0, -1, -6, -3], SWIPE_DOWN)
# weights_circle = Vector([1, 3, 1, 2, 0], CIRCLE)
# weights_heart = Vector([0, 0, 0, 0, 0], HEART)
# weights_triangle = Vector([0, 0, 0, 0, 0], TRIANGLE)

weights_unknown = Vector([0, 0, 0, 0, 0, 0], UNKNOWN)
weights_swipeRight = Vector([-7, -5, 6, 5, 0, 4], SWIPE_RIGHT)
weights_swipeLeft = Vector([9, -5, 0, 7, 0, 2], SWIPE_LEFT)
weights_swipeUp = Vector([-5, 1, -6, -10, 6, 1], SWIPE_UP)
weights_swipeDown = Vector([2, 2, 3, -9, -2, -2], SWIPE_DOWN)
weights_circle = Vector([1, 3, 1, 0, 2, 0], CIRCLE)


weights_heart = Vector([0, 0, 0, 0, 0, 0], HEART)
weights_triangle = Vector([0, 0, 0, 0, 0, 0], TRIANGLE)

#heart
#triangle
all_weights = []
all_weights.append(weights_unknown)
all_weights.append(weights_swipeRight)
all_weights.append(weights_swipeLeft)
all_weights.append(weights_swipeUp)
all_weights.append(weights_swipeDown)
all_weights.append(weights_circle)
#all_weights.append(weights_heart)
#all_weights.append(weights_triangle)
    

def process_data(array):
    print array
    gesture, fv = calculate_features(array)

    right_answer = SWIPE_RIGHT

    print gesture

    if gesture != right_answer and gesture != UNKNOWN:
        update_weights(gesture, right_answer, fv)
        print "UPDATED WEIGHTS!"
    print "Length of processed: " + str(len(array)) 
    print_weights()

def print_weights():
    for w in all_weights:
        print w.data


def update_weights(wrong_gesture, right_gesture, feature_vector):
    wrong_weights = all_weights[wrong_gesture]
    right_weights = all_weights[right_gesture]
    for i in range(0, len(wrong_weights.data)):
        if feature_vector.data[i] > 0:
            #Reduces weight by feature vector
            wrong_weights.data[i] -= feature_vector.data[i]
        else: #feature vector negative
            if wrong_weights.data[i] > 0:
                wrong_weights.data[i] += abs(feature_vector.data[i])
            else:
                wrong_weights.data[i] -= abs(feature_vector.data[i])            
    for i in range(0, len(right_weights.data)):
        if (feature_vector.data[i]) > 0:
            right_weights.data[i] += feature_vector.data[i]
        else:
            if right_weights.data[i] > 0:
                right_weights.data[i] -= abs(feature_vector.data[i])
            else:
                right_weights.data[i] += abs(feature_vector.data[i])
       





    #based on gesture, do something

def calculate_features(array):
    feature_vector = Vector([], UNKNOWN);
    gesture = UNKNOWN
    if (len(array) < 2):
        return gesture, None

    first = array[0] 
    last = array[len(array)-1]

    state_first = first[0]
    state_last = last[0]

    #Vector[0] = starting location? -1 = left, 0 = middle, 1 = right
    if (state_first == LEFT_DOWN or state_first == LEFT_MIDDLE or state_first == LEFT_UP):
        feature_vector.add_data(-1)
    elif (state_first == MIDDLE_DOWN or state_first == NEUTRAL or state_first == MIDDLE_UP):
        feature_vector.add_data(0)
    else:
        feature_vector.add_data(1)
        
    #Vector[1] = Does gesture loop back on itself? (Based on states)
    if (state_first == state_last):
        feature_vector.add_data(1)
    else:
        feature_vector.add_data(-1)

    #Vector[2] = Same as above but calculated based on sensor values
    diff = total_difference(first, last)
    if (diff < 8):
        feature_vector.add_data(1)
    else:
        feature_vector.add_data(-1)


    #Average values for sensor0, sensor1, sensor2
    #Positive values for direction = increasing
    #Negative = decreasing, 0 = neutral
    sensor0_avg = first[1]
    sensor0_direction = 0
    previous_sensor0 = first[1]
    
    sensor1_avg = first[2]
    sensor1_direction = 0
    previous_sensor1 = first[2]

    sensor2_avg = first[3]
    sensor2_direction = 0
    previous_sensor2 = first[3]

    for i in range(1, len(array)):
        sensor0_avg += array[i][1]
        sensor1_avg += array[i][2]
        sensor2_avg += array[i][3]

        if (array[i][1] > previous_sensor0):
            sensor0_direction += 1
        elif (array[i][1] < previous_sensor0):
            sensor0_direction -= 1
        
        if (array[i][2] > previous_sensor1):
            sensor1_direction += 1
        elif (array[i][2] < previous_sensor1):
            sensor1_direction -= 1

        if (array[i][3] > previous_sensor2):
            sensor2_direction += 1
        elif (array[i][3] < previous_sensor2):
            sensor2_direction -= 1
        
        previous_sensor0 = array[i][1]
        previous_sensor1 = array[i][2]
        previous_sensor2 = array[i][3]

    #Before averaging and dividing the values (don't want to deal with floats)
    #Vector[3] = Does gesture loop hit all sensors? (Based on values)
    if (sensor0_avg != 0 and sensor1_avg != 0 and sensor2_avg != 0):
        feature_vector.add_data(1)
    else:
        feature_vector.add_data(-1)

    sensor0_avg = sensor0_avg / len(array)
    sensor1_avg = sensor1_avg / len(array)
    sensor2_avg = sensor2_avg / len(array)


    
    print "sensor0_avg: " + str(sensor0_avg)
    print "sensor1_avg: " + str(sensor1_avg)
    print "sensor2_avg: " + str(sensor2_avg)

    print "sensor0_dir: " + str(sensor0_direction)
    print "sensor1_dir: " + str(sensor1_direction)
    print "sensor2_dir: " + str(sensor2_direction)

   
  

    #Vector[4] = What's the overall directions of each sensor? 
    #If sum of directions fall within abs 2, then must likely circle/horizontal swipes
    sum_directions = sensor0_direction + sensor1_direction + sensor2_direction
    feature_vector.add_data(sum_directions)

    #Vector[5] = overall direction of sensor with max value?
    #Positive direction most likely indicate upward swipe
    #Negative Direction most likely indicate downward swipe

    #sensor0 = max
    if sensor0_avg >= sensor1_avg and sensor0_avg >= sensor2_avg:
        feature_vector.add_data(sensor0_direction)

    #sensor1 = max
    elif sensor1_avg >= sensor0_avg and sensor1_avg >= sensor2_avg:
        feature_vector.add_data(sensor1_direction)
       
    #sensor2 = max
    elif sensor2_avg >= sensor0_avg and sensor2_avg >= sensor1_avg:
        feature_vector.add_data(sensor2_direction)

    print feature_vector.get_data()


    #Calculate weights
    current_max = float("-inf")
    index_max = 0
    index = 0
    for weight in all_weights:
        if index == 0:
            index += 1 
            continue
        dot_product = weight.dot_product(feature_vector)
        print "DOT PRODUCT " + str(index) + ": " + str(dot_product)
        if dot_product > current_max:
            current_max = dot_product
            index_max = index
        index += 1 

    gesture = all_weights[index_max].gesture
    if (abs(current_max) < GESTURE_THRESHOLD):
        return UNKNOWN, feature_vector
    return gesture, feature_vector

def total_difference(array1, array2):
    total = 0;
    for i in range(1, len(array1)):
        total += abs(array1[i]-array2[i])
    return total

if __name__ == "__main__":
    main();
