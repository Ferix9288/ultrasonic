from classifier import *

class FeatureCalculator:

    def __init__(self, features_on):
        #Placeholder
        self.feature_on = features_on

    #Vector[0] = starting location? -1 = left, 1 = right
    def starting_leftright(self, feature_vector, state_first):
        self.which_sensor = 1
        if (state_first == RIGHT_DOWN or state_first == RIGHT_MIDDLE or state_first == RIGHT_UP):
            feature_vector.add_data(1)
            self.which_sensor = 3 #Right sensor
        elif state_first == MIDDLE_DOWN or state_first == NEUTRAL or state_first == MIDDLE_UP:
            feature_vector.add_data(0)
            self.which_sensor = 2 #Middle sensor
        else:
            feature_vector.add_data(-1)
            self.which_sensor = 1 #Left Sensor

    #Vector[1] = end location? -1 = left, 0 = neutral, 1 =  right
    def end_leftright(self, feature_vector, state_last):
        if (state_last == RIGHT_DOWN or state_last == RIGHT_MIDDLE or state_last == RIGHT_UP):
            feature_vector.add_data(1)
        elif state_last == MIDDLE_DOWN or state_last == NEUTRAL or state_last == MIDDLE_UP:
            feature_vector.add_data(0)
        else:
            feature_vector.add_data(-1)

    #Vector[2] = starting location? -1 = bottom, 1 = top
    def starting_downup(self, feature_vector, state_first):
        if (state_first == LEFT_DOWN or state_first == MIDDLE_DOWN or state_first == RIGHT_DOWN):
            feature_vector.add_data(-1)
        elif state_first == LEFT_MIDDLE or state_first == NEUTRAL or state_first == RIGHT_MIDDLE:
            feature_vector.add_data(0) 
        else:
            feature_vector.add_data(1)

    #Vector[3] = end location? -1 = left, 0 = neutral, 1 =  right
    def end_downup(self, feature_vector, state_last):
        if (state_last == LEFT_DOWN or state_last == MIDDLE_DOWN or state_last == RIGHT_DOWN):
            feature_vector.add_data(-1)
        elif state_last == LEFT_MIDDLE or state_last == NEUTRAL or state_last == RIGHT_MIDDLE:
                feature_vector.add_data(0) 
        else:
            feature_vector.add_data(1)
        
    #Vector[4] = Does gesture loop back on itself? (Based on states)   
    def cycle(self, feature_vector, state_first, state_last):
        if (state_first == state_last):
            feature_vector.add_data(1)
        else:
            feature_vector.add_data(0)
    
    #Vector[5] = Same as above but calculated based on sensor values
    #Difference only based on one sensor
    def cycle_2(self, feature_vector, array1, array2):
        total = 0;
        diff = abs(array1[self.which_sensor] - array2[self.which_sensor])
        if array2[self.which_sensor] == 0:
            diff = -1
        if diff  == -1:
            feature_vector.add_data(0)
        elif diff < 9:
            feature_vector.add_data(1)   
        else:
            feature_vector.add_data(0)

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

    #Before averaging and dividing the values (don't want to deal with floats)
    #Vector[6] = Does gesture loop hit all sensors? (Based on values)
    def all_sensors(self, feature_vector, sensor0_total, sensor1_total, sensor2_total):
        if (sensor0_total != 0 and sensor1_total != 0 and sensor2_total != 0):
            feature_vector.add_data(1)
        else:
            feature_vector.add_data(0)


    #Vector[7] = What's the overall directions of each sensor? 
    #If sum of directions fall within abs 3, then must likely circle/horizontal swipes
    def total_direction(self, feature_vector, sum_directions):
        if (abs(sum_directions) <= 3):
            feature_vector.add_data(0)
        else:
            feature_vector.add_data(1)
            

    #Vector[8] = overall direction of sensor with max value?
    #Positive direction most likely indicate upward swipe
    #Negative Direction most likely indicate downward swipe
    def max_sensor_direction(self,feature_vector, direction):
        if direction > 0:
            feature_vector.add_data(1)
        else:
            feature_vector.add_data(-1)

    #Vector[9] = 1 if large range of motion, -1 otherwise
    #Distinguish between horizontal swipes vs circles
    def range(self, feature_vector, max_seen, min_seen):
        if (max_seen - min_seen) <= RANGE_THRESHOLD:
            feature_vector.add_data(-1)
        else:
            feature_vector.add_data(1)

    #Vector[10] = See how close the start and end are in terms of vertical range
    def mirrored(self, feature_vector, start, end):
        if feature_vector.data[0] != feature_vector.data[1]:
            max_start = max(start[1:])
            max_end = max(end[1:])
            diff = abs(max_start - max_end)
            if diff <= RANGE_THRESHOLD:
                feature_vector.add_data(-1)
            else:
                feature_vector.add_data(1)
        else:
            feature_vector.add_data(0)

    #Vector[11] = if start/end at same side, calculate difference in sensor value
    def risingorfalling(self, feature_vector, start, end):
        if feature_vector.data[0] == feature_vector.data[1]:
            max_start = max(start[1:])
            max_end = max(end[1:])
            diff = max_start - max_end
            if diff > 0:
                feature_vector.add_data(-1) # falling
            elif diff < 0:
                feature_vector.add_data(1) #rising
            else:
                feature_vector.add_data(0)     
        else:
            feature_vector.add_data(0)   

    #Vector[12] = look at overall direction in first half
    #Vector[13] = look at overall direction in second half
    def directions(self, feature_vector, directions):
        if (directions > DIRECTION_THRESHOLD):
            feature_vector.add_data(1)
        elif (directions < -DIRECTION_THRESHOLD):
            feature_vector.add_data(-1)
        else:
            feature_vector.add_data(0)

    #Vector[14] = Flunctuation of states. Less = swipes 
    def fluctuations(self, feature_vector, fluctunate_states):
        if (fluctunate_states > FLUCTUATION):
            feature_vector.add_data(1)
        else:
            feature_vector.add_data(0)

    #Vector[15] = See positioning of middle. Helps with caret vs V 
    def where_middle(self, feature_vector, middle):
        if middle[2] != 0:
            if middle[2] < MIDDLE_CUTOFF:
                feature_vector.add_data(1)
            else:
                feature_vector.add_data(0)
        else:
            feature_vector.add_data(0)


    def calculate_features(self, array):
        feature_vector = Vector([], UNKNOWN);
        gesture = UNKNOWN
        if (len(array) < 3):
            return None

        # #Last Data is always the noisest because user has to take hand away. Filter it out.
        # array = array[0:len(array)-1]
        # print "Filtered Array: " + str(array)

        first = array[0] 
        last = array[len(array)-1]

        state_first = first[0]
        state_last = last[0]

        #Vector[0] feature - start location = left, middle, or right?
        self.starting_leftright(feature_vector, state_first)
        #Vector[1] = end location? -1 = left, 0 = neutral, 1 =  right
        self.end_leftright(feature_vector, state_last)
        #Vector[2] = starting location? -1 = bottom, 1 = top
        self.starting_downup(feature_vector, state_first)
        #Vector[3] = end location? -1 = left, 0 = neutral, 1 =  right
        self.end_downup(feature_vector, state_last)
    
        #Vector[4] = Does gesture loop back on itself? (Based on states)
        self.cycle(feature_vector, state_first, state_last)

        #Vector[5] = Same as above but calculated based on sensor values
        #Difference only based on one sensor
        self.cycle_2(feature_vector, first, last)
     
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

        compensate_max_noise = 0
        compensate_min_noise = 0

        set_first_max = False
        set_first_min = False

        first_half = True
        first_half_directions = 0
        second_half_directions = 0
        previous = max(first[1:])
        #print previous
        for i in range(1, len(array)):
            sensor0_total += array[i][1]
            sensor1_total += array[i][2]
            sensor2_total += array[i][3]

            if first_half:
                if i == len(array)/2:
                    middle = array[i]
                    first_half = False
                value = max(array[i][1:])
                if value > (previous + STEP):
                    first_half_directions += 1
                elif value < (previous - STEP):
                    first_half_directions -= 1
                previous = value
            else:
                value = max(array[i][1:])
                if value > (previous + STEP):
                    second_half_directions += 1
                elif value < (previous - STEP):
                    second_half_directions -= 1     
                previous = value
               



            if (array[i][0]) != previous_state:
                fluctunate_states += 1
            previous_state = array[i][0]

            if (array[i][1] != 0):
                if array[i][1] > max_seen:
                    if (not set_first_max):
                        max_seen = array[i][1]
                        set_first_max = True 
                    elif compensate_max_noise > NOISE_MAX_THRESHOLD:
                        max_seen = array[i][1]
                    else:
                        compensate_max_noise += 1

                if array[i][1] < min_seen:
                    if (not set_first_min):                        
                       min_seen = array[i][1]  
                       set_first_min = True   
                    elif compensate_min_noise > NOISE_MIN_THRESHOLD:
                        min_seen = array[i][1]
                    else:
                        compensate_min_noise += 1

                if (array[i][1] > previous_sensor0):
                    sensor0_direction += 1
                elif (array[i][1] < previous_sensor0):
                    sensor0_direction -= 1
                previous_sensor0 = array[i][1]

            else:
                actual_sensor0 -= 1

            if (array[i][2] != 0):

                if array[i][2] > max_seen:
                    if (not set_first_max):
                        max_seen = array[i][2]
                        set_first_max = True 
                    elif compensate_max_noise > NOISE_MAX_THRESHOLD:
                        max_seen = array[i][2]
                    else:
                        compensate_max_noise += 1

                if array[i][2] < min_seen:
                    if (not set_first_min):                        
                       min_seen = array[i][2]  
                       set_first_min = True   
                    elif compensate_min_noise > NOISE_MIN_THRESHOLD:
                        min_seen = array[i][2]
                    else:
                        compensate_min_noise += 1

       
                if (array[i][2] > previous_sensor1):
                    sensor1_direction += 1
                elif (array[i][2] < previous_sensor1):
                    sensor1_direction -= 1

                previous_sensor1 = array[i][2]
            else:
                actual_sensor1 -= 1

        
            if (array[i][3]!=0):                        
        
                if array[i][3] > max_seen:
                    if (not set_first_max):
                        max_seen = array[i][3]
                        set_first_max = True 
                    elif compensate_max_noise > NOISE_MAX_THRESHOLD:
                        max_seen = array[i][3]
                    else:
                        compensate_max_noise += 1

                if array[i][3] < min_seen:
                    if (not set_first_min):                        
                       min_seen = array[i][3]  
                       set_first_min = True   
                    elif compensate_min_noise > NOISE_MIN_THRESHOLD:
                        min_seen = array[i][3]
                    else:
                        compensate_min_noise += 1

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
        print "middle: " + str(middle)

        #Before averaging and dividing the values (don't want to deal with floats)
        #Vector[6] = Does gesture loop hit all sensors? (Based on values)
        self.all_sensors(feature_vector, sensor0_total, sensor1_total, sensor2_total)

        sensor0_avg = sensor0_total / actual_sensor0
        sensor1_avg = sensor1_total / actual_sensor1
        sensor2_avg = sensor2_total / actual_sensor2

        print "sensor0_avg: " + str(sensor0_avg)
        print "sensor1_avg: " + str(sensor1_avg)
        print "sensor2_avg: " + str(sensor2_avg)

        print "sensor0_dir: " + str(sensor0_direction)
        print "sensor1_dir: " + str(sensor1_direction)
        print "sensor2_dir: " + str(sensor2_direction)

        print "first half directions: " + str(first_half_directions)
        print "second half directions: " + str(second_half_directions)


        #Vector[7] = What's the overall directions of each sensor? 
        #If sum of directions fall within abs 3, then must likely circle/horizontal swipes
        sum_directions = sensor0_direction + sensor1_direction + sensor2_direction
        self.total_direction(feature_vector, sum_directions)

        #Vector[8] = overall direction of sensor with max value?
        #Positive direction most likely indicate upward swipe
        #Negative Direction most likely indicate downward swipe
        #sensor0 = max
        find_max = []
        find_max.append(sensor0_total)
        find_max.append(sensor1_total)
        find_max.append(sensor2_total)

        max_total = max(find_max)
        find_sensor = find_max.index(max_total)
        if find_sensor == 0:
            self.max_sensor_direction(feature_vector, sensor0_direction)
        elif find_sensor == 1:
            self.max_sensor_direction(feature_vector, sensor1_direction)
        else:
            self.max_sensor_direction(feature_vector, sensor2_direction)
       
        #Vector[9] = 1 if large range of motion, -1 otherwise
        #Distinguish between horizontal swipes vs circles
        self.range(feature_vector, max_seen, min_seen)

        #Vector[10] = See how close the start and end are in terms of vertical range
        #if start/end is on different sides
        self.mirrored(feature_vector, first, last)

        #Vector[11] = if start/end at same side, calculate difference in sensor value
        self.risingorfalling(feature_vector, first, last)

        #Vector[12/13] = look at overall direction in first half/second half
        self.directions(feature_vector, first_half_directions)
        self.directions(feature_vector, second_half_directions)

        #Vector[14] = Flunctuation of states. Less = swipes 
        self.fluctuations(feature_vector, fluctunate_states)

        #Vector[15] = See positioning of middle. Helps with caret vs V 
        self.where_middle(feature_vector, middle)


        #Nullify features based on FEATURE_ON 
        index = 0
        for number in FEATURE_ON:
            if number == 0:
                feature_vector.data[index] = 0
            index += 1

        print feature_vector.get_data()
        print "ADJUSTING FEATURE: " + str(feature_vector.get_data()[5])

 
        return feature_vector