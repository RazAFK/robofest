#include <iarduino_I2C_Software.h>
SoftTwoWire sWire(A4, A5);

#include <iarduino_I2C_Motor.h>

#include <ServoDriverSmooth.h>
#include <ServoSmooth.h>
#include <GyverStepper.h>
#include <StepperCore.h>

// количество аргументов
// #define ARGUMENTS_COUNT 5

// пины csl и sda
// #define PIN_SCL A5
// #define PIN_SDA A4

// пины сервы захвата
#define PIN_SERVO_GRAB 0

// пины сервы поворота клешни
#define PIN_SERVO_MANIPULATOR_ROTATION 0

// пины сервы поворота горизонтальной рейки
#define PIN_SERVO_RAIL_ROTATION 5

// пины мотора на горизонтальной рейке
#define PIN_STEPPER_DIR 10
#define PIN_STEPPER_STEP 11
#define PIN_STEPPER_ENABLE 12
#define STEPPER_STEPS_PER_ROUND 200 // количество шагов для 1 оборота

// вертикальная рейка
// характеристики мотора
#define ENCODER_MAGNET_COUNT_VERTICAL_RAIL 0 // количество магнитов на энкодере (указывается продавцом)
#define REDUCER_VERTICAL_RAIL 0              // передаточное число редуктора
#define RADIUS_VERTICAL_RAIL 0.0             // радиус колеса на моторе
// опционально обозначить скорости

// полярность (направление) мотора
#define VERTICAL_RAIL_MOTOR_DEFAULT_DIRECTION true

// I2C адрес мотора вертикальной рейки
#define ADDRESS_VERTICAL_RAIL_MOTOR 0x09

// колесная база
// характеристики моторов (на колесной базе они одинаковые)
#define ENCODER_MAGNET_COUNT_WHEELS 7   // количество магнитов на энкодере (указывается продавцом)
#define REDUCER_WHEELS 56.0             // передаточное число редуктора
#define RADIUS_WHEELS 50.0              // радиус колеса на моторе
// опционально обозначить скорости

// полярности (направления) колес
#define WHEEL_DEFAULT_DIRECTION_FORWARD_RIGHT false
#define WHEEL_DEFAULT_DIRECTION_FORWARD_LEFT true
#define WHEEL_DEFAULT_DIRECTION_BACKWARD_RIGHT false
#define WHEEL_DEFAULT_DIRECTION_BACKWARD_LEFT true

// I2C адреса колес
#define ADDRESS_FORWARD_RIGHT 0x0A
#define ADDRESS_FORWARD_LEFT 0x0B
#define ADDRESS_BACKWARD_RIGHT 0x0C
#define ADDRESS_BACKWARD_LEFT 0x0D

class MessageSender {
    static const String prefixes[];

    static const char separator = '#';

    enum prefix {
        RAIL,
        WHEELS,
        DATA
    };

    static void sendMessage(prefix p, String msg) {
        Serial.println(prefixes[DATA] + separator + 
                       prefixes[p] + separator + msg);
    }
};
const String MessageSender::prefixes[] = {
    "arm",
    "whe",
    "data"
};

class EncoderMotor {
    iarduino_I2C_Motor motor;

    public:
    EncoderMotor(int I2CAddress, 
                 int magnetsCount,
                 float reducer, 
                 float wheelRadius, 
                 bool defaultDirection,
                 SoftTwoWire sWire) : 
        motor(iarduino_I2C_Motor(I2CAddress))
    { 
        motor.begin(&sWire);
        motor.setMagnet(magnetsCount);
        motor.setReducer(reducer);
        motor.radius = wheelRadius;
        motor.setDirection(defaultDirection);

        Serial.println("motor initialized");
    }

    void move(float speed = 0, float distance = 0);
    void stop();
};

class Rail {
    Servo& grabServo;
    Servo& manipulatorRotationServo;
    ServoSmooth& railRotationServo;
    GStepper<STEPPER2WIRE>& horizontalRailMotor;
    EncoderMotor& verticalRailMotor;

    public:
    Rail(Servo& grabServo, 
         Servo& manipulatorRotationServo, 
         ServoSmooth& railRotationServo, 
         GStepper<STEPPER2WIRE>& horizontalRailMotor, 
         EncoderMotor& verticalRailMotor) :
        grabServo(grabServo),
        manipulatorRotationServo(manipulatorRotationServo),
        railRotationServo(railRotationServo),
        horizontalRailMotor(horizontalRailMotor),
        verticalRailMotor(verticalRailMotor) 
    { }

    // движение манипулятора в горизонтальной плоскости
    void moveManipulator(int manipulatorPosition = 0, int servoDegrees = 90);
    void moveHorizontalRail(int position);
    void rotateRail(int degs);

