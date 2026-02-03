#include <ServoDriverSmooth.h>
#include <ServoSmooth.h>
#include <Servo.h>

// пины манипулятора
#define PIN_HORSENS A5 // сенсор горизонтального движения
#define PIN_VERSENS A7 // сенсор вертикального движения
#define PIN_HORMOT_PLUS 7
#define PIN_HORMOT_MINUS 8
#define PIN_VERMOT_PLUS 4
#define PIN_VERMOT_MINUS 9
#define PIN_RAILSERVO 6
#define PIN_ROTSERVO 11
#define PIN_GRABSERVO 10

#define SEPARATOR '#'

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

class railMotor : yellowMotor {
  int pinSensor;
  bool isMovingForward = true;

  int curPosition = 0;
  int target = 0;
  bool isOpened;
  bool lastState;

  int delta;

  unsigned long startTime; // начало шага
  
  public: 
  unsigned int getStartTime() {
    return startTime;
  }

  void setStartTime() {
    startTime = millis();
  }
  
  void attach(int plus, int minus, int sensor, int msp, int d, int mspin){
    pinPlus = plus;
    pinMinus = minus;
    pinSensor = sensor;
    movementSpeed = msp;
    pinSpeed = mspin;
    delta = d;
  }

  int getTraget() {
    return target;
  }

  int getCurrent() {
    return curPosition;
  }

  void setTarget(int t) {
    target = t;
    isMovingForward = target > curPosition;
  }

  void step(){  
    if (curPosition != target) {
      isOpened = analogRead(pinSensor) < 500;
      lastState = isOpened;

      if (isMovingForward) {        
        this->writeSpeed(movementSpeed - delta);
        this->moveForward();
      }
      else {
        this->writeSpeed(movementSpeed);
        this->moveBackward();
      }
      
      for (int i = 0; i < 2; i++) {
        this->setStartTime();
        
        while (lastState == isOpened) {
          isOpened = analogRead(pinSensor) < 500;
          
          if (millis() - startTime > 1000) {
            if (!isMovingForward) {
              curPosition = 0;
            }
            else {
              curPosition = 47;
            }
            Serial.println("data#moveDone");
            return;
          }
        }
        lastState = isOpened;
      }
      
      if (isMovingForward) {
        curPosition++;
      }
      else {
        curPosition--;
      }
      if (curPosition == target) {
        Serial.println("data#moveDone");
      }
    }
    this->Stop();
  }

  void reset () {
    if (delta != 0) {
      this->setTarget(-100);
    }
    else {
      this->setTarget(70);
    }
    while (target != curPosition) {
      this->step();
    }
    this->Stop();
    target = 0;
    curPosition = 0;
  }
};

// переменные для сообщений
String msg; // буфер
int index; // индекс разделителя
char sep = SEPARATOR; // разделитель
String command; // команда
int argument1; // аргумент(-ы) команды
int argument2;

// для движения манипулятора в координатной плоскости
float railLength = 45; // длина рейки
int angle0 = 60; // нулевой угол
int minRadius = 10; // минимальный радиус
float dstep = 0.745;//длинна шага в сантиметрах

// моторы движения по рейке 
railMotor horMotor;
railMotor verMotor;

// сервоприводы манипулятора
ServoSmooth railServo;
ServoSmooth manRotServo;
// Servo manRotServo;
Servo manGrabServo;

