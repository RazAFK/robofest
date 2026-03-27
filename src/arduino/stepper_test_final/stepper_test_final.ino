#define DRIVER_STEP_TIME 4
#include <GyverStepper.h>

GStepper<STEPPER2WIRE> stepper(200, 2, 1, 3);

void setup() {
  Serial.begin(9600);
  stepper.setRunMode(FOLLOW_POS);
  stepper.setMaxSpeed(500);
  stepper.setAcceleration(1000);

  stepper.autoPower(true);

  Serial.println(DRIVER_STEP_TIME);

  stepper.setTarget(200);

  stepper.enable();

  // delay(1000);

  // stepper.setTarget(300);
  // // while (stepper.tick()) {
  // // // Serial.print(stepper.getCurrent());
  // //   delay(50);
  // //   // Serial.println(stepper.getCurrent());
  // //   }
  // // // драйвер автоматически выключится через 1 секунду после остановки
}
uint32_t tmr;
unsigned long lastPrint = 0;
void loop() 
{

    if (!stepper.tick()) {
      static bool dir;
      dir = !dir;
      stepper.setTarget(dir ? -200 : 200);
      delay(1000);
    }
    else {
      Serial.print(NULL);
    }

    // stepper.tick();

    // if (!stepper.getState())
    // {
    //   stepper.setTarget(-200);
    // }

    // // Выводим данные раз в 100 мс
    // if (millis() - lastPrint >= 100) {
    //   lastPrint = millis();
    //   Serial.print("Pos: ");
    //   Serial.println(stepper.pos);
    // }
}