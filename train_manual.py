import classifier 
from classifier import *
import feature_calculator
from feature_calculator import *
#INSERT CURRENT GESTURE HERE
right_gesture = SWIPE_DOWN


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


def main():
    
    track_data = 0;
    sensor_data = [];
    
    sensor_state = 0;
    sensor0 = 0;
    sensor1 = 0;
    sensor2 = 0;
    cl = classifier.Classifier(ALL_WEIGHTS, feature_calculator.FeatureCalculator(FEATURE_ON))
    print FEATURE_ON
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
                cl.learning(sensor_data, right_gesture);
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

if __name__ == "__main__":
    main();
