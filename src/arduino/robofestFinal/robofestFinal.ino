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

#define SEPARATOR '#'

// пины сервы захвата
#define PIN_SERVO_GRAB 7

// пины сервы поворота клешни
#define PIN_SERVO_MANIPULATOR_ROTATION 6

// пины сервы поворота горизонтальной рейки
#define PIN_SERVO_RAIL_ROTATION 4

// пины мотора на горизонтальной рейке
#define PIN_STEPPER_DIR 3
#define PIN_STEPPER_STEP 2
#define PIN_STEPPER_ENABLE 1
#define STEPPER_STEPS_PER_ROUND 200 // количество шагов для 1 оборота

// вертикальная рейка
// характеристики мотора
#define ENCODER_MAGNET_COUNT_VERTICAL_RAIL 1 // количество магнитов на энкодере (указывается продавцом)
#define REDUCER_VERTICAL_RAIL 48

// передаточное число редуктора
#define RADIUS_VERTICAL_RAIL 30.0            // радиус колеса на моторе
#define SPEED_VERTICAL_RAIL 0.5f
// опционально обозначить скорости

// полярность (направление) мотора
#define VERTICAL_RAIL_MOTOR_DEFAULT_DIRECTION true

// I2C адрес мотора вертикальной рейки
#define ADDRESS_VERTICAL_RAIL_MOTOR 0x0B

// колесная база
// характеристики моторов (на колесной базе они одинаковые)
#define ENCODER_MAGNET_COUNT_WHEELS 12       // количество магнитов на энкодере (указывается продавцом)
#define ENCODER_MAGNET_COUNT_BROKEN_WHEEL 12 // одно колесо поломанное вообще 11.7
#define REDUCER_WHEELS 51.6                  // передаточное число редуктора
#define RADIUS_WHEELS 50.0                   // радиус колеса на моторе
// опционально обозначить скорости

// полярности (направления) колес
#define WHEEL_DEFAULT_DIRECTION_FORWARD_RIGHT true
#define WHEEL_DEFAULT_DIRECTION_FORWARD_LEFT true
#define WHEEL_DEFAULT_DIRECTION_BACKWARD_RIGHT true
#define WHEEL_DEFAULT_DIRECTION_BACKWARD_LEFT false

// I2C адреса колес
#define ADDRESS_FORWARD_RIGHT 0x0D
#define ADDRESS_FORWARD_LEFT 0x0C
#define ADDRESS_BACKWARD_RIGHT 0x09
#define ADDRESS_BACKWARD_LEFT 0x0A

class EncoderMotor {
    iarduino_I2C_Motor motor;

    int flagDefaultDirection;

    int timer = 0;

    // bool isMoving = false;

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

    void move(float speed = 0, float distance = 0);
    bool checkIfStuck();
    int getPosition();
    void stop();
};

class Manipulator {
    Servo& grabServo;
    Servo& manipulatorRotationServo;
    ServoSmooth& railRotationServo;
    GStepper<STEPPER2WIRE>& horizontalRailMotor;
    EncoderMotor& verticalRailMotor;

