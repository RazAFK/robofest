#include <ServoDriverSmooth.h>
#include <ServoSmooth.h>

// пины манипулятора
#define PIN_HORSENS A6 // сенсор горизонтального движения
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
  
  public: 
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
    this->Stop();
  }

  void reset () {
    this->setTarget(-1);

    while (target != curPosition) {
      this->step();
    }

    target = 0;
    curPosition = 0;
  }
};

// переменные для сообщений
String msg; // буфер
int index; // индекс разделителя
char sep = SEPARATOR; // разделитель
String command; // команда
int argument; // аргумент(-ы) команды

// моторы движения по рейке 
railMotor horMotor;
railMotor verMotor;

// сервоприводы манипулятора
ServoSmooth railServo;
ServoSmooth manRotServo;
// Servo manRotServo;
ServoSmooth manGrabServo;

void executeCommand(String cmd, int arg) {
  if (cmd == "getPlate") {
    Serial.println("manipulator");
  }
  else if (cmd == "moveVerRail") {
    verMotor.setTarget(arg);
  }
  else if (cmd == "moveHorRail") {
    horMotor.setTarget(arg);
  }
  else if (cmd == "rotateManipulator") {
    // manRotServo.setTargetDeg(arg);

    manRotServo.write(arg);
  }
  else if (cmd == "grabManipulator") {
    manGrabServo.setTargetDeg(arg);
  }
  else if (cmd == "rotateRail") {
    railServo.setTargetDeg(arg);
  }
  else if (cmd == "reset") {
    verMotor.reset();
    railServo.setTargetDeg(90);
    while (railServo.getCurrentDeg() != 90) {
      railServo.tick();
    }
    horMotor.reset();
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
  
  horMotor.attach(PIN_HORMOT_PLUS, PIN_HORMOT_MINUS, PIN_HORSENS, 120, 0, 5);
  verMotor.attach(PIN_VERMOT_PLUS, PIN_VERMOT_MINUS, PIN_VERSENS, 220, 100, 5);

  railServo.attach(6, 600, 2400);  // 600 и 2400 - длины импульсов, при которых
  // серво поворачивается максимально в одну и другую сторону, зависят от самой серво
  // и обычно даже указываются продавцом. Мы их тут указываем для того, чтобы
  // метод setTargetDeg() корректно отрабатывал полный диапазон поворота сервы
  // manRotServo.attach(PIN_ROTSERVO, 600, 2400);   
  railServo.setSpeed(50);   // ограничить скорость
  railServo.setAccel(0.3);    // установить ускорение (разгон и торможение)

  manRotServo.attach(PIN_ROTSERVO);
  manRotServo.setSpeed(50);   // ограничить скорость
  manRotServo.setAccel(0.3);    // установить ускорение (разгон и торможение)
  
  manGrabServo.attach(PIN_GRABSERVO, 600, 2400);
  manGrabServo.setSpeed(50);   // ограничить скорость
  manGrabServo.setAccel(0.3);    // установить ускорение (разгон и торможение)
  
  railServo.setAutoDetach(false); // отключить автоотключение (detach) при достижении целевого угла (по умолчанию включено)
  manRotServo.setAutoDetach(false);
  manGrabServo.setAutoDetach(false);
}

void loop()
{
  railServo.tick();
  manRotServo.tick();
  manGrabServo.tick();

  horMotor.step();
  verMotor.step();

  if (Serial.available()) {
    msg = Serial.readStringUntil('\n');
    index = msg.indexOf(sep);
    command = msg.substring(0, index);
    msg.remove(0, index+1);
    argument = msg.toInt();

    executeCommand(command, argument);
  }
  
  delay(10);
}
