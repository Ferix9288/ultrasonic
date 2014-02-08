// ---------------------------------------------------------------------------
// Example NewPing library sketch that does a ping about 20 times per second.
// ---------------------------------------------------------------------------

#include <NewPing.h>

//Number of total sensors
#define SONAR_NUM 3

//Pins for first ultrasonic sensor
#define TRIGGER1  13  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO1     12  // Arduino pin tied to echo pin on the ultrasonic sensor.

//Pins for second ultrasonic sensor
#define TRIGGER2  11
#define ECHO2     10

//Pins for third ultrasonic sensor
#define TRIGGER3   9
#define ECHO3      8

#define MAX_DISTANCE 30 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
#define PING_INTERVAL 30 //keep track of timing difference among pings of different sensors
#define DELAY 0

#define UP_THRESHOLD 12 //13 cm and above = up
#define DOWN_THRESHOLD 6 //8 cm and below = down
#define MOVEMENT_THRESHOLD 2
#define RESILIENCY 1

#define GESTURE_COUNT 10

unsigned int counter = 0;
uint8_t currentSensor = 0; //keep track which sensor is active

//Sonar[0] = BOTTOM LEFT
//Sonar[1] = TOP MIDDLE
//Sonar[2] = BOTTOM RIGHT
NewPing sonar[SONAR_NUM] = {
  NewPing (TRIGGER1, ECHO1, MAX_DISTANCE), // NewPing setup of pins and maximum distance.  
  NewPing (TRIGGER2, ECHO2, MAX_DISTANCE), // NewPing setup of pins and maximum distance.
  NewPing (TRIGGER3, ECHO3, MAX_DISTANCE) // NewPing setup of pins and maximum distance.  
};

unsigned long pingTimer[SONAR_NUM]; //holds time for when next ping should happen for designated sensor
unsigned int cm[SONAR_NUM]; // keeps track of the distance finding of said sensor
unsigned int previous_cm[SONAR_NUM];

boolean sensor0_detected = false;
boolean sensor1_detected = false;
boolean sensor2_detected = false;

unsigned int state = 0; //identifies what information to send based on state
unsigned int current_state = 0;
unsigned int previous_state = 0;
unsigned int resiliency_counter = 0; //only send character if state has been consistent for some time. Avoids noise

boolean click_once = true;
unsigned int last_time = 0;

int gesture_array[GESTURE_COUNT];
int sensor0_array[GESTURE_COUNT];
int sensor1_array[GESTURE_COUNT];
int sensor2_array[GESTURE_COUNT];


int gesture_counter = 0;
boolean sweep_leftright = false;
boolean sweep_rightleft = false;
boolean gestureCheck = false;




void setup() {
  Serial.begin(9600); // Open serial monitor at 9600 baud to see ping results.
  pingTimer[0] = millis() + 75;
  for (uint8_t i = 1; i < SONAR_NUM; i++) {
    pingTimer[i] = pingTimer[i-1] + PING_INTERVAL + DELAY;  
  }

}

void loop() {
  for (uint8_t i = 0; i < SONAR_NUM; i++) {
    if (millis() >= pingTimer[i]) {
      pingTimer[i] += (DELAY+PING_INTERVAL) * SONAR_NUM;
      if (i == 0 && currentSensor == SONAR_NUM - 1) fullCycle();
      sonar[currentSensor].timer_stop();
      currentSensor = i;
      cm[currentSensor] = 0;
      sonar[currentSensor].ping_timer(echoCheck);
    
    }  
    
  }
}

void echoCheck() {
  if (sonar[currentSensor].check_timer()) { 
    cm[currentSensor] = sonar[currentSensor].ping_result / US_ROUNDTRIP_CM;
  }  
}
void fullCycle() {
  
  //report_cycle();
//  
  decipherSensor(); //deciphers the readings of the sensors and writes corresponding message to python script via serial
  gestureRecognition();
  resiliency();
  //communicate();
  
  //Serial.println("State:" + String(state));
  //Serial.println("Current State:" + String(current_state));
  //Serial.println();
  store_previous();
}