    public:
    Manipulator(Servo& grabServo, 
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
    void grab(int rotateServoDegrees = 90, int grabServoDegrees = 0);
    void moveVerticalRail(bool flagIfUp);
    void rotateManipulator(int degs);
    void grabManipulator(int degs);

    // todo: написать гетеры для позиций всех компонентов
    int getRailRotationServoDegrees();
    int getManipulatorRotationServoDegrees();
    int getGrabServoDegrees();
    int getHorizontalRailMotorPosition();

    bool checkIfStuck();
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

    bool checkIfStuck();
    void stop();

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
        String processedMessage = prefixes[DATA] + separator +
                                  prefixes[p] + separator;
        for (int i = 0; i < sizeof(messageArguments); i++) {
            processedMessage += messageArguments[i] + separator;
        }
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
                               VERTICAL_RAIL_MOTOR_DEFAULT_DIRECTION);

Manipulator manipulator(grabServo, 
          manipulatorRotationServo, 
          railRotationServo, 
          horizontalRailMotor, 
          verticalRailMotor);

EncoderMotor forwardRight(ADDRESS_FORWARD_RIGHT, 
                          ENCODER_MAGNET_COUNT_WHEELS,
                          REDUCER_WHEELS,
                          RADIUS_WHEELS,
                          WHEEL_DEFAULT_DIRECTION_FORWARD_RIGHT);
EncoderMotor forwardLeft(ADDRESS_FORWARD_LEFT, 
                         ENCODER_MAGNET_COUNT_BROKEN_WHEEL,
                         REDUCER_WHEELS,
                         RADIUS_WHEELS,
                         WHEEL_DEFAULT_DIRECTION_FORWARD_LEFT);
EncoderMotor backwardRight(ADDRESS_BACKWARD_RIGHT, 
                           ENCODER_MAGNET_COUNT_WHEELS,
                           REDUCER_WHEELS,
                           RADIUS_WHEELS,
                           WHEEL_DEFAULT_DIRECTION_BACKWARD_RIGHT);
EncoderMotor backwardLeft(ADDRESS_BACKWARD_LEFT, 
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

    sWire.begin();

    delay(1000); // китенок сказал для стабилизации надо

    Serial.println("wire has began");

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
    horizontalRailMotor.enable();

    grabServo.attach(PIN_SERVO_GRAB);
    manipulatorRotationServo.attach(PIN_SERVO_MANIPULATOR_ROTATION);

    forwardRight.begin(&sWire);
    forwardLeft.begin(&sWire);
    backwardRight.begin(&sWire);
    backwardLeft.begin(&sWire);
    // verticalRailMotor.begin(&sWire);

    MessageHandler::setWheelBase(wheelBase);
    MessageHandler::setManipulator(manipulator);

    // verticalRailMotor.move(-0.1, 0.1);

    // railRotationServo.setTargetDeg(90);

    horizontalRailMotor.setTarget(1000);
}

String msg; // буфер для полученных сообщений

void loop() {
    railRotationServo.tick();
    horizontalRailMotor.tick();

    if (Serial.available()) {
        msg = Serial.readStringUntil('\n');

        MessageHandler::processMessage(msg);

        Serial.println(msg);
    }
}

//
// методы класса EncoderMotor
//
void EncoderMotor::move(float speed, float distance) {
    motor.delSum();
    if (!flagDefaultDirection)
    {
        motor.setSpeed(-speed, MOT_M_S, distance, MOT_MET);
        return;
    }
        motor.setSpeed(speed, MOT_M_S, distance, MOT_MET);
}

void EncoderMotor::stop() {
    this->move(0, 0);
}

int EncoderMotor::getPosition() {
    return motor.getSum(MOT_MET);
}

bool EncoderMotor::checkIfStuck() {
    if (millis() - timer > 500) {
        this->stop();
    }
    timer = millis();
}
//
// методы класса Manipulator
//
void Manipulator::moveManipulator(int manipulatorPosition, int servoDegrees) {
    this->moveHorizontalRail(manipulatorPosition);
    this->rotateRail(servoDegrees);
}

void Manipulator::rotateRail(int degs) {
    railRotationServo.setTargetDeg(degs);
}

void Manipulator::moveHorizontalRail(int position) {
    horizontalRailMotor.setTarget(position, ABSOLUTE);
}

void Manipulator::grab(int rotateServoDegrees, int grabServoDegrees) {
    this->moveVerticalRail(true);
    this->rotateManipulator(rotateServoDegrees);
}

void Manipulator::moveVerticalRail(bool flagIfUp) {
    verticalRailMotor.move(SPEED_VERTICAL_RAIL * flagIfUp, MOT_M_S);
}

void Manipulator::rotateManipulator(int degs) {
    manipulatorRotationServo.write(degs);
}

void Manipulator::grabManipulator(int degs) {
    grabServo.write(degs);
}

int Manipulator::getGrabServoDegrees() {
    return grabServo.read();
}

int Manipulator::getManipulatorRotationServoDegrees() {
    return manipulatorRotationServo.read();
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
// методы класса MessageHandler
//
void MessageHandler::processMessage(String message) {
    int index;
    String command;
    float arguments[ARGUMENTS_COUNT] = {0};
    
    index = message.indexOf(separator);

    command = message.substring(0, index);
    message.remove(0, index+1);

    for (int i = 0; i < ARGUMENTS_COUNT; i++) {
        index = message.indexOf(separator);
        if (index != -1) {
            arguments[i] = message.substring(0, index).toFloat();
            message.remove(0, index+1);
        }
        else {
            break;
        }
    }

    MessageHandler::executeCommand(command, arguments);
}

void MessageHandler::executeCommand(String command, float* arguments) {
    //
    // команды для колесной базы
    //
    if (command == "stop") {
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
    // else if (command == "getWheelsPositions") {
    //     MessageHandler::sendMessage(MessageHandler::prefix.WHEELS, 
    //                                 {forwardRight.getPosition(),
    //                                  forwardLeft.getPosition(),
    //                                  backwardRight.getPosition(),
    //                                  backwardLeft.getPosition()});
    // }
    //
    // команды для движения рейки
    //
    else if (command == "moveManipulator") {
        MessageHandler::manipulator->moveManipulator((int)arguments[0], (int)arguments[1]);
    }
    else if (command == "rotateManipulator") {
        MessageHandler::manipulator->rotateManipulator((int)arguments[0]);
    }
}