    // движение манипулятора в вертикальной плоскости
    void grab(int position = 0, int rotateServoDegrees = 90, int grabServoDegrees = 0);
    void moveVerticalRail(int position);
    void rotateManipulator(int deWgs);
    void grabManipulator(int degs);
};

class WheelBase {
    EncoderMotor& forwardRight;
    EncoderMotor& forwardLeft;
    EncoderMotor& backwardRight;
    EncoderMotor& backwardLeft;

    public:
    WheelBase(EncoderMotor& forwardRight,
              EncoderMotor& forwardLeft,
              EncoderMotor& backwardRight,
              EncoderMotor& backwardLeft) :
        forwardRight(forwardRight),
        forwardLeft(forwardLeft),
        backwardRight(backwardRight),
        backwardLeft(backwardLeft)
    {}

    void virtual moveForward(float speed, float distance);
    void moveForward(float speedFR, 
                     float speedFL, 
                     float speedBR, 
                     float speedBL, 
                     float distance);
    void virtual moveBackward(float speed, float distance);
    void moveBackward(float speedFR, 
                      float speedFL, 
                      float speedBR, 
                      float speedBL, 
                      float distance);
    void virtual rotateRight(float speed, float distance);
    void rotateRight(float speedFR, 
                     float speedFL, 
                     float speedBR, 
                     float speedBL, 
                     float distance);
    void virtual rotateLeft(float speed, float distance);
    void rotateLeft(float speedFR, 
                    float speedFL, 
                    float speedBR, 
                    float speedBL, 
                    float distance);

    void stop();

};

class InputMessageHandler {
    static Rail* rail = nullptr;
    static WheelBase* base = nullptr;

    public:
    static void setRail(Rail& r) {
        rail = &r;
    }

    static void setWheelBase(WheelBase& b) {
        base = &b;
    }

    static String processMessage(String message); // парсинг строки

    static void executeCommand(String command = "stop", int argument1 = 0, int argument2 = 0); // выполнение полученной команды
};

Servo grabServo;
Servo manipulatorRotationServo;

ServoSmooth railRotationServo;

GStepper<STEPPER2WIRE> horizontalRailMotor(STEPPER_STEPS_PER_ROUND, 
                                           PIN_STEPPER_STEP, 
                                           PIN_STEPPER_DIR, 
                                           PIN_STEPPER_ENABLE);

EncoderMotor verticalRailMotor(ADDRESS_VERTICAL_RAIL_MOTOR,
                               ENCODER_MAGNET_COUNT_VERTICAL_RAIL,
                               REDUCER_VERTICAL_RAIL,
                               RADIUS_VERTICAL_RAIL,
                               VERTICAL_RAIL_MOTOR_DEFAULT_DIRECTION,
                               sWire);

Rail rail(grabServo, 
          manipulatorRotationServo, 
          railRotationServo, 
          horizontalRailMotor, 
          verticalRailMotor);

EncoderMotor forwardRight(ADDRESS_FORWARD_RIGHT, 
                          ENCODER_MAGNET_COUNT_WHEELS,
                          REDUCER_WHEELS,
                          RADIUS_WHEELS,
                          WHEEL_DEFAULT_DIRECTION_FORWARD_RIGHT,
                          sWire);
EncoderMotor forwardLeft(ADDRESS_FORWARD_LEFT, 
                         ENCODER_MAGNET_COUNT_WHEELS,
                         REDUCER_WHEELS,
                         RADIUS_WHEELS,
                         WHEEL_DEFAULT_DIRECTION_FORWARD_LEFT,
                         sWire);
EncoderMotor backwardRight(ADDRESS_BACKWARD_RIGHT, 
                           ENCODER_MAGNET_COUNT_WHEELS,
                           REDUCER_WHEELS,
                           RADIUS_WHEELS,
                           WHEEL_DEFAULT_DIRECTION_BACKWARD_RIGHT,
                           sWire);
EncoderMotor backwardLeft(ADDRESS_BACKWARD_LEFT, 
                          ENCODER_MAGNET_COUNT_WHEELS,
                          REDUCER_WHEELS,
                          RADIUS_WHEELS,
                          WHEEL_DEFAULT_DIRECTION_BACKWARD_LEFT,
                          sWire);

WheelBase wheelBase(forwardRight,
                    forwardLeft,
                    backwardRight,
                    backwardLeft);

