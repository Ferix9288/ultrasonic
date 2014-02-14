from configandsetup import *

class Classifier:

    which_sensor = 0

    def __init__(self, all_weights, feature_calculator):
        self.gesture = UNKNOWN
        self.feature_calculator = feature_calculator
        self.all_weights = all_weights
       
    def add_weight(self, weight_array, type_gesture):
        new_weight = Vector(weight_array, type_gesture)
        all_weights.append(new_weight)

    def classify(self, feature_vector):
        if not(feature_vector):
            return UNKNOWN
        #Calculate weights
        current_max = float("-inf")
        index_max = 0
        index = 0
        for weight in self.all_weights:
            dot_product = weight.dot_product(feature_vector)
            print "DOT PRODUCT " + str(index) + ": " + str(dot_product)
            if dot_product > current_max:
                current_max = dot_product
                index_max = index
            index += 1 
        gesture = self.all_weights[index_max].gesture
        return gesture
    
    def classifying_data(self, array):
        print array
        fv = self.feature_calculator.calculate_features(array)
        self.gesture = self.classify(fv)
        self.print_weights()
        return self.gesture

    def learning(self, array, right_answer):
        print array
        
        fv = self.feature_calculator.calculate_features(array)
        self.gesture = self.classify(fv)

        if self.gesture != right_answer and self.gesture != UNKNOWN:
            self.update_weights(self.gesture, right_answer, fv)
            #print fv
            print "UPDATED WEIGHTS:" + gestureToText(right_answer)
            print "GUESSED: " + gestureToText(self.gesture)
        print "Length of processed: " + str(len(array)) 
        self.print_weights()

    def print_weights(self):
        update_file = open('updateWeights.txt', 'w')
        for w in self.all_weights:
            print w.data
            update_file.write(str(w.data) + "\n")
        update_file.close()

    #Note: certain features may be nullified with FEATURE_ON where their values = 0
    def update_weights(self, wrong_gesture, right_gesture, feature_vector):
        wrong_weights = self.all_weights[wrong_gesture]
        right_weights = self.all_weights[right_gesture]

        for i in range(0, len(wrong_weights.data)):
            if feature_vector.data[i] > 0:
                wrong_weights.data[i] -= feature_vector.data[i]
            else:
                wrong_weights.data[i] += abs(feature_vector.data[i])
            
        for i in range(0, len(right_weights.data)):
            if feature_vector.data[i] > 0:
                right_weights.data[i] += feature_vector.data[i]
            else:
                right_weights.data[i] -= abs(feature_vector.data[i])
        
   
    

