#include <iarduino_I2C_Software.h>
#include <iarduino_I2C_Motor.h>
#include <ServoDriverSmooth.h>
#include <ServoSmooth.h>
#include <GyverStepper.h>
#include <StepperCore.h>

// количество аргументов
#define ARGUMENTS_COUNT 5

// пины csl и sda
#define PIN_SCL A5
#define PIN_SDA A4

#define SEPARATOR "#"

// пины сервы захвата
#define PIN_SERVO_GRAB 8

// пины сервы поворота клешни
#define PIN_SERVO_MANIPULATOR_ROTATION 9

// пины сервы поворота горизонтальной рейки
#define PIN_SERVO_RAIL_ROTATION 4

// пины мотора на горизонтальной рейке
#define PIN_STEPPER_DIR 1
#define PIN_STEPPER_STEP 2
#define PIN_STEPPER_ENABLE 3
#define STEPPER_STEPS_PER_ROUND 200 // количество шагов для 1 оборота

// вертикальная рейка
// характеристики мотора
#define ENCODER_MAGNET_COUNT_VERTICAL_RAIL 13 // количество магнитов на энкодере (указывается продавцом)
#define REDUCER_VERTICAL_RAIL 49.4f

// передаточное число редуктора
#define RADIUS_VERTICAL_RAIL 30.0            // радиус колеса на моторе
#define SPEED_VERTICAL_RAIL 0.15f
// опционально обозначить скорости

// полярность (направление) мотора
#define VERTICAL_RAIL_MOTOR_DEFAULT_DIRECTION true

// I2C адрес мотора вертикальной рейки
#define ADDRESS_VERTICAL_RAIL_MOTOR 0x0C

// колесная база
// характеристики моторов (на колесной базе они одинаковые)
#define ENCODER_MAGNET_COUNT_WHEELS 12       // количество магнитов на энкодере (указывается продавцом)
#define ENCODER_MAGNET_COUNT_BROKEN_WHEEL 12 // одно колесо поломанное вообще 11.7
#define REDUCER_WHEELS 27.5                  // передаточное число редуктора
#define RADIUS_WHEELS 50.0                   // радиус колеса на моторе
#define CHARGE_DISTANCE 0.12f                 // дистанция для разгона до максимальной скорости
// опционально обозначить скорости

// полярности (направления) колес
#define WHEEL_DEFAULT_DIRECTION_FORWARD_RIGHT true
#define WHEEL_DEFAULT_DIRECTION_FORWARD_LEFT false
#define WHEEL_DEFAULT_DIRECTION_BACKWARD_RIGHT true
#define WHEEL_DEFAULT_DIRECTION_BACKWARD_LEFT false

// I2C адреса колес
#define ADDRESS_FORWARD_RIGHT 0x0B
#define ADDRESS_FORWARD_LEFT 0x09
#define ADDRESS_BACKWARD_RIGHT 0x0D
#define ADDRESS_BACKWARD_LEFT 0x0A

class EncoderMotor {
    protected:
    iarduino_I2C_Motor motor;

    bool flagDefaultDirection;
    bool isMoving = false;

    public:
    EncoderMotor(int I2CAddress, 
                 int magnetsCount,
                 float reducer, 
                 float wheelRadius, 
                 bool defaultDirection) : 
        motor(iarduino_I2C_Motor(I2CAddress)),
        flagDefaultDirection(defaultDirection)
    { 
        motor.setMagnet(magnetsCount);
        motor.setReducer(reducer);
        motor.radius = wheelRadius;
    }

    void begin(SoftTwoWire* sWire) {
        motor.begin(sWire);
    }

    void movea(float speed = 0, float distance = 0);
    float getPosition();
    float getTarget();
    void stop();
};

class WheelMotor : public EncoderMotor {
    public:
    WheelMotor(int I2CAddress, 
               int magnetsCount,
               float reducer, 
               float wheelRadius, 
               bool defaultDirection) : 
        EncoderMotor(I2CAddress, 
                     magnetsCount,
                     reducer, 
                     wheelRadius, 
                     defaultDirection) {}
    void move(float speed, float distance);
    bool checkIfStop();
    
};

class VerticalRailMotor : public EncoderMotor {
    float tempPosition = 0.0f;
    int timer = 0;