void decipherSensor() {
  //if ( cm[1] != 0) {
 
 if ( current_state == 0 && cm[0] !=0 && cm[1] != 0 && cm[2] != 0) {
   state = 9;   
 }  else if ( (cm[1] != 0)) {
   
   if (sensor1_detected) {
     //if ( cm[1] > UP_THRESHOLD) {
     if ( cm[1] > UP_THRESHOLD && !(cm[1] < previous_cm[1] - MOVEMENT_THRESHOLD) ) {  
       state = 1;
     } else if ( cm[1] < DOWN_THRESHOLD && !(cm[1]  > previous_cm[1] + MOVEMENT_THRESHOLD) ) { 
       state = 2;
     } else {
       state = 0;  
     }
   } else { 
     sensor1_detected = true;
   }
   
   //sensor0_detected = false;
   //sensor2_detected = false;
   
 
 } else if ( (cm[0] == 0) && (cm[2] != 0) ) { //go right
    if (sensor2_detected) {
         //if ( cm[1] > UP_THRESHOLD) {
       if ( cm[2] > UP_THRESHOLD && !(cm[2] < previous_cm[2] - MOVEMENT_THRESHOLD) ) {  
         state = 5;
       } else if ( cm[2] < DOWN_THRESHOLD && !(cm[2]  > previous_cm[2] + MOVEMENT_THRESHOLD) ) { 
         state = 6;
       } else {
         state = 8;  
       }       
     } else { 
       sensor2_detected = true;
     }
   
   //sensor0_detected = false;
   //sensor1_detected = false;
 
 //   } 
 } else if ( (cm[0] != 0) && (cm[2] == 0) ) { //go left
   if (sensor0_detected) {
        //if ( cm[1] > UP_THRESHOLD) {
     if ( cm[0] > UP_THRESHOLD && !(cm[0] < previous_cm[0] - MOVEMENT_THRESHOLD) ) {  
       state = 3;
     } else if ( cm[0] < DOWN_THRESHOLD && !(cm[0]  > previous_cm[0] + MOVEMENT_THRESHOLD) ) { 
       state = 4;
     } else {
       state = 7;  
     }
   } else { 
     
     sensor0_detected = true;
     if (!(sensor1_detected) && !(sensor2_detected)) {
       sweep_leftright = true;
     }
   }
   
   //sensor1_detected = false;
   //sensor2_detected = false;
 

 } else {
   state = 0;
   //sensor0_detected = false;
   //sensor1_detected = false;
   //sensor2_detected = false;
       
 }
}


void gestureRecognition() {
   
  if (!gestureCheck) {
    if (sensor0_detected || sensor1_detected || sensor2_detected) {
      gestureCheck = true;
      last_time = millis();
    }
  } else {
    int difference_time = millis() - last_time;
    
    if (state != 0) {
      gesture_array[gesture_counter] = state;  
      sensor0_array[gesture_counter] = cm[0];
      sensor1_array[gesture_counter] = cm[1];
      sensor2_array[gesture_counter] = cm[2];
      gesture_counter++;
    }
    
    if (difference_time > 1000) { //check after every second
        
      //Serial.println("Checking gesture...");

       //printGestureArray();
       for (int i = 0; i < gesture_counter; i++) {
       
         Serial.write(gesture_array[i]);
         Serial.write(sensor0_array[i]);
         Serial.write(sensor1_array[i]);
         Serial.write(sensor2_array[i]);    
         
         /*
         Serial.println(gesture_array[i]);
         Serial.println(sensor0_array[i]);
         Serial.println(sensor1_array[i]);
         Serial.println(sensor2_array[i]);    
         */
       }
       
       Serial.write('d');


   
      if (sensor0_detected && sensor1_detected && sensor2_detected) {
        if (sweep_leftright) {
          state = 10;
          //Serial.println("Swept Left...");   
        } else {
          state = 11;
          //Serial.println("Swept Right...");     
        }
        
      }
      
      sensor0_detected = false; 
      sensor1_detected = false; 
      sensor2_detected = false;
      sweep_leftright = false;
      
      gestureCheck = false;   
      gesture_counter = 0;
    }
  } 
    
}

void resiliency() {
   if (state == previous_state) {
      resiliency_counter ++;
  } else {
    resiliency_counter = 0;  
  }
 
  if (resiliency_counter > RESILIENCY || state == 9 || state == 10 || state == 11 || state == 0) {
    current_state = state;      
  }  
}
void printGestureArray() {
  for (int i = 0; i < gesture_counter; i++) {
    Serial.print(F("Gesture Array: "));
    Serial.println(gesture_array[i]);
   
  } 
}

//state 0: send nothing
//state 1: go up
//state 2: go down
//state 3: go up left
//state 4: go down left
//state 5: go up right
//state 6: go down right
//state 7: go left
//state 8: go right
//state 9: click
//state 10: swept left to right
//state 11: swept right to left

void communicate() {
  
  switch(current_state) {
    case 0:
      break;
    case 1:
      Serial.write('A'); //go up
      break;
    case 2: 
      Serial.write('a'); //go down
      break;
    case 3:
      Serial.write('L'); //go up left
      break;
    case 4: 
      Serial.write('l'); //go down left
      break;
    case 5: 
      Serial.write('R'); //go up right
      break;
    case 6: 
      Serial.write('r'); //go down right
      break;
    case 7: 
      Serial.write('c'); //go left
      break;
    case 8: 
      Serial.write('b'); //go right
      break;
    case 9:
    
      if (click_once) {
        Serial.write('C');
        click_once = false;
      } 
      break;
    
    case 10:
      Serial.write('x');
      break;
      
    case 11:
      Serial.write('y');
      break;
  }  
  
  
  
  if (current_state != 9) {
    click_once = true;  
  }  
}

void report_cycle() {
 //if (counter < 100) {
    Serial.print(F("Counter:"));
    Serial.print(counter);
    Serial.println();
    for (uint8_t i = 0; i < SONAR_NUM; i++) {
  // 
  //  //for (uint8_t i = 0; i < SONAR_NUM; i++) {
      Serial.print(i);
      Serial.print("=");
      Serial.print(cm[i]);
      Serial.println("cm ");
    }  
    counter++;
  // } 
}
void store_previous() {
    for (uint8_t i = 0; i < SONAR_NUM; i++) {
  // 
  //  //for (uint8_t i = 0; i < SONAR_NUM; i++) {
      previous_cm[i] = cm[i];    
  }  
    previous_state = state; 
  
}
