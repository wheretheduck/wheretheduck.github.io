#include <Servo.h>

Servo rightServo;
Servo leftServo;

const int SERVO_POSITIVE = 1700;
const int SERVO_NEUTRAL = 1500;
const int SERVO_NEGATIVE = 1300;

const int RIGHT_SERVO_ID = 12;
const int LEFT_SERVO_ID = 13;

const int RIGHT_INST_PIN = 13;
const int LEFT_INST_PIN = 12;
const int FORWARD_INST_PIN = 11;
const int STOP_INST_PIN = 10;

const int ALL_DIGITAL_INPUT_PINS[] = {RIGHT_INST_PIN, LEFT_INST_PIN,
FORWARD_INST_PIN, STOP_INST_PIN};

void goRight(){
  leftServo.writeMicroseconds(SERVO_POSITIVE);
  rightServo.writeMicroseconds(SERVO_POSITIVE);
}

void goLeft(){
  leftServo.writeMicroseconds(SERVO_NEGATIVE);
  rightServo.writeMicroseconds(SERVO_NEGATIVE);
}

void goForward(){
  leftServo.writeMicroseconds(SERVO_POSITIVE);
  rightServo.writeMicroseconds(SERVO_NEGATIVE);
}

void goBackward(){
  leftServo.writeMicroseconds(SERVO_NEGATIVE);
  rightServo.writeMicroseconds(SERVO_POSITIVE);
}

void stopAll(){
  leftServo.writeMicroseconds(SERVO_NEUTRAL);
  rightServo.writeMicroseconds(SERVO_NEUTRAL);
}

void setup() {
  // put your setup code here, to run once:
  leftServo.attach(LEFT_SERVO_ID);
  rightServo.attach(RIGHT_SERVO_ID);

  for(int i=0;i<3;i++)
  {
  	pinMode(ALL_DIGITAL_INPUT_PINS[i], INPUT);
  }

}

void loop() {	
 if(digitalRead(FORWARD_INST_PIN)==HIGH)
 {
 	goForward();
 }
 else if(digitalRead(RIGHT_INST_PIN)==HIGH)
 {
 	goRight();
 }
 else if(digitalRead(LEFT_INST_PIN)==HIGH)
 {
 	goLeft();
 }
 else if(digitalRead(STOP_INST_PIN)==HIGH)
 {
 	stopAll();
 }
  
}