// ---------------------------------------------------------------------------
// Example NewPing library sketch that does a ping about 20 times per second.
// ---------------------------------------------------------------------------

#include <NewPing.h>

#define BUTTON_SWITCH 6
#define LED_PIN 7

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
#define PING_INTERVAL 10 //keep track of timing difference among pings of different sensors
#define DELAY 0

#define UP_THRESHOLD 12 //13 cm and above = up
#define DOWN_THRESHOLD 6 //8 cm and below = down
#define MOVEMENT_THRESHOLD 2
#define RESILIENCY 1

#define GESTURE_COUNT 50
#define GESTURE_TIME 1500

//FOR STATE VARIABLE
#define OUTSIDE  0
#define LEFT_DOWN 1
#define MIDDLE_DOWN 2
#define RIGHT_DOWN 3
#define LEFT_MIDDLE 4
#define NEUTRAL 5
#define RIGHT_MIDDLE 6
#define LEFT_UP 7
#define MIDDLE_UP 8
#define RIGHT_UP 9
#define SPAN_ALL 10
#define SWIPE_RIGHT 11
#define SWIPE_LEFT 12
#define GESTURE 13

//FOR MODE VARIABLE
#define MOUSE_MODE 0
#define GAMING_MODE 1

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

unsigned int mode = GAMING_MODE; //0 = mouse navigation/clicking; 1 = for gaming/gesture recognition heavy

unsigned int state = 0; //identifies what information to send based on state
unsigned int current_state = 0;
unsigned int previous_state = 0;
unsigned int resiliency_counter = 0; //only send character if state has been consistent for some time. Avoids noise

boolean click_once = true;
unsigned int last_clicked = 0;
unsigned int last_time = 0;
unsigned int last_mode = 0;

int gesture_array[GESTURE_COUNT];
int sensor0_array[GESTURE_COUNT];
int sensor1_array[GESTURE_COUNT];
int sensor2_array[GESTURE_COUNT];

int gesture_counter = 0;
boolean sweep_leftright = false;
boolean sweep_rightleft = false;
boolean gestureCheck = false;

int led_state = LOW;
boolean pressed = false;