    public:
    VerticalRailMotor(int I2CAddress, 
                      int magnetsCount,
                      float reducer, 
                      float wheelRadius, 
                      bool defaultDirection) : 
        EncoderMotor(I2CAddress, 
                     magnetsCount,
                     reducer, 
                     wheelRadius, 
                     defaultDirection) {}

    void move(float speed);
    void stopIfStuck();
};

class Manipulator {
    Servo& grabServo;
    ServoSmooth& manipulatorRotationServo;
    ServoSmooth& railRotationServo;
    GStepper<STEPPER2WIRE>& horizontalRailMotor;
    VerticalRailMotor& verticalRailMotor;

    public:
    Manipulator(Servo& grabServo, 
                ServoSmooth& manipulatorRotationServo, 
                ServoSmooth& railRotationServo, 
                GStepper<STEPPER2WIRE>& horizontalRailMotor, 
                VerticalRailMotor& verticalRailMotor) :
        grabServo(grabServo),
        manipulatorRotationServo(manipulatorRotationServo),
        railRotationServo(railRotationServo),
        horizontalRailMotor(horizontalRailMotor),
        verticalRailMotor(verticalRailMotor) 
    { }

    // движение манипулятора в горизонтальной плоскости
    void moveManipulator(int manipulatorPosition = 0, int servoDegrees = 180, int manipulatorServoDegrees = 0);
    void moveHorizontalRail(int position);
    void rotateRail(int degs);

    // движение манипулятора в вертикальной плоскости
    void grab(int rotateServoDegrees = 90, int grabServoDegrees = 0);
    void moveVerticalRail(float speed);
    void rotateManipulator(int degs);
    void rotateGrabServo(int degs);

    int getRailRotationServoDegrees();
    int getManipulatorRotationServoDegrees();
    int getGrabServoDegrees();
    int getHorizontalRailMotorPosition();
};

class WheelBase {
    int timer = 0;

    WheelMotor& forwardRight;
    WheelMotor& forwardLeft;
    WheelMotor& backwardRight;
    WheelMotor& backwardLeft;

    public:
    WheelBase(WheelMotor& forwardRight,
              WheelMotor& forwardLeft,
              WheelMotor& backwardRight,
              WheelMotor& backwardLeft) :
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
    void virtual moveRight(float speed, float distance); // езда крабом
    void moveRight(float speedFR, 
                   float speedFL, 
                   float speedBR, 
                   float speedBL, 
                   float distance);
    void virtual moveLeft(float speed, float distance);
    void moveLeft(float speedFR, 
                  float speedFL, 
                  float speedBR, 
                  float speedBL, 
                  float distance);
    void stop();
    bool checkIfStop();
};

class MessageHandler {
    static Manipulator* manipulator;
    static WheelBase* wheelBase;

    static const char separator;
    static const String prefixes[];

    public:
    enum prefix {
        RAIL,
        WHEELS,
        DATA
    };

    static void setManipulator(Manipulator& r) {
        manipulator = &r;
    }

    static void setWheelBase(WheelBase& b) {
        wheelBase = &b;
    }

    static void sendMessage(prefix p, String* messageArguments) {
        String processedMessage = prefixes[DATA] + SEPARATOR +
                                  prefixes[p] + SEPARATOR;
        for (int i = 0; i < sizeof(messageArguments) - 1; i++) {
            processedMessage += messageArguments[i] + SEPARATOR;
        }
        Serial.println(processedMessage);
    }

    static void processMessage(String message); // парсинг строки

    static void executeCommand(String command = "stop", float* arguments = nullptr); // выполнение полученной команды
};

Manipulator* MessageHandler::manipulator = nullptr;
WheelBase* MessageHandler::wheelBase = nullptr;

const char MessageHandler::separator = SEPARATOR;

const String MessageHandler::prefixes[] = {
    "arm",
    "whe",
    "data"
}; // егор дибил нормальные не придумал и переделывать не хочет

SoftTwoWire sWire(PIN_SDA, PIN_SCL);

Servo grabServo;
ServoSmooth manipulatorRotationServo;

ServoSmooth railRotationServo;

GStepper<STEPPER2WIRE> horizontalRailMotor(STEPPER_STEPS_PER_ROUND,
                                           PIN_STEPPER_STEP, 
                                           PIN_STEPPER_DIR, 
                                           PIN_STEPPER_ENABLE);

