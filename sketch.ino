// Simple Robot Arduino Sketch
// This robot moves forward, turns left, turns right, and stops in a loop

// Define pin numbers for motor control
const int leftMotorForward = 8;
const int leftMotorBackward = 9;
const int rightMotorForward = 10;
const int rightMotorBackward = 11;

void setup() {
  // Initialize motor control pins as outputs
  pinMode(leftMotorForward, OUTPUT);
  pinMode(leftMotorBackward, OUTPUT);
  pinMode(rightMotorForward, OUTPUT);
  pinMode(rightMotorBackward, OUTPUT);
  
  // Ensure all motors are stopped at startup
  stopRobot();
  
  // Print message to serial monitor
  Serial.begin(9600);
  Serial.println("Simple Robot Ready");
}

void loop() {
  // Move forward for 2 seconds
  moveForward();
  delay(2000);
  
  // Stop for 1 second
  stopRobot();
  delay(1000);
  
  // Turn left for 1 second
  turnLeft();
  delay(1000);
  
  // Stop for 1 second
  stopRobot();
  delay(1000);
  
  // Turn right for 1 second
  turnRight();
  delay(1000);
  
  // Stop for 1 second
  stopRobot();
  delay(1000);
}

// Function to move robot forward
void moveForward() {
  digitalWrite(leftMotorForward, HIGH);
  digitalWrite(leftMotorBackward, LOW);
  digitalWrite(rightMotorForward, HIGH);
  digitalWrite(rightMotorBackward, LOW);
  Serial.println("Moving Forward");
}

// Function to turn robot left
void turnLeft() {
  digitalWrite(leftMotorForward, LOW);
  digitalWrite(leftMotorBackward, HIGH);
  digitalWrite(rightMotorForward, HIGH);
  digitalWrite(rightMotorBackward, LOW);
  Serial.println("Turning Left");
}

// Function to turn robot right
void turnRight() {
  digitalWrite(leftMotorForward, HIGH);
  digitalWrite(leftMotorBackward, LOW);
  digitalWrite(rightMotorForward, LOW);
  digitalWrite(rightMotorBackward, HIGH);
  Serial.println("Turning Right");
}

// Function to stop all motors
void stopRobot() {
  digitalWrite(leftMotorForward, LOW);
  digitalWrite(leftMotorBackward, LOW);
  digitalWrite(rightMotorForward, LOW);
  digitalWrite(rightMotorBackward, LOW);
  Serial.println("Stopped");
}