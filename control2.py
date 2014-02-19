import classifier 
from classifier import *
import feature_calculator
from feature_calculator import *

#import sending keys
from sendKeyboard import *
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

movement = 5

#Code taken from: http://code.activestate.com/lists/python-win32/12702/
#-------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-

import win32api,time,win32con


def keyb(ch=None,shift=False,control=False,alt=False, delaik=0.02):
    for b in ch:
        c=b
        if (b>='A' and b<='Z') or shift:
            win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
        if b>='a' and b<='z':
            c=b.upper()
        if alt:
            win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
            time.sleep(0.250)
        if control:
            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
        if isinstance(b,(int)):
            cord=b
        else:
            cord=ord(c)

        win32api.keybd_event(cord, 0, win32con.KEYEVENTF_EXTENDEDKEY | 0, 0)
        if delaik>0.0:
            time.sleep(delaik)
        win32api.keybd_event(cord, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
        if delaik>0.0:
            time.sleep(delaik)

        if control:
            win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
        if alt:
            win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.05)
        if (b>='A' and b<='Z') or shift:
            win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)



# time.sleep(5)  #user has 5 sec for prepare a target-window
# keyb("AZERTYUIOP ")
# keyb("azertyuiop")
# keyb("\r")
# keyb("1234567890",shift=True) #shift == True for french keyboard
# keyb("\n")
# keyb("AAAAAAAAA\n")
# time.sleep(1)
# keyb("f",alt=True)  # {Alt} F   (ouvre menu ?)
# time.sleep(1)
# keyb([27,27])  # 2 x {Escape}
#-------------------------------------------------------------------------------------

from win32gui import GetWindowText, GetForegroundWindow

def main():
    
    track_data = 0;
    sensor_data = [];
    
    sensor_state = 0;
    sensor0 = 0;
    sensor1 = 0;
    sensor2 = 0;

    cl = classifier.Classifier(ALL_WEIGHTS, feature_calculator.FeatureCalculator(FEATURE_ON))

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
                g = cl.classifying_data(sensor_data);
                gesture_handling(g)
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

def gesture_handling(gesture):
    current_window = GetWindowText(GetForegroundWindow())
    print current_window
    if current_window != "Avalanche":
        if gesture == SWIPE_RIGHT:
            speech.say("Swiping Right")
        elif gesture == SWIPE_LEFT:
            speech.say("Swiping Left")
        elif gesture == SWIPE_UP:
            speech.say("Swiping Up")
        elif gesture == SWIPE_DOWN:
            speech.say("Swiping Down")
        elif gesture == CIRCLE:
            speech.say("You drew a circle. Whoa!")
        elif gesture == V:
            speech.say("You drew a V. So amazing!")
        elif gesture == CARET:
            speech.say("You drew a caret. Phenomenal!")
        elif gesture == TRIANGLE:
            speech.say("You drew a triangle. Wow!")
    else:
        print gestureToText(gesture)
        if gesture == SWIPE_RIGHT:
            SendInput(Keyboard(KEY_D))
            time.sleep(0.2)
            SendInput(Keyboard(KEY_D, KEYEVENTF_KEYUP))
        elif gesture == SWIPE_LEFT:
            SendInput(Keyboard(KEY_A))
            time.sleep(0.2)
            SendInput(Keyboard(KEY_A, KEYEVENTF_KEYUP))
        elif gesture == SWIPE_UP:
            #speech.say("Swiping Up")
            print "HERE"
            SendInput(Keyboard(VK_UP))
            time.sleep(0.2)
            SendInput(Keyboard(VK_UP, KEYEVENTF_KEYUP))
                # elif gesture == SWIPE_DOWN:
        #     speech.say("Swiping Down")
        # elif gesture == CIRCLE:
        #     speech.say("You drew a circle. Whoa!")
        # elif gesture == V:
        #     speech.say("You drew a V. So amazing!")
        # elif gesture == CARET:
        #     speech.say("You drew a caret. Phenomenal!")
        # elif gesture == TRIANGLE:
        #     speech.say("You drew a triangle. Wow!")



if __name__ == "__main__":
    main();
