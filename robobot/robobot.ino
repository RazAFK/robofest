#include <ServoDriverSmooth.h>
#include <Adafruit_PWMServoDriver.h>
#include <ServoSmooth.h>
#include <smoothUtil.h>

#define PIN_SENS_HOR A6 // сенсор горизонтального движения
#define PIN_SENS_VER A7 // сенсор вертикального движения

class yellowMotor {
  protected:
  int pinPlus;
  int pinMinus;

  public:
  yellowMotor(int plus, int minus) {
    pinPlus = plus;
    pinMinus = minus; 
  }
};

class reykaMotor : yellowMotor {
  int pinSpeed;
  int pinSensor;
  int movementSpeed;
  int stoppingSpeed;
  int del;
  
  public: 
  reykaMotor(int plus, int minus, int sp, int sensor, int msp, int ssp, int d) : yellowMotor(plus, minus) {
    pinSpeed = sp;
    pinSensor = sensor;
    movementSpeed = msp;
    stoppingSpeed = ssp;
    del = d;
  }

  void moveBySteps(int n, bool isMovingForward){
    for (int i = 0; i < n; i++) {
      int changes = 0;
      bool flag = analogRead(pinSensor) > 500;
      while (changes != 1) {
          analogWrite(pinSpeed, movementSpeed);
          
          if (isMovingForward) {
            digitalWrite(pinPlus, HIGH);
            digitalWrite(pinMinus, LOW);
          }
          else {
            digitalWrite(pinPlus, LOW);
            digitalWrite(pinMinus, HIGH);
          }
          if (analogRead(pinSensor) > 500 != flag) {
            flag = analogRead(pinSensor) > 500;
            changes++;
          }
          analogWrite(pinSpeed, stoppingSpeed);
          if (!isMovingForward) {
            digitalWrite(pinPlus, HIGH);
            digitalWrite(pinMinus, LOW);
          }
          else {
            digitalWrite(pinPlus, LOW);
            digitalWrite(pinMinus, HIGH);
          }
      }
      delay(del);
    }
    digitalWrite(pinPlus, LOW);
    digitalWrite(pinMinus, LOW);
  }
};

//String[3] ProcessMessage(String message) {
//  String command;
//  String object;
//  String 
//}

String msg;

reykaMotor* horMotor;
reykaMotor* verMotor;

ServoSmooth reykaServo;
ServoSmooth manRotServo;
ServoSmooth manHvatServo;
 
void setup()
{
  Serial.begin(9600);
  pinMode(5, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  
  horMotor = new reykaMotor(7, 8, 5, PIN_SENS_HOR, 100, 30, 100);
  verMotor = new reykaMotor(4, 9, 5, PIN_SENS_VER, 100, 30, 100); // последние 3 аргумента скорость движения, остановки, делэй

  reykaServo.attach(6, 600, 2400);  // 600 и 2400 - длины импульсов, при которых
  // серво поворачивается максимально в одну и другую сторону, зависят от самой серво
  // и обычно даже указываются продавцом. Мы их тут указываем для того, чтобы
  // метод setTargetDeg() корректно отрабатывал полный диапазон поворота сервы
  manRotServo.attach(/*пин поворота*/, 600, 2400);
  manHvatServo.attach(/*пин хвата*/, 600, 2400);
  
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
  if (Serial.available()) {
    msg = Serial.readStringUntil('\n');
  }
  reykaServo.tick();
  manRotServo.tick();
  manHvatServo.tick();
  

//   horMotor->moveBySteps(10, true);
//   horMotor->moveBySteps(10, false);

  delay(50);
}