VerticalRailMotor verticalRailMotor(ADDRESS_VERTICAL_RAIL_MOTOR,
                                    ENCODER_MAGNET_COUNT_VERTICAL_RAIL,
                                    REDUCER_VERTICAL_RAIL,
                                    RADIUS_VERTICAL_RAIL,
                                    VERTICAL_RAIL_MOTOR_DEFAULT_DIRECTION);

Manipulator manipulator(grabServo, 
                        manipulatorRotationServo, 
                        railRotationServo, 
                        horizontalRailMotor, 
                        verticalRailMotor);

WheelMotor forwardRight(ADDRESS_FORWARD_RIGHT, 
                        ENCODER_MAGNET_COUNT_WHEELS,
                        REDUCER_WHEELS,
                        RADIUS_WHEELS,
                        WHEEL_DEFAULT_DIRECTION_FORWARD_RIGHT);
WheelMotor forwardLeft(ADDRESS_FORWARD_LEFT, 
                       ENCODER_MAGNET_COUNT_BROKEN_WHEEL,
                       REDUCER_WHEELS,
                       RADIUS_WHEELS,
                       WHEEL_DEFAULT_DIRECTION_FORWARD_LEFT);
WheelMotor backwardRight(ADDRESS_BACKWARD_RIGHT, 
                         ENCODER_MAGNET_COUNT_WHEELS,
                         REDUCER_WHEELS,
                         RADIUS_WHEELS,
                         WHEEL_DEFAULT_DIRECTION_BACKWARD_RIGHT);
WheelMotor backwardLeft(ADDRESS_BACKWARD_LEFT, 
                        ENCODER_MAGNET_COUNT_WHEELS,
                        REDUCER_WHEELS,
                        RADIUS_WHEELS,
                        WHEEL_DEFAULT_DIRECTION_BACKWARD_LEFT);

WheelBase wheelBase(forwardRight,
                    forwardLeft,
                    backwardRight,
                    backwardLeft);

void setup () {
    Serial.begin(9600);

    Serial.println("Setup started");

    delay(500);

    sWire.begin();

    delay(1000); // китенок сказал для стабилизации надо

    Serial.println("wire has began");

    pinMode(PIN_SERVO_GRAB, OUTPUT);
    pinMode(PIN_SERVO_MANIPULATOR_ROTATION, OUTPUT);
    pinMode(PIN_SERVO_RAIL_ROTATION, OUTPUT);
    pinMode(PIN_STEPPER_DIR, OUTPUT);
    pinMode(PIN_STEPPER_ENABLE, OUTPUT);
    pinMode(PIN_STEPPER_STEP, OUTPUT);

    railRotationServo.setMaxAngle(270);
    railRotationServo.setSpeed(60);         // ограничить скорость
    railRotationServo.setAccel(0);          // установить ускорение (разгон и торможение)
    // railRotationServo.setAutoDetach(false); // отключить автоотключение (detach) при достижении целевого угла (по умолчанию включено)
    railRotationServo.attach(PIN_SERVO_RAIL_ROTATION, 500, 2500, 180);
    railRotationServo.smoothStart();

    horizontalRailMotor.autoPower(true);
    horizontalRailMotor.setRunMode(FOLLOW_POS);
    horizontalRailMotor.reverse(true);
    horizontalRailMotor.setMaxSpeed(800);
    horizontalRailMotor.setAcceleration(800);

    manipulatorRotationServo.setMaxAngle(180);
    manipulatorRotationServo.setSpeed(90);         // ограничить скорость
    manipulatorRotationServo.setAccel(0);          // установить ускорение (разгон и торможение)
    // railRotationServo.setAutoDetach(false); // отключить автоотключение (detach) при достижении целевого угла (по умолчанию включено)
    manipulatorRotationServo.attach(PIN_SERVO_MANIPULATOR_ROTATION);
    manipulatorRotationServo.smoothStart();

    // grabServo.attach(PIN_SERVO_GRAB);

    forwardRight.begin(&sWire);
    forwardLeft.begin(&sWire);
    backwardRight.begin(&sWire);
    backwardLeft.begin(&sWire);
    verticalRailMotor.begin(&sWire);

    // delay(2000);

    // wheelBase.moveForward(0.3f, 0.6f);

    // delay(3000);

    // wheelBase.moveBackward(0.3f, 0.6f);

    // delay(3000);

    // wheelBase.moveRight(0.3f, 0.3f);

    // delay(2000);

    // wheelBase.moveLeft(0.3f, 0.3f);

    MessageHandler::setWheelBase(wheelBase);
    MessageHandler::setManipulator(manipulator);

    // manipulatorRotationServo.setTargetDeg(0);
    // railRotationServo.setTargetDeg(180);
}

