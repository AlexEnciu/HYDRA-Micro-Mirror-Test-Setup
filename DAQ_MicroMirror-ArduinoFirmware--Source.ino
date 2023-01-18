#include <Stepper.h>
int led=10;
const int stepsPerRevolution = 80*8;  //steps per revolution (20 steps * 8 microsteps)
float distPerRevolution=3; // distance of the carrige when the motor is spining one revolution
int homing_speed=150;
const int homeSwitchPin = 11;
int currentPosition = 0;
int diff=0;
Stepper myStepper(stepsPerRevolution, 13, 12);


void setup() {
  Serial.begin(9600);
  pinMode(homeSwitchPin, INPUT_PULLUP);
  pinMode(led,OUTPUT);
  digitalWrite(led,HIGH);
  myStepper.setSpeed(homing_speed);// default speed
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    switch (command) {
      case 'H': // Homing command example "H"
        home();
        break;
      case 'S': // Set speed command example "S 1000" 
        setSpeed();
        break;
      case 'M': // Move command example "M 1000 or M -1000"
        move();
        break;
      case 'L': // LedStatus
        ledstat();  
        break;
    }
  }
}

void home() {
  myStepper.setSpeed(homing_speed);
  while (digitalRead(homeSwitchPin) == LOW) {
    myStepper.step(-1);
    currentPosition--;
  }
  setCurrentPosition(0);
  Serial.println("Homing Done!");
}

void setSpeed() {
  int speed = Serial.parseInt();
  myStepper.setSpeed(speed);
  Serial.print("Current speed = ");
  Serial.println(speed);
}

void ledstat() {
  int stat = Serial.parseInt();
  if (stat==0){digitalWrite(led,HIGH); Serial.println("Laser On");}
  else if (stat==1) {digitalWrite(led,LOW); Serial.println("Laser Off");}
}

void move() {
  int steps = Serial.parseFloat()*stepsPerRevolution/distPerRevolution;
  if (steps>currentPosition){diff=steps-currentPosition;}
  else if(steps<currentPosition){diff=(currentPosition-steps)*(-1);}
  else if(steps=currentPosition){diff=0;}
  myStepper.step(diff); //myStepper.step(steps);
  currentPosition = steps; //currentPosition += steps;
  Serial.println(steps);
}

void setCurrentPosition(int position) {
  currentPosition = position;
}
