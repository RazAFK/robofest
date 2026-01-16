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
#define MOT1_SPEED 170
#define MOT2_SPEED 160
#define MOT3_SPEED 130
#define MOT4_SPEED 130

// todo: скорости для поворота

class yellowMotor {
  protected:
  int pinPlus;
  int pinMinus;

  int pinSpeed;

  public:
  void attach(int plus, int minus, int mspin) {
    pinPlus = plus;
    pinMinus = minus;
    pinSpeed = mspin;
  }

  // int getSpeed() {
  //   return movementSpeed;
  // }

  void writeSpeed(int msp) {
    analogWrite(pinSpeed, msp);
  }

  void moveForward(int msp) {
    this->writeSpeed(msp);
    digitalWrite(pinPlus, HIGH);
    digitalWrite(pinMinus, LOW);
  }

  void moveBackward(int msp) {
    this->writeSpeed(msp);
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
    int speeds[4]

    int i = 1;
    while(index != -1){
      speeds[i] = arg.substring(0, index).toInt();
      arg.remove(0, index+1);
      index = commandStr.indexOf(sep);
      i++;
    }
    motor1.writeSpeed(speeds[0]);
    motor2.writeSpeed(speeds[1]);
    motor3.writeSpeed(speeds[2]);
    motor4.writeSpeed(speeds[3]);
  }
  else if (cmd == "moveForward") {
    int iarg = arg.toInt();
    move_flag = true;
    start_time = millis();
    moving_time = iarg;
    motor1.moveForward(MOT1_SPEED);
    motor2.moveForward(MOT2_SPEED);
    motor3.moveForward(MOT3_SPEED);
    motor4.moveForward(MOT4_SPEED);
    //delay(arg); // tofo: таймер вместо делэя
    //Serial.println("moveFdone");
  }
  else if (cmd == "moveBackward") {
    int iarg = arg.toInt();
    move_flag = true;
    start_time = millis();
    moving_time = iarg;
    motor1.moveBackward(MOT1_SPEED);
    motor2.moveBackward(MOT2_SPEED);
    motor3.moveBackward(MOT3_SPEED);
    motor4.moveBackward(MOT4_SPEED);
    //delay(arg);
    //Serial.println("moveBdone");
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

  motor1.attach(PIN_MOT1_PLUS, PIN_MOT1_MINUS, PIN_MOT1_SPEED);
  motor2.attach(PIN_MOT2_PLUS, PIN_MOT2_MINUS, PIN_MOT2_SPEED);
  motor3.attach(PIN_MOT3_PLUS, PIN_MOT3_MINUS, PIN_MOT3_SPEED);
  motor4.attach(PIN_MOT4_PLUS, PIN_MOT4_MINUS, PIN_MOT4_SPEED);
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
    executeCommand("moveStop", 0);
  }  

  
  //delay(10);
}
