// пины платформы
#define PIN_MOT1_PLUS A0
#define PIN_MOT1_MINUS A1
#define PIN_MOT2_PLUS A3
#define PIN_MOT2_MINUS A2
#define PIN_MOT3_PLUS A4
#define PIN_MOT3_MINUS A5
#define PIN_MOT4_PLUS 13
#define PIN_MOT4_MINUS 12

#define PIN_MOT1_SPEED 150
#define PIN_MOT2_SPEED 150
#define PIN_MOT3_SPEED 150
#define PIN_MOT4_SPEED 150

#define MOT1_SPEED 150
#define MOT2_SPEED 150
#define MOT3_SPEED 150
#define MOT4_SPEED 150

class yellowMotor {
  protected:
  int pinPlus;
  int pinMinus;
  int movementSpeed;

  int pinSpeed;

  public:
  void attach(int plus, int minus, int msp, int mspin) {
    pinPlus = plus;
    pinMinus = minus; 
    movementSpeed = msp;
    pinSpeed = mspin;
  }

  void writeSpeed(int msp) {
    analogWrite(pinSpeed, msp);
  }

  void moveForward() {
    this->writeSpeed(movementSpeed);
    digitalWrite(pinPlus, HIGH);
    digitalWrite(pinMinus, LOW);
  }

  void moveBackward() {
    this->writeSpeed(movementSpeed);
    digitalWrite(pinPlus, LOW);
    digitalWrite(pinMinus, HIGH);
  }

  void Stop() {
    digitalWrite(pinPlus, LOW);
    digitalWrite(pinMinus, LOW);
  }
};

// моторы движения платформы
yellowMotor motor1;
yellowMotor motor2;
yellowMotor motor3;
yellowMotor motor4;

void executeCommand(String cmd, int arg) {
  if (cmd == "getPlate") {
    Serial.println("wheels");
  }
  else if (cmd == "moveForward") {
    motor1.moveForward();
    motor2.moveForward();
    motor3.moveForward();
    motor4.moveForward();
    delay(arg);
  }
  else if (cmd == "moveBackward") {
    motor1.moveBackward();
    motor2.moveBackward();
    motor3.moveBackward();
    motor4.moveBackward();
    delay(arg);
  }
  motor1.Stop();
  motor2.Stop();
  motor3.Stop();
  motor4.Stop();
}

void setup() {
  pinMode(PIN_MOT1_PLUS, OUTPUT);
  pinMode(PIN_MOT1_MINUS, OUTPUT);
  pinMode(PIN_MOT2_PLUS, OUTPUT);
  pinMode(PIN_MOT2_MINUS, OUTPUT);
  pinMode(PIN_MOT3_PLUS, OUTPUT);
  pinMode(PIN_MOT3_MINUS, OUTPUT);
  pinMode(PIN_MOT4_PLUS, OUTPUT);
  pinMode(PIN_MOT4_MINUS, OUTPUT);

  motor1.attach(PIN_MOT1_PLUS, PIN_MOT1_MINUS, MOT1_SPEED, PIN_MOT1_SPEED);
  motor2.attach(PIN_MOT2_PLUS, PIN_MOT2_MINUS, MOT2_SPEED, PIN_MOT2_SPEED);
  motor3.attach(PIN_MOT3_PLUS, PIN_MOT3_MINUS, MOT3_SPEED, PIN_MOT3_SPEED);
  motor4.attach(PIN_MOT4_PLUS, PIN_MOT4_MINUS, MOT4_SPEED, PIN_MOT4_SPEED);
}

void loop() {
  if (Serial.available()) {
    msg = Serial.readStringUntil('\n');
    index = msg.indexOf(sep);
    command = msg.substring(0, index);
    msg.remove(0, index+1);
    argument = msg.toInt();

    Serial.println(command + msg);

    executeCommand(command, argument);
  }
  
  delay(10);
}