String msg; // буфер для полученных сообщений

bool kostyl1 = false;  // для сервы поворота рейки
bool kostyl2 = false;  // для горизонтальной рейки (шаговый)
bool kostyl3 = false;  // для хватательной сервы
bool kostyl4 = false;  // для вращательной сервы

void loop() {
    if (kostyl1 == true && railRotationServo.tick()) {
        String arg[] = {"moveDone"};
        MessageHandler::sendMessage(MessageHandler::prefix::RAIL,
                                    arg);
        kostyl1 = false;
    }

    if (kostyl4 == true && manipulatorRotationServo.tick()) {
        String arg[] = {"moveDone"};
        MessageHandler::sendMessage(MessageHandler::prefix::RAIL,
                                    arg);
        kostyl4 = false;
    }

    // if (kostyl3 == true && targetGrab == grabServo.read()) {
    //     grabServo.detach();
    //     String arg[] = {"moveDone"};
    //     MessageHandler::sendMessage(MessageHandler::prefix::RAIL,
    //                                 arg);
    //     kostyl3 = false;
    // }

    if(horizontalRailMotor.tick()) {
        Serial.print(NULL);
    }
    else if (kostyl2 == true) {
        String arg[] = {"moveDone"};
        MessageHandler::sendMessage(MessageHandler::prefix::RAIL,
                                    arg);
        kostyl2 = false;
    }

    // verticalRailMotor.stopIfStuck();

    if(wheelBase.checkIfStop() == true) {
        String arg[] = {"moveDone"};
        MessageHandler::sendMessage(MessageHandler::prefix::WHEELS,
                                    arg);
        wheelBase.stop();
    }

    if (Serial.available()) {
        msg = Serial.readStringUntil('\n');

        MessageHandler::processMessage(msg);

        Serial.println(msg);
    }
}

//
// методы класса EncoderMotor
//
void EncoderMotor::movea(float speed, float distance) {
    isMoving = true;

    if (!flagDefaultDirection)
    {
        motor.setSpeed(-speed, MOT_M_S, distance, MOT_MET);
        return;
    }
    motor.setSpeed(speed, MOT_M_S, distance, MOT_MET);
}
void EncoderMotor::stop() {
    this->movea(0, 0);
    motor.delSum();
    isMoving = false;
}
float EncoderMotor::getPosition() {
    return motor.getSum(MOT_MET);
}
float EncoderMotor::getTarget() {
    return motor.getStop(MOT_MET);
}
// void EncoderMotor::setTarget(float position) {
//     targetPosition = position;
// }
// void EncoderMotor::checkAcseleration() {
// }
//
// методы класса WheelMotor
//
void WheelMotor::move(float speed, float distance) {
    this->movea(speed, distance);
}

bool WheelMotor::checkIfStop() {
    // return false;
    return (isMoving == true &&
            this->getTarget() == 0.0f);
}
//
// методы класса VerticalRailMotor
//
void VerticalRailMotor::move(float speed) {
    tempPosition = 0.0f;
    motor.delSum();
    this->movea(speed, -1.0f);
    timer = millis();
}

void VerticalRailMotor::stopIfStuck() {
    if (isMoving == true) {
        if (this->getPosition() == tempPosition) {
            if (millis() - timer > 300) {
                this->stop();
            }
        }
        else {
            tempPosition = this->getPosition();
            timer = millis();
        }
    }
}
//
// методы класса Manipulator
//
void Manipulator::moveManipulator(int manipulatorPosition, int servoDegrees, int manipulatorServoDegrees) {
    this->moveHorizontalRail(manipulatorPosition);
    this->rotateRail(servoDegrees);
    this->rotateManipulator(manipulatorServoDegrees);
}

