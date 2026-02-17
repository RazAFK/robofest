// пример с использованием "внешнего" драйвера, который может быть
// подключен к расширителю портов.

// в качестве примера использую digitalWrite и родные пины
#define PIN_A 2
#define PIN_B 3
#define PIN_C 4

#include <GyverStepper.h>
GStepper<STEPPER2WIRE> stepper(200, PIN_B, PIN_C, PIN_A);

void setup() {
  Serial.begin(9600);
  // выходы
  pinMode(PIN_A, 1);
  pinMode(PIN_B, 1);
  pinMode(PIN_C, 1);
  
  stepper.setRunMode(FOLLOW_POS); // режим поддержания скорости
  stepper.setSpeed(200);       // в шагах/сек
  stepper.setAcceleration(200);

  stepper.autoPower(1);   // включаем авто выкл питания

  stepper.setTarget(200);
}

void loop() {
  stepper.tick();
}