void executeCommand(String cmd, int arg1, int arg2) {
  if (cmd == "getPlate") { // проверка платы
    Serial.println("data#manipulator");
  }
  else if (cmd == "moveVerRail") { // 
    verMotor.setTarget(arg1);
  }
  else if (cmd == "moveHorRail") { // движение манипулятора по горизонтальной рейке
    horMotor.setTarget(arg1);
  }
  else if (cmd == "rotateRail") { // повернуть горизонтальную рейку
    railServo.setTargetDeg(arg1);
  }
  else if (cmd == "rotateManipulator") { // повернуть манипулятор
    manRotServo.setTargetDeg(arg1);

    // manRotServo.write(arg);
  }
  else if (cmd == "grabManipulator") { // захват манипулятора
    manGrabServo.write(arg1);
  }
  else if (cmd == "reset") { // выставление в 0 для сброса погрешности
    verMotor.reset();
    railServo.setTargetDeg(90);
    while (railServo.getCurrentDeg() != 90) {
      railServo.tick();
    }
    horMotor.reset();
    Serial.println("data#resetDone");
  }
  else if (cmd == "moveManipulator") { // движение манипулятора по абсолютным координатам
    Serial.println("start moving");
    int railAngle = (int)round(degrees(atan2((railLength * sin(radians(angle0)) - arg2), (railLength * cos(radians(angle0)) - arg1)))); // новый угол рейки
    int manipulatorPos = (int)round(((railLength * cos(radians(angle0)) - arg1) / cos(radians(railAngle)) - minRadius) / dstep); // позиция манипулятора на горизонтальной рейке
    Serial.println(String(railAngle));
    Serial.println(String(manipulatorPos));
    horMotor.setTarget(manipulatorPos);
    railServo.setTargetDeg(railAngle);
    manRotServo.setTargetDeg(180-railAngle);
  }
  else if (cmd == "getCoordinates") {
    int x1 = (int)round(railLength * cos(radians(angle0)) - (horMotor.getCurrent() * dstep + minRadius) * cos(radians(railServo.getCurrentDeg())));
    int y1 = (int)round(railLength * sin(radians(angle0)) - (horMotor.getCurrent() * dstep + minRadius) * sin(radians(railServo.getCurrentDeg())));
    Serial.println("data#cords#" + String(x1) + '#' + String(y1));
  }
  else if (cmd == "getCurrent") {
    Serial.println(String(horMotor.getCurrent()) + " " + String(railServo.getCurrentDeg()));
  }
}  
 
void setup()
{
  Serial.begin(9600);

  // настройка пинов
  pinMode(5, OUTPUT);
  pinMode(PIN_HORMOT_PLUS, OUTPUT);
  pinMode(PIN_HORMOT_MINUS, OUTPUT);
  pinMode(PIN_VERMOT_PLUS, OUTPUT);
  pinMode(PIN_VERMOT_MINUS, OUTPUT);
  
  horMotor.attach(PIN_HORMOT_PLUS, PIN_HORMOT_MINUS, PIN_HORSENS, 140, 0, 5);
  verMotor.attach(PIN_VERMOT_PLUS, PIN_VERMOT_MINUS, PIN_VERSENS, 220, 100, 5);

  railServo.attach(6, 600, 2400, 90);  // 600 и 2400 - длины импульсов, при которых
  // серво поворачивается максимально в одну и другую сторону, зависят от самой серво
  // и обычно даже указываются продавцом. Мы их тут указываем для того, чтобы
  // метод setTargetDeg() корректно отрабатывал полный диапазон поворота сервы 
  railServo.smoothStart();
  railServo.setSpeed(40);   // ограничить скорость
  railServo.setAccel(0);    // установить ускорение (разгон и торможение)
  railServo.setAutoDetach(false); // отключить автоотключение (detach) при достижении целевого угла (по умолчанию включено)

  manRotServo.attach(PIN_ROTSERVO, 90);
  railServo.smoothStart();
  manRotServo.setSpeed(50);   // ограничить скорость
  manRotServo.setAccel(0.3);    // установить ускорение (разгон и торможение)
  manRotServo.setAutoDetach(false);
 
  manGrabServo.attach(PIN_GRABSERVO);
  // manGrabServo.setSpeed(50);   // ограничить скорость
  // manGrabServo.setAccel(0.3);    // установить ускорение (разгон и торможение)
  // manGrabServo.setAutoDetach(false);

  // manRotServo.setTargetDeg(90);
}

void loop()
{
  railServo.tick();
  manRotServo.tick();
  //  manGrabServo.tick();

  horMotor.step();
  verMotor.step();

  if (Serial.available()) {
    msg = Serial.readStringUntil('\n');
    
    index = msg.indexOf(sep);
    command = msg.substring(0, index);
    msg.remove(0, index+1);
    index = msg.indexOf(sep);
    argument1 = (msg.substring(0, index)).toInt();
    msg.remove(0, index+1);
    argument2 = msg.toInt();

    Serial.println(command);

    executeCommand(command, argument1, argument2);
  }
  
  delay(10);
}