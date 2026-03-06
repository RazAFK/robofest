#include <Wire.h>
#include <iarduino_I2C_Motor.h>

iarduino_I2C_Motor motA(0x0A);
iarduino_I2C_Motor motB(0x0B);
iarduino_I2C_Motor motC(0x0C);
iarduino_I2C_Motor motD(0x0D);

// // Параметры вашего мотора
// const float REDUCER = 99.0;
// const float MAGNETS = 7.0;
// const float WHEEL_RADIUS_CM = 3.0; // Ваш радиус в см

// void setup() {
//     mot.begin();
//     mot.setMagnet(MAGNETS);
//     mot.setReducer(REDUCER);
//     mot.radius = WHEEL_RADIUS_CM;
// }

// void loop() {
//     // 1. Проехать 5 оборотов
//     mot.setSpeed(100, MOT_RPM, 1, MOT_REV);
//     delay(2000);
    
//     // mot.setSpeed(70, MOT_RPM, 5, MOT_SEC);
//     // delay(5000);
// }

void setup() {
    Serial.begin(9600);
    motA.begin();
    motB.begin();
    motC.begin();
    motD.begin();
    
    motA.setMagnet(13);
    motB.setMagnet(13);
    motC.setMagnet(9);
    motD.setMagnet(13);
    
    motA.setReducer(39.5f);//A 71 B 72 C 81.5f D 71
    motB.setReducer(39.5f);//A 71 B 72 C 81.5f D 71
    motC.setReducer(39.5f);//A 71 B 72 C 81.5f D 71
    motD.setReducer(39.5f);//A 71 B 72 C 81.5f D 71
    // mot.radius = 50.0f;
    motA.setSpeed(60, MOT_RPM, 2, MOT_REV);
    motB.setSpeed(-60, MOT_RPM, 2, MOT_REV);
    motC.setSpeed(-60, MOT_RPM, 2, MOT_REV);
    motD.setSpeed(-60, MOT_RPM, 2, MOT_REV);
}

void loop() {
    // Выводим текущее положение в тиках (или оборотах, которые сейчас равны тикам)
    Serial.print("Position: ");
    Serial.println(motA.getSum(MOT_REV));
    // mot.setSpeed(100, MOT_RPM, 1, MOT_REV);
    // delay(2000);
}
