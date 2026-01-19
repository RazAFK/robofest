#define SEPARATOR '#'

// пины платформы
// моторы
#define PIN_MOT1_PLUS A0
#define PIN_MOT1_MINUS A1
#define PIN_MOT2_PLUS A3
#define PIN_MOT2_MINUS A2
#define PIN_MOT3_PLUS A4
#define PIN_MOT3_MINUS 12
#define PIN_MOT4_PLUS 13
#define PIN_MOT4_MINUS A5
// пины мощности
#define PIN_MOT1_SPEED 3
#define PIN_MOT2_SPEED 5
#define PIN_MOT3_SPEED 9
#define PIN_MOT4_SPEED 10
// скорости
#define MOT1_SPEED 163
#define MOT2_SPEED 154
#define MOT3_SPEED 135
#define MOT4_SPEED 135

// todo: скорости для поворота

class yellowMotor {
  protected:
  int pinPlus;
  int pinMinus;

  int pinSpeed;

  int motSpeed;

  public:
  void attach(int plus, int minus, int mspin, int mspeed) {
    pinPlus = plus;
    pinMinus = minus;
    pinSpeed = mspin;
    motSpeed = mspeed;
  }

  

  void writeSpeed(int msp) {
    analogWrite(pinSpeed, msp);
  }

  void resetSpeed(int msp) {
    motSpeed = msp;
  }

  int getSpeed() {
    return motSpeed;
  }

  void moveForward() {
    this->writeSpeed(motSpeed);
    digitalWrite(pinPlus, HIGH);
    digitalWrite(pinMinus, LOW);
  }

  void moveBackward() {
    this->writeSpeed(motSpeed);
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

// переменные для сообщений
String msg; // буфер
int index; // индекс разделителя
char sep = SEPARATOR; // разделитель
String command; // команда
String argument; // аргумент(-ы) команды
unsigned long start_time = millis(); // время начала исполнения команды для таймера
unsigned long moving_time = millis(); // время движения
bool move_flag = false;// флаг выполнения команды

void executeCommand(String cmd, String arg) {
  if (cmd == "getPlate") {
      Serial.println("wheels");
  }
  else if (cmd == "moveStop") {
    move_flag = false;
    motor1.Stop();
    motor2.Stop();
    motor3.Stop();
    motor4.Stop();
    Serial.println("moveDone");
    //Serial.println("moveSdone");
  }
  else if (cmd == "changeSpeed") {
    
    // Serial.println(arg);
    int speeds[4];

    int i = 0;
    index = arg.indexOf(sep);
    while(index != -1) {
      speeds[i] = arg.substring(0, index).toInt();
      arg.remove(0, index+1);
      index = arg.indexOf(sep);
      i++;
    }
    speeds[i] = arg.substring(0, index).toInt();

    motor1.resetSpeed(speeds[0]);
    motor2.resetSpeed(speeds[1]);
    motor3.resetSpeed(speeds[2]);
    motor4.resetSpeed(speeds[3]);
    
    // Serial.println(speeds[0]);
    // Serial.println(speeds[1]);
    // Serial.println(speeds[2]);
    Serial.println(speeds[3]);
    Serial.println(motor4.getSpeed());
  }
  else if (cmd == "moveForward") {
    int iarg = arg.toInt();
    move_flag = true;
    start_time = millis();
    moving_time = iarg;
    motor1.moveForward();
    motor2.moveForward();
    motor3.moveForward();
    motor4.moveForward();
    //delay(arg); // tofo: таймер вместо делэя
    
    // Serial.println("moveFdone");
    // Serial.println(iarg);
  }
  else if (cmd == "moveBackward") {
    int iarg = arg.toInt();
    move_flag = true;
    start_time = millis();
    moving_time = iarg;
    motor1.moveBackward();
    motor2.moveBackward();
    motor3.moveBackward();
    motor4.moveBackward();
    //delay(arg);
    // Serial.println("moveBdone");
    // Serial.println(iarg);
  }
  else if (cmd == "rotateRight") {
    int iarg = arg.toInt();
    move_flag = true;
    start_time = millis();
    moving_time = iarg;
    motor1.moveBackward();
    motor2.moveBackward();
    motor3.moveForward();
    motor4.moveForward();
    //delay(arg); // tofo: таймер вместо делэя
    
    // Serial.println("moveFdone");
    // Serial.println(iarg);
  }
  else if (cmd == "rotateLeft") {
    int iarg = arg.toInt();
    move_flag = true;
    start_time = millis();
    moving_time = iarg;
    motor1.moveForward();
    motor2.moveForward();
    motor3.moveBackward();
    motor4.moveBackward();
    //delay(arg); // tofo: таймер вместо делэя
    
    // Serial.println("moveFdone");
    // Serial.println(iarg);
  }
}

void setup() {
  Serial.begin(9600);

  pinMode(PIN_MOT1_SPEED, OUTPUT);
  pinMode(PIN_MOT2_SPEED, OUTPUT);
  pinMode(PIN_MOT3_SPEED, OUTPUT);
  pinMode(PIN_MOT4_SPEED, OUTPUT);

  pinMode(PIN_MOT1_PLUS, OUTPUT);
  pinMode(PIN_MOT1_MINUS, OUTPUT);
  pinMode(PIN_MOT2_PLUS, OUTPUT);
  pinMode(PIN_MOT2_MINUS, OUTPUT);
  pinMode(PIN_MOT3_PLUS, OUTPUT);
  pinMode(PIN_MOT3_MINUS, OUTPUT);
  pinMode(PIN_MOT4_PLUS, OUTPUT);
  pinMode(PIN_MOT4_MINUS, OUTPUT);

  motor1.attach(PIN_MOT1_PLUS, PIN_MOT1_MINUS, PIN_MOT1_SPEED, MOT1_SPEED);
  motor2.attach(PIN_MOT2_PLUS, PIN_MOT2_MINUS, PIN_MOT2_SPEED, MOT2_SPEED);
  motor3.attach(PIN_MOT3_PLUS, PIN_MOT3_MINUS, PIN_MOT3_SPEED, MOT3_SPEED);
  motor4.attach(PIN_MOT4_PLUS, PIN_MOT4_MINUS, PIN_MOT4_SPEED, MOT4_SPEED);
  // везде 1 для подбора
}

void loop() {
  if (Serial.available()) {
    msg = Serial.readStringUntil('\n');
    index = msg.indexOf(sep);
    command = msg.substring(0, index);

    msg.remove(0, index+1);
    argument = msg;//.toInt();

    
    //Serial.println(command + msg);

    
    executeCommand(command, argument);
  }
  
  if (move_flag == true && millis()-start_time >= moving_time){
    move_flag = false;
    executeCommand("moveStop", "0");
  }  

  
  //delay(10);
}