void setup () {
    Serial.begin(9600);

    Serial.println("Setup started");

    sWire.begin();

    Serial.println("wire have began");

    pinMode(PIN_SERVO_GRAB, OUTPUT);
    pinMode(PIN_SERVO_MANIPULATOR_ROTATION, OUTPUT);
    pinMode(PIN_SERVO_RAIL_ROTATION, OUTPUT);
    pinMode(PIN_STEPPER_DIR, OUTPUT);
    pinMode(PIN_STEPPER_ENABLE, OUTPUT);
    pinMode(PIN_STEPPER_STEP, OUTPUT);

    railRotationServo.attach(PIN_SERVO_RAIL_ROTATION, 500, 2500, 0);
    railRotationServo.smoothStart();
    railRotationServo.setMaxAngle(270);
    railRotationServo.setSpeed(60);         // ограничить скорость
    railRotationServo.setAccel(0);          // установить ускорение (разгон и торможение)
    railRotationServo.setAutoDetach(false); // отключить автоотключение (detach) при достижении целевого угла (по умолчанию включено)

    horizontalRailMotor.setRunMode(FOLLOW_POS);
    horizontalRailMotor.setMaxSpeed(400);
    horizontalRailMotor.setAcceleration(400);

    grabServo.attach(PIN_SERVO_GRAB);
    manipulatorRotationServo.attach(PIN_SERVO_MANIPULATOR_ROTATION);

    wheelBase.moveForward(0.5f, 1.0f);

    // forwardRight.move(0.5f, 1.0f);
}

String msg; // буфер для полученных сообщений

void loop() {
    // railRotationServo.tick();
    // horizontalRailMotor.tick();

    // if (Serial.available()) {
    // msg = Serial.readStringUntil('\n');

    // Serial.println(msg);

    // rail.moveHorizontalRail(msg.toInt());

    // // rail.rotateRail(msg.toInt());
//   }
}
//
// методы класса EncoderMotor
//
void EncoderMotor::move(float speed, float distance) {
    motor.setSpeed(speed, MOT_M_S, distance, MOT_MET);
}

void EncoderMotor::stop() {
    this->move(0, 0);
}
//
// методы класса Rail
//
void Rail::rotateRail(int degs) {
    railRotationServo.setTargetDeg(degs);
}

void Rail::moveHorizontalRail(int position) {
    horizontalRailMotor.setTarget(position);
}
//
// методы класса WheelBase
//
void WheelBase::moveForward(float speed, float distance) {
    forwardRight.move(speed, distance);
    forwardLeft.move(speed, distance);
    backwardRight.move(speed, distance);
    backwardLeft.move(speed, distance);
}
void WheelBase::moveForward(float speedFR, 
                            float speedFL, 
                            float speedBR, 
                            float speedBL, 
                            float distance) {
    forwardRight.move(speedFR, distance);
    forwardLeft.move(speedFL, distance);
    backwardRight.move(speedBR, distance);
    backwardLeft.move(speedBL, distance);
}

void WheelBase::moveBackward(float speed, float distance) {
    forwardRight.move(-speed, distance);
    forwardLeft.move(-speed, distance);
    backwardRight.move(-speed, distance);
    backwardLeft.move(-speed, distance);
}
void WheelBase::moveBackward(float speedFR, 
                             float speedFL, 
                             float speedBR, 
                             float speedBL, 
                             float distance) {
    forwardRight.move(-speedFR, distance);
    forwardLeft.move(-speedFL, distance);
    backwardRight.move(-speedBR, distance);
    backwardLeft.move(-speedBL, distance);
}

void WheelBase::rotateRight(float speed, float distance) {
    forwardRight.move(speed, distance);
    forwardLeft.move(-speed, distance);
    backwardRight.move(speed, distance);
    backwardLeft.move(-speed, distance);
}
void WheelBase::rotateRight(float speedFR, 
                            float speedFL, 
                            float speedBR, 
                            float speedBL, 
                            float distance) {
    forwardRight.move(speedFR, distance);
    forwardLeft.move(-speedFL, distance);
    backwardRight.move(speedBR, distance);
    backwardLeft.move(-speedBL, distance);
}

void WheelBase::rotateLeft(float speed, float distance) {
    forwardRight.move(-speed, distance);
    forwardLeft.move(speed, distance);
    backwardRight.move(-speed, distance);
    backwardLeft.move(speed, distance);
}
void WheelBase::rotateLeft(float speedFR, 
                           float speedFL, 
                           float speedBR, 
                           float speedBL, 
                           float distance) {
    forwardRight.move(-speedFR, distance);
    forwardLeft.move(speedFL, distance);
    backwardRight.move(-speedBR, distance);
    backwardLeft.move(speedBL, distance);
}

void WheelBase::stop() {
    forwardRight.stop();
    forwardLeft.stop();
    backwardRight.stop();
    backwardLeft.stop();
}
//
// методы класса InputMessageHandler
//
static String InputMessageHandler::processMessage(String message) {
    // todo: парсинг строки и ифы для команд
    String command;
    // float[ARGUMENTS_COUNT] arguments = new;
    // if ()
}
//
// методы класса OutputMessageHandler
//