void Manipulator::rotateRail(int degs) {
    kostyl1 = true;
    railRotationServo.setTargetDeg(degs);
}

void Manipulator::moveHorizontalRail(int position) {
    horizontalRailMotor.setTarget(position);
}

void Manipulator::grab(int rotateServoDegrees, int grabServoDegrees) {
    return;
    this->moveVerticalRail(true);
    this->rotateManipulator(rotateServoDegrees);
}

void Manipulator::moveVerticalRail(float speed) {
    verticalRailMotor.move(speed);
}

void Manipulator::rotateManipulator(int degs) {
    // manipulatorRotationServo.attach(PIN_SERVO_MANIPULATOR_ROTATION);
    // manipulatorRotationServo.write(degs);
    // // manipulatorRotationServo.detach();
    // String arg[] = {"moveDone"};
    // MessageHandler::sendMessage(MessageHandler::prefix::RAIL,
    //                             arg);
    manipulatorRotationServo.setTargetDeg(degs);
    kostyl4 = true;
}

void Manipulator::rotateGrabServo(int degs) {
    grabServo.attach(PIN_SERVO_GRAB, 500, 2400);
    grabServo.write(degs);
    delay(500); // план Б, егор иди нахуй мне похуй нахуй
    grabServo.detach();
    String arg[] = {"moveDone"};
    MessageHandler::sendMessage(MessageHandler::prefix::RAIL,
                                arg);
}

int Manipulator::getGrabServoDegrees() {
    return grabServo.read();
}

int Manipulator::getManipulatorRotationServoDegrees() {
    return manipulatorRotationServo.getCurrent();
}

int Manipulator::getRailRotationServoDegrees() {
    return railRotationServo.getCurrent();
}

int Manipulator::getHorizontalRailMotorPosition() {
    return horizontalRailMotor.getCurrent();
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
    forwardRight.move(-speed, distance);
    forwardLeft.move(speed, distance);
    backwardRight.move(-speed, distance);
    backwardLeft.move(speed, distance);
}

void WheelBase::rotateRight(float speedFR, 
                            float speedFL, 
                            float speedBR, 
                            float speedBL, 
                            float distance) {
    forwardRight.move(-speedFR, distance);
    forwardLeft.move(speedFL, distance);
    backwardRight.move(-speedBR, distance);
    backwardLeft.move(speedBL, distance);
}

void WheelBase::rotateLeft(float speed, float distance) {
    forwardRight.move(speed, distance);
    forwardLeft.move(-speed, distance);
    backwardRight.move(speed, distance);
    backwardLeft.move(-speed, distance);
}

void WheelBase::rotateLeft(float speedFR, 
                           float speedFL, 
                           float speedBR, 
                           float speedBL, 
                           float distance) {
    forwardRight.move(speedFR, distance);
    forwardLeft.move(-speedFL, distance);
    backwardRight.move(speedBR, distance);
    backwardLeft.move(-speedBL, distance);
}

void WheelBase::moveRight(float speed, float distance) {
    forwardRight.move(-speed, distance);
    forwardLeft.move(speed, distance);
    backwardRight.move(speed, distance);
    backwardLeft.move(-speed, distance);
}


void WheelBase::moveRight(float speedFR, 
                            float speedFL, 
                            float speedBR, 
                            float speedBL, 
                            float distance) {
    forwardRight.move(-speedFR, distance);
    forwardLeft.move(speedFL, distance);
    backwardRight.move(speedBR, distance);
    backwardLeft.move(-speedBL, distance);
}

void WheelBase::moveLeft(float speed, float distance) {
    forwardRight.move(speed, distance);
    forwardLeft.move(-speed, distance);
    backwardRight.move(-speed, distance);
    backwardLeft.move(speed, distance);
}


void WheelBase::moveLeft(float speedFR, 
                            float speedFL, 
                            float speedBR, 
                            float speedBL, 
                            float distance) {
    forwardRight.move(speedFR, distance);
    forwardLeft.move(-speedFL, distance);
    backwardRight.move(-speedBR, distance);
    backwardLeft.move(speedBL, distance);
}

void WheelBase::stop() {
    forwardRight.stop();
    forwardLeft.stop();
    backwardRight.stop();
    backwardLeft.stop();
}