void setup() {
  Serial.begin(9600); // Open serial monitor at 9600 baud to see ping results.
  pinMode(BUTTON_SWITCH, INPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  pingTimer[0] = millis() + 75;
  for (uint8_t i = 1; i < SONAR_NUM; i++) {
    pingTimer[i] = pingTimer[i-1] + PING_INTERVAL + DELAY;  
  }

}

void loop() {
  int button = digitalRead(BUTTON_SWITCH);
  //Serial.println(button);
  if (button == 0 && !(pressed) && millis() > 200) {
    pressed = true;
    last_mode = millis();
    changeLED();  
    changeMODE();
  } else if (button == 1) {
    pressed = false;
  }
  
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

void changeLED() {
  led_state = !led_state;
  digitalWrite(LED_PIN, led_state);
}

void changeMODE() {
  if (mode == MOUSE_MODE) { 
    mode = GAMING_MODE;
  } else {
    mode = MOUSE_MODE;
  }  
}
void fullCycle() {
  
  //report_cycle();
//  
  decipherSensor(); //deciphers the readings of the sensors and writes corresponding message to python script via serial
  //Serial.println("State:" + String(state));

  gestureRecognition();
  resiliency();
  communicate();
  check_mode();
 // Serial.println("State:" + String(state));
 // Serial.println("Current State:" + String(current_state));
 // Serial.println("Mode:" + String(mode));
 //Serial.println();
  store_previous();
}

void decipherSensor() {
  //if ( cm[1] != 0) {
 
 if ( mode == MOUSE_MODE && ((current_state == NEUTRAL && cm[0] !=0 && cm[1] != 0 && cm[2] != 0) ||
       (current_state == SPAN_ALL && cm[0] !=0 && cm[1] != 0 && cm[2] != 0) )){
   state = SPAN_ALL;   
 }  else if ( (cm[1] != 0)) {
     sensor1_detected = true; 
     //if ( cm[1] > UP_THRESHOLD) {
     if ( cm[1] > UP_THRESHOLD && !(cm[1] < previous_cm[1] - MOVEMENT_THRESHOLD) ) {  
       state = MIDDLE_UP;
     } else if ( cm[1] < DOWN_THRESHOLD && !(cm[1]  > previous_cm[1] + MOVEMENT_THRESHOLD) ) { 
       state = MIDDLE_DOWN;
     } else {
       state = NEUTRAL;  
     }
 } else if ( (cm[0] == 0) && (cm[2] != 0) ) { //go right
     
    sensor2_detected = true;
    //if ( cm[1] > UP_THRESHOLD) {
    if ( cm[2] > UP_THRESHOLD && !(cm[2] < previous_cm[2] - MOVEMENT_THRESHOLD) ) {  
      state = RIGHT_UP;
    } else if ( cm[2] < DOWN_THRESHOLD && !(cm[2]  > previous_cm[2] + MOVEMENT_THRESHOLD) ) { 
       state = RIGHT_DOWN;
    } else {
       state = RIGHT_MIDDLE;  
     }       
     
     if (!(sensor0_detected) && !(sensor1_detected)) {
       sweep_rightleft = true;
     }
   
 } else if ( (cm[0] != 0) && (cm[2] == 0) ) { //go left
    sensor0_detected = true;
     if ( cm[0] > UP_THRESHOLD && !(cm[0] < previous_cm[0] - MOVEMENT_THRESHOLD) ) {  
       state = LEFT_UP;
     } else if ( cm[0] < DOWN_THRESHOLD && !(cm[0]  > previous_cm[0] + MOVEMENT_THRESHOLD) ) { 
       state = LEFT_DOWN;
     } else {
       state = LEFT_MIDDLE;  
     }     
     
     if (!(sensor1_detected) && !(sensor2_detected)) {
       sweep_leftright = true;
     }
   

 } else {
   state = OUTSIDE;   
 }
}


void gestureRecognition() {
   
  if (!gestureCheck) {
    if (sensor0_detected || sensor1_detected || sensor2_detected) {
      gestureCheck = true;
      last_time = millis();
      if (state != OUTSIDE && mode == GAMING_MODE && gesture_counter < GESTURE_COUNT) {
        gesture_array[gesture_counter] = state;  
        sensor0_array[gesture_counter] = cm[0];
        sensor1_array[gesture_counter] = cm[1];
        sensor2_array[gesture_counter] = cm[2];
        gesture_counter++;
      }
    }
  } else {
    int difference_time = millis() - last_time;
    
    //Track all hand movements above sensor. Ignore if outside range
    if (state != OUTSIDE && mode == GAMING_MODE && gesture_counter < GESTURE_COUNT) {
      gesture_array[gesture_counter] = state;  
      sensor0_array[gesture_counter] = cm[0];
      sensor1_array[gesture_counter] = cm[1];
      sensor2_array[gesture_counter] = cm[2];
      gesture_counter++;
    }
    
    //if (difference_time > GESTURE_TIME) { //check after every second
    if (state == OUTSIDE) {    
      //Serial.println("Checking gesture...");
       if (mode == GAMING_MODE) {
          state = GESTURE;
       } else {
        if (sensor0_detected && sensor1_detected && sensor2_detected) {
          if (sweep_leftright) {
            state = SWIPE_RIGHT;
            //Serial.println("Swept Left...");   
          } else if (sweep_rightleft) {
            state = SWIPE_LEFT;
            //Serial.println("Swept Right...");     
          }
        }
        
      }
      
      sensor0_detected = false; 
      sensor1_detected = false; 
      sensor2_detected = false;
      sweep_leftright = false;
      sweep_rightleft = false;
      
      gestureCheck = false;   
    }
  } 
    
}

void resiliency() {
   if (state == previous_state) {
      resiliency_counter ++;
  } else {
    resiliency_counter = 0;  
  }
  
  if (resiliency_counter > RESILIENCY || state == SPAN_ALL || state == GESTURE ||
          state == SWIPE_RIGHT || state == SWIPE_LEFT || state == NEUTRAL || state == OUTSIDE) {
        current_state = state;       
  }
}


void printGestureArray() {
  for (int i = 0; i < gesture_counter; i++) {
    Serial.print(F("Gesture Array: "));
    Serial.println(gesture_array[i]);
   
  } 
}

/*
~THE STATES~
#define OUTSIDE  0
#define LEFT_DOWN 1
#define MIDDLE_DOWN 2
#define RIGHT_DOWN 3
#define LEFT_MIDDLE 4
#define NEUTRAL 5
#define RIGHT_MIDDLE 6
#define LEFT_UP 7
#define MIDDLE_UP 8
#define RIGHT_UP 9
#define SPAN_ALL 10
#define SWIPE_RIGHT 11
#define SWIPE_LEFT 12
*/

void communicate() {
  
  if (mode == MOUSE_MODE) {
    switch(current_state) {
      case OUTSIDE:
        break;
      case LEFT_DOWN: 
        Serial.write('l'); //go down left
        break;
      case MIDDLE_DOWN: 
        Serial.write('a'); //go down
        break;
      case RIGHT_DOWN: 
        Serial.write('r'); //go down right
        break;   
      case LEFT_MIDDLE: 
        Serial.write('c'); //go left
        break;      
      case NEUTRAL:
        break;   
     case RIGHT_MIDDLE: 
        Serial.write('b'); //go right
        break;      
      case LEFT_UP:
        Serial.write('L'); //go up left
        break;
      case MIDDLE_UP:
        Serial.write('A'); //go up
        break;  
      case RIGHT_UP: 
        Serial.write('R'); //go up right
        break;
      case SPAN_ALL:
        if (!(click_once)) {
          last_clicked = millis();
          Serial.write('C');
          click_once = true;
        } 
        break;
      case SWIPE_RIGHT:
        Serial.write('x');
        break;
      case SWIPE_LEFT:
        Serial.write('y');
        break;
      }
  } else {
    
//     if (current_state == SPAN_ALL) {
//        if (!(click_once)) {
//          last_clicked = millis();
//          Serial.write('C');
//          click_once = true;
////          gesture_counter = 0;
////          sensor0_detected = false; 
////          sensor1_detected = false; 
////          sensor2_detected = false;
////          sweep_leftright = false;
////          sweep_rightleft = false;  
////          gestureCheck = false;   
//        } 
//     } else 
     if (current_state == GESTURE) {
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
      gesture_counter = 0;
    } 
  }  
  
}

void check_mode() {
  if (current_state != SPAN_ALL) {
    click_once = false;
  }
//  if (current_state != SPAN_ALL && click_once) {
//      if (millis() - last_clicked > 5000) {
//      changeLED();
//      if (mode == MOUSE_MODE) {
//        mode = GAMING_MODE;
//      }  else {
//        mode = MOUSE_MODE;
//      }
//    }
//    click_once = false;  
//  }  

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
