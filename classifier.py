#Brainstorm features for classifying features (worth to implement?)
#Numbers for each sensor: is it increasing, decreasing, staying the same? (discusses up vs down)
#The average of all three sensors (if all of them are the same height and all active, most likely a line)
#Circle: did it go back to where it was

# What's being given? All three numbers at the same time
# What can I do? Plot numbers, calculate all the features

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

#Works with swipe up, right, down, left, circle
# weights_swipeRight = Vector([-7, 13, 0, 0, 0, -2, 1, 0, 0], SWIPE_RIGHT)
# weights_swipeLeft = Vector([13, -5, 0, 0, 0, 0, 0, 1, 0], SWIPE_LEFT)
# weights_swipeUp = Vector([0, 0, -5, 3, -2, 0, -6, -3, 10], SWIPE_UP)
# weights_swipeDown = Vector([0, 0, 4, -6, 0, 0, -6, -4, -9], SWIPE_DOWN)
# weights_circle = Vector([0, 0, 0, 0, 1, 0, -5, 10, 1], CIRCLE)
# weights_heart = Vector([0, 0, 0, 0, 0], HEART)
# weights_triangle = Vector([0, 0, 0, 0, 0], TRIANGLE)

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


class Classifier:

    weights_swipeRight = Vector([-5, 4, -2, 0, 3, -2, 1, -1, -1, 1], SWIPE_RIGHT)
    weights_swipeLeft = Vector([3, -3, -1, -2, 5, 0, 1, -3, -1, 1], SWIPE_LEFT)
    weights_swipeUp = Vector([3, 2, -5, 3, 2, -1, -4, 3, 6, 2], SWIPE_UP)
    weights_swipeDown = Vector([2, 0, 5, -5, -3, -7, 2, -5, -4, 3], SWIPE_DOWN)
    weights_circle = Vector([1, 1, -1, -4, 2, 5, 2, 5, 0, 6], CIRCLE)
    weights_v = Vector([1, 3, 3, 2, -1, -4, 3, -1, -1, 3], V)
    weights_caret = Vector([-4, -5, 0, 3, -5, 7, 8, 5, 1, -1], CARET)
    weights_triangle = Vector([0, -1, 0, 0, -2, 3, 3, -1, 1, 1], TRIANGLE)

    all_weights = []
    all_weights.append(weights_swipeRight)
    all_weights.append(weights_swipeLeft)
    all_weights.append(weights_swipeUp)
    all_weights.append(weights_swipeDown)
    all_weights.append(weights_circle)
    all_weights.append(weights_v)
    all_weights.append(weights_caret)
    all_weights.append(weights_triangle)

    def __init__(self):
        self.gesture = UNKNOWN

    def classifying_data(self, array):
        print array
        gesture, fv = self.calculate_features(array)
        return gesture

    def learning(self, array, right_answer):
        print array
        gesture, fv = self.calculate_features(array)

        print gesture

        if gesture != right_answer and gesture != UNKNOWN:
            self.update_weights(gesture, right_answer, fv)
            #print fv
            print "UPDATED WEIGHTS!"
        print "Length of processed: " + str(len(array)) 
        self.print_weights()

    def print_weights(self):
        for w in Classifier.all_weights:
            print w.data


    def update_weights(self, wrong_gesture, right_gesture, feature_vector):
        wrong_weights = Classifier.all_weights[wrong_gesture]
        right_weights = Classifier.all_weights[right_gesture]
        for i in range(0, len(wrong_weights.data)):
            #if wrong_weights.data[i] != 0: #don't update if 0, manually chosen these features don't matter
            if feature_vector.data[i] > 0:
                wrong_weights.data[i] -= feature_vector.data[i]
            else:
                wrong_weights.data[i] += abs(feature_vector.data[i])
            
        for i in range(0, len(right_weights.data)):
            #if right_weights.data[i] != 0: #don't update if 0, manually chosen these features don't matter
            if feature_vector.data[i] > 0:
                right_weights.data[i] += feature_vector.data[i]
            else:
                right_weights.data[i] -= abs(feature_vector.data[i])
       
    #based on gesture, do something

    def calculate_features(self, array):
        feature_vector = Vector([], UNKNOWN);
        gesture = UNKNOWN
        if (len(array) < 3):
            return gesture, None

        #Last Data is always the noisest because user has to take hand away. Filter it out.
        array = array[0:len(array)-1]
        print "Filtered Array: " + str(array)

        first = array[0] 
        last = array[len(array)-1]

        state_first = first[0]
        state_last = last[0]

        #Vector[0] = starting location? -1 = left, 1 = right
        which_sensor = 1
        if (state_first == RIGHT_DOWN or state_first == RIGHT_MIDDLE or state_first == RIGHT_UP):
            feature_vector.add_data(1)
            which_sensor = 3 #Right sensor
        elif state_first == MIDDLE_DOWN or state_first == NEUTRAL or state_first == MIDDLE_UP:
            feature_vector.add_data(0)
            which_sensor = 2 #Middle sensor
        else:
            feature_vector.add_data(-1)
            which_sensor = 1 #Left Sensor

        #Vector[1] = end location? -1 = left, 0 = neutral, 1 =  right
        if (state_last == RIGHT_DOWN or state_last == RIGHT_MIDDLE or state_last == RIGHT_UP):
            feature_vector.add_data(1)
        elif state_last == MIDDLE_DOWN or state_last == NEUTRAL or state_last == MIDDLE_UP:
            feature_vector.add_data(0)
        else:
            feature_vector.add_data(-1)

        #Vector[2] = starting location? -1 = bottom, 1 = top
        if (state_first == LEFT_DOWN or state_first == MIDDLE_DOWN or state_first == RIGHT_DOWN):
            feature_vector.add_data(-1)
        elif state_first == LEFT_MIDDLE or state_first == NEUTRAL or state_first == RIGHT_MIDDLE:
            feature_vector.add_data(0) 
        else:
            feature_vector.add_data(1)
        
        #Vector[3] = end location? -1 = left, 0 = neutral, 1 =  right
        if (state_last == LEFT_DOWN or state_last == MIDDLE_DOWN or state_last == RIGHT_DOWN):
            feature_vector.add_data(-1)
        elif state_last == LEFT_MIDDLE or state_last == NEUTRAL or state_last == RIGHT_MIDDLE:
            feature_vector.add_data(0) 
        else:
            feature_vector.add_data(1)
        
        #Vector[4] = Does gesture loop back on itself? (Based on states)
        if (state_first == state_last):
            feature_vector.add_data(1)
        else:
            feature_vector.add_data(-1)

        #Vector[5] = Same as above but calculated based on sensor values
        #Difference only based on one sensor
        diff = self.sensor_difference(first, last, which_sensor)
        if diff  == -1:
            feature_vector.add_data(0)
        elif diff < 9:
            feature_vector.add_data(1)   
        else:
            feature_vector.add_data(-1)


        #Average values for sensor0, sensor1, sensor2
        #Positive values for direction = increasing
        #Negative = decreasing, 0 = neutral
        sensor0_total = first[1]
        sensor0_direction = 0
        previous_sensor0 = first[1]
        actual_sensor0 = len(array);
        
        sensor1_total = first[2]
        sensor1_direction = 0
        previous_sensor1 = first[2]
        actual_sensor1 = len(array);

        sensor2_total = first[3]
        sensor2_direction = 0
        previous_sensor2 = first[3]
        actual_sensor2 = len(array);

        fluctunate_states = 0
        previous_state = first[0]

        max_seen = float("-inf")
        min_seen = float("inf")

        for i in range(1, len(array)):
            sensor0_total += array[i][1]
            sensor1_total += array[i][2]
            sensor2_total += array[i][3]

            if (array[i][0]) != previous_state:
                fluctunate_states += 1

            if (array[i][1] != 0):
                if array[i][1] > max_seen:
                    max_seen = array[i][1]
                
                if array[i][1] < min_seen:
                    min_seen = array[i][1]     

                if (array[i][1] > previous_sensor0):
                    sensor0_direction += 1
                elif (array[i][1] < previous_sensor0):
                    sensor0_direction -= 1

                previous_sensor0 = array[i][1]
            else:
                actual_sensor0 -= 1

            if (array[i][2]!=0):     

                if array[i][2] > max_seen:
                    max_seen = array[i][2]
                
                if array[i][2] < min_seen:
                    min_seen = array[i][2]     

       
                if (array[i][2] > previous_sensor1):
                    sensor1_direction += 1
                elif (array[i][2] < previous_sensor1):
                    sensor1_direction -= 1

                previous_sensor1 = array[i][2]
            else:
                actual_sensor1 -= 1

        
            if (array[i][3]!=0):                        
        
                if array[i][3] > max_seen:
                    max_seen = array[i][3]
                
                if array[i][3] < min_seen:
                    min_seen = array[i][3]    

                if (array[i][3] > previous_sensor2):
                    sensor2_direction += 1
                elif (array[i][3] < previous_sensor2):
                    sensor2_direction -= 1
                
                previous_sensor2 = array[i][3]
            else:
                actual_sensor2 -= 1

        print "sensor0_total: " + str(sensor0_total)
        print "sensor1_total: " + str(sensor1_total)
        print "sensor2_total: " + str(sensor2_total)
        print "fluctunate_states: " + str(fluctunate_states)
        print "max seen: " + str(max_seen)
        print "min seen: " + str(min_seen)

        #Before averaging and dividing the values (don't want to deal with floats)
        #Vector[6] = Does gesture loop hit all sensors? (Based on values)
        if (sensor0_total != 0 and sensor1_total != 0 and sensor2_total != 0):
            feature_vector.add_data(1)
        else:
            feature_vector.add_data(0)

        sensor0_avg = sensor0_total / actual_sensor0
        sensor1_avg = sensor1_total / actual_sensor1
        sensor2_avg = sensor2_total / actual_sensor2

        print "sensor0_avg: " + str(sensor0_avg)
        print "sensor1_avg: " + str(sensor1_avg)
        print "sensor2_avg: " + str(sensor2_avg)

        print "sensor0_dir: " + str(sensor0_direction)
        print "sensor1_dir: " + str(sensor1_direction)
        print "sensor2_dir: " + str(sensor2_direction)

        #Vector[7] = What's the overall directions of each sensor? 
        #If sum of directions fall within abs 3, then must likely circle/horizontal swipes
        sum_directions = sensor0_direction + sensor1_direction + sensor2_direction
        if (abs(sum_directions) <= 3):
            feature_vector.add_data(1)
        else:
            feature_vector.add_data(-1)
            

        #Vector[8] = overall direction of sensor with max value?
        #Positive direction most likely indicate upward swipe
        #Negative Direction most likely indicate downward swipe

        #sensor0 = max
        if sensor0_total >= sensor1_total and sensor0_total >= sensor2_total:
            if sensor0_direction > 0:
                feature_vector.add_data(1)
            else:
                feature_vector.add_data(-1)
           
        #sensor1 = max
        elif sensor1_total >= sensor0_total and sensor1_total >= sensor2_total:
            if sensor1_direction > 0:
                feature_vector.add_data(1)
            else:
                feature_vector.add_data(-1)       
        #sensor2 = max
        elif sensor2_total >= sensor0_total and sensor2_total >= sensor1_total:
            if sensor2_direction > 0:
                feature_vector.add_data(1)
            else:
                feature_vector.add_data(-1) 

        #Vector[9] = 1 if large range of motion, -1 otherwise
        #Distinguish between horizontal swipes vs circles
        if (max_seen - min_seen) < 8:
            feature_vector.add_data(-1)
        else:
            feature_vector.add_data(1)

        print feature_vector.get_data()
        print "ADJUSTING FEATURE: " + str(feature_vector.get_data()[5])

        #Calculate weights
        current_max = float("-inf")
        index_max = 0
        index = 0
        for weight in Classifier.all_weights:
            dot_product = weight.dot_product(feature_vector)
            print "DOT PRODUCT " + str(index) + ": " + str(dot_product)
            if dot_product > current_max:
                current_max = dot_product
                index_max = index
            index += 1 

        gesture = Classifier.all_weights[index_max].gesture
        if (abs(current_max) < GESTURE_THRESHOLD):
            return UNKNOWN, feature_vector
        return gesture, feature_vector

    def sensor_difference(self, array1, array2, which_sensor):
        total = 0;
        diff = abs(array1[which_sensor] - array2[which_sensor])
        if array2[which_sensor] != 0:
            return diff
        else:
            # if which_sensor == 1:
            #     if array2[2] != 0:
            #         diff = abs(array1[which_sensor] - array2[2])
            #     else:
            #         diff = -1
            # elif which_sensor == 2:
            #     if array2[1] != 0:
            #         diff = abs(array1[which_sensor] - array2[1])
            #     elif array2[3] != 0 and array1[1] == 0: #array1 = middle sensor only
            #         diff = abs(array1[which_sensor] - array2[3])
            #     else:
            #         diff = -1
            # elif which_sensor == 3:
            #     if array2[2] != 0:
            #         diff = abs(array1[which_sensor] - array2[2])
            #     else:
            #         diff = -1
            # else:
            #     diff = -1
            return -1
