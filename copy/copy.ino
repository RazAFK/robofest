#include <ServoDriverSmooth.h>
#include <Adafruit_PWMServoDriver.h>
#include <ServoSmooth.h>
#include <smoothUtil.h>

// пины платформы
#define PIN_MOT1_PLUS A0
#define PIN_MOT1_MINUS A1
#define PIN_MOT2_PLUS A2
#define PIN_MOT2_MINUS A3
#define PIN_MOT3_PLUS A4
#define PIN_MOT3_MINUS A5
#define PIN_MOT4_PLUS 12
#define PIN_MOT4_MINUS 13

// пины манипулятора
#define PIN_HORSENS A6 // сенсор горизонтального движения
#define PIN_VERSENS A7 // сенсор вертикального движения

class yellowMotor {
  protected:
  int pinPlus;
  int pinMinus;

  static const int pinSpeed = 5;

  public:
  void attach(int plus, int minus) {
    pinPlus = plus;
    pinMinus = minus; 
  }
};

class reykaMotor : yellowMotor {
  int pinSensor;
  int movementSpeed;
  int stoppingSpeed;
  bool isMovingForward = true;

  int curPosition = 0;
  int target = 0;
  bool isOpened;
  bool lastState;
  
  public: 
  void attach(int plus, int minus, int sensor, int msp){
    pinPlus = plus;
    pinMinus = minus;
    pinSensor = sensor;
    movementSpeed = msp;
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

  void Step(){
    
    if (curPosition != target) {
      analogWrite(yellowMotor::pinSpeed, movementSpeed);
      isOpened = analogRead(pinSensor) < 500;
      lastState = isOpened;

      if (isMovingForward) {
        digitalWrite(pinPlus, HIGH);
        digitalWrite(pinMinus, LOW);
      }
      else {
        digitalWrite(pinPlus, LOW);
        digitalWrite(pinMinus, HIGH);
      }
      
      while (lastState == isOpened) {
        isOpened = analogRead(pinSensor) < 500;
      }
      
      if (isMovingForward) {
        curPosition++;
      }
      else {
        curPosition--;
      }
    }
    else if (!isMovingForward && target == 0) {
      curPosition++;
    }
    digitalWrite(pinPlus, LOW);
    digitalWrite(pinMinus, LOW);
  }
};

String msg; // буфер для сообщений

reykaMotor horMotor;
reykaMotor verMotor;

ServoSmooth reykaServo;
ServoSmooth manRotServo;
ServoSmooth manHvatServo;
 
void setup()
{
  Serial.begin(9600);

  // настройка пинов
  pinMode(PIN_MOT1_PLUS, OUTPUT);
  pinMode(PIN_MOT1_MINUS, OUTPUT);
  pinMode(PIN_MOT2_PLUS, OUTPUT);
  pinMode(PIN_MOT2_MINUS, OUTPUT);
  pinMode(PIN_MOT3_PLUS, OUTPUT);
  pinMode(PIN_MOT3_MINUS, OUTPUT);
  pinMode(PIN_MOT4_PLUS, OUTPUT);
  pinMode(PIN_MOT4_MINUS, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(9, OUTPUT);
  
  horMotor.attach(7, 8, PIN_HORSENS, 120);
  verMotor.attach(4, 9, PIN_VERSENS, 250); // последние 3 аргумента скорость движения, остановки, делэй

  reykaServo.attach(6, 600, 2400);  // 600 и 2400 - длины импульсов, при которых
  // серво поворачивается максимально в одну и другую сторону, зависят от самой серво
  // и обычно даже указываются продавцом. Мы их тут указываем для того, чтобы
  // метод setTargetDeg() корректно отрабатывал полный диапазон поворота сервы
  // manRotServo.attach(/*пин поворота*/, 600, 2400);
  // manHvatServo.attach(/*пин хвата*/, 600, 2400);

  reykaServo.setSpeed(50);   // ограничить скорость
  reykaServo.setAccel(0.3);    // установить ускорение (разгон и торможение)

  manRotServo.setSpeed(50);   // ограничить скорость
  manRotServo.setAccel(0.3);    // установить ускорение (разгон и торможение)

  manHvatServo.setSpeed(50);   // ограничить скорость
  manHvatServo.setAccel(0.3);    // установить ускорение (разгон и торможение)
  
  reykaServo.setAutoDetach(false); // отключить автоотключение (detach) при достижении целевого угла (по умолчанию включено)
  manRotServo.setAutoDetach(false);
  manHvatServo.setAutoDetach(false);
}

void loop()
{
//  reykaServo.tick();
//  manRotServo.tick();
//  manHvatServo.tick();

  horMotor.Step();
  verMotor.Step();

  if (Serial.available()) {
    msg = Serial.readStringUntil('\n');

    if (msg == "get") {
//      Serial.print("current == ");
//      Serial.println(curPos);
//      
//      Serial.print("target == ");
//      Serial.println(target);
//
//      Serial.print("counter == ");
//      Serial.println(counter);
    }
    else {
      int t = msg.toInt();

      if (t > verMotor.getCurrent()) {
        verMotor.setTarget(t);
      }
      else {
        verMotor.setTarget(t - 1);
      }
      Serial.println(msg);
    }
  }

  delay(10);
}
