#include <ServoDriverSmooth.h>
#include <ServoSmooth.h>
#include <GyverStepper.h>
#include <StepperCore.h>
#include <Wire.h>
#include <iarduino_I2C_Motor.h>

// пины сервы захвата
#define PIN_SERVO_GRAB

// пины сервы поворота клешни
#define PIN_SERVO_ROTATE_MANIPULATOR

// пины сервы поворота горизонтальной рейки
#define PIN_SERVO_ROTATE_RAIL

// пины мотора на горизонтальной рейке
#define PIN_STEPPER_DIR
#define PIN_STEPPER_STEP
#define PIN_STEPPER_ENABLE

// вертикальная рейка
// характеристики мотора
#define ENCODER_MAGNET_COUNT_VERTICAL_RAIL // количество магнитов на энкодере (указывается продавцом)
#define REDUCER_VERTICAL_RAIL              // передаточное число редуктора
#define RADIUS_VERTICAL_RAIL               // радиус колеса на моторе
// опционально обозначить скорости

// I2C адрес мотора вертикальной рейки
#define ADDRESS_VERTICAL_RAIL_MOTOR

// колесная база
// характеристики моторов (на колесной базе они одинаковые)
#define ENCODER_MAGNET_COUNT_WHEELS // количество магнитов на энкодере (указывается продавцом)
#define REDUCER_WHEELS              // передаточное число редуктора
#define RADIUS_WHEELS               // радиус колеса на моторе
// опционально обозначить скорости

// I2C адреса колес
#define ADDRESS_FORWARD_RIGHT
#define ADDRESS_FORWARD_LEFT
#define ADDRESS_BACKWARD_RIGHT
#define ADDRESS_BACKWARD_LEFT

class EncoderMotor {
    iarduino_I2C_Motor motor;

    public:
    EncoderMotor(int I2CAddress, float reducer, float wheelRadius) : 
        motor(new iarduino_I2C_Motor(I2CAddress))
    { 
        motor.setReducer(reducer);
        motor.radius = wheelRadius;
    }

    void move(int speed, int time);
    void stop();

    void move(int speed, int time) {

    }

    void stop() {
        this->move(0, 0);
    }
};

class Rail {
    Servo grabServo;
    Servo rotateManipulatorServo;
    ServoSmooth rotateRailServo;
    GStepper<STEPPER2WIRE> horizontalRailMotor;
    EncoderMotor verticalRailMotor;

    public:
    Rail(Servo grabServo, Servo rotateManipulatorServo, ServoSmooth rotateRailServo, GStepper<STEPPER2WIRE> horizontalRailMotor, EncoderMotor verticalRailMotor) :
        grabServo(grabServo),
        rotateManipulatorServo(rotateManipulatorServo),
        rotateRailServo(rotateRailServo),
        horizontalRailMotor(horizontalRailMotor),
        verticalRailMotor(verticalRailMotor) 
    { }

    // движение манипулятора в горизонтальной плоскости
    void moveManipulator(int manipulatorPosition, int servoDegrees);
    void moveHorizontalRail(int position);
    void rotateRail(int degrees);

    // движение манипулятора в вертикальной плоскости
    void grab(int position, int rotateServoDegrees, int grabServoDegrees);
    void moveVerticalRail(int position);
    void rotateManipulator(int degrees);
    void grabManipulator(int degrees);
};

void setup () {

}

void loop() {
    
}