bool WheelBase::checkIfStop() {
    // if (millis() - timer > 200) {
    //     timer = millis();
        return (forwardRight.checkIfStop() &&
                forwardLeft.checkIfStop() &&
                backwardRight.checkIfStop() &&
                backwardLeft.checkIfStop());
    // }
    // return false;
}
//
// методы класса MessageHandler
//
void MessageHandler::processMessage(String message) {
    int index;
    String command;
    float arguments[ARGUMENTS_COUNT] = {0};
    
    index = message.indexOf(SEPARATOR);

    command = message.substring(0, index);
    message.remove(0, index+1);

    for (int i = 0; i < ARGUMENTS_COUNT; i++) {
        index = message.indexOf(SEPARATOR);
        if (index != -1) {
            arguments[i] = message.substring(0, index).toFloat();
            message.remove(0, index+1);
        }
        else {
            break;
        }
    }
    
    Serial.println("MessageHandler: " + command);

    MessageHandler::executeCommand(command, arguments);
}

void MessageHandler::executeCommand(String command, float* arguments) {
    //
    // команды для колесной базы
    //
    if (command == "wheelsStop") {
        MessageHandler::wheelBase->stop();
    }
    else if (command == "moveForward") {
        MessageHandler::wheelBase->moveForward(arguments[0],
                                               arguments[1],
                                               arguments[2],
                                               arguments[3],
                                               arguments[4]);
    }
    else if (command == "moveBackward") {
        MessageHandler::wheelBase->moveBackward(arguments[0],
                                                arguments[1],
                                                arguments[2],
                                                arguments[3],
                                                arguments[4]);
    }
    else if (command == "rotateRight") {
        MessageHandler::wheelBase->rotateRight(arguments[0],
                                               arguments[1],
                                               arguments[2],
                                               arguments[3],
                                               arguments[4]);
    }
    else if (command == "rotateLeft") {
        MessageHandler::wheelBase->rotateLeft(arguments[0],
                                              arguments[1],
                                              arguments[2],
                                              arguments[3],
                                              arguments[4]);
    }
    // гетеры колесной базы
    // else if (command == "getWheelsPositions") {
    //     MessageHandler::sendMessage(MessageHandler::prefix::WHEELS, 
    //                                 {forwardRight.getPosition(),
    //                                  forwardLeft.getPosition(),
    //                                  backwardRight.getPosition(),
    //                                  backwardLeft.getPosition()});
    // }
    //
    // команды для движения манипулятора
    //
    else if (command == "moveManipulator") {
        MessageHandler::manipulator->moveManipulator((int)arguments[0], (int)arguments[1]);
    }
    else if (command == "rotateManipulator") {
        MessageHandler::manipulator->rotateManipulator((int)arguments[0]);
    }
    else if (command == "rotateHorizontalRail") {
        MessageHandler::manipulator->rotateRail((int)arguments[0]);
    }
    else if (command == "rotateGrabServo") {
        MessageHandler::manipulator->rotateGrabServo((int)arguments[0]);
    }
    else if (command == "moveHorizontalRail") {
        MessageHandler::manipulator->moveHorizontalRail((int)arguments[0]);
    }
    else if (command == "moveVerticalRail") {
        MessageHandler::manipulator->moveVerticalRail((float)arguments[0]);
    }
    // гетеры манипулятора
    else if (command == "getHorizontalPosition") {
        String args[1] = {String(MessageHandler::manipulator->getHorizontalRailMotorPosition())};
        MessageHandler::sendMessage(MessageHandler::prefix::RAIL,
                                    args);
    }
    else if (command == "getRailServoDegrees") {
        String args[1] = {String(MessageHandler::manipulator->getRailRotationServoDegrees())};
        MessageHandler::sendMessage(MessageHandler::prefix::RAIL,
                                    args);
    }
    else if (command == "getManipulatorServoDegrees") {
        String args[1] = {String(MessageHandler::manipulator->getManipulatorRotationServoDegrees())};
        MessageHandler::sendMessage(MessageHandler::prefix::RAIL,
                                    args);
    }
    else if (command == "getGrabServoDegrees") {
        String args[1] = {String(MessageHandler::manipulator->getGrabServoDegrees())};
        MessageHandler::sendMessage(MessageHandler::prefix::RAIL,
                                    args);
    }
}