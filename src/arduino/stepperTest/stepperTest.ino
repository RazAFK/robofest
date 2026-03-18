// пример с использованием "внешнего" драйвера, который может быть
// подключен к расширителю портов.

// в качестве примера использую digitalWrite и родные пины
#define PIN_STEPPER_DIR 3
#define PIN_STEPPER_STEP 2
#define PIN_STEPPER_ENABLE 1
#define STEPPER_STEPS_PER_ROUND 200

#include <GyverStepper.h>
GStepper<STEPPER2WIRE> stepper(STEPPER_STEPS_PER_ROUND, 
                                           PIN_STEPPER_STEP, 
                                           PIN_STEPPER_DIR, 
                                           PIN_STEPPER_ENABLE);
void setup() {
    Serial.begin(9600);
    // выходы
    pinMode(PIN_STEPPER_DIR, OUTPUT);
    pinMode(PIN_STEPPER_ENABLE, OUTPUT);
    pinMode(PIN_STEPPER_STEP, OUTPUT);
    
    stepper.setRunMode(FOLLOW_POS); // режим поддержания скорости
    stepper.setSpeed(200);       // в шагах/сек
    stepper.setAcceleration(200);

    stepper.autoPower(1);   // включаем авто выкл питания

    stepper.setTarget(200);
}

void loop() {
  stepper.tick();
}
