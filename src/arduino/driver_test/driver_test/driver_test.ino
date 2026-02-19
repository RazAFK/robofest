#include <Wire.h>
#include <iarduino_I2C_Motor.h>

iarduino_I2C_Motor mot(0x0A); 

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
    mot.begin();
    // Сбрасываем настройки в 1, чтобы видеть "чистые" данные
    mot.setMagnet(7);
    mot.setReducer(94.5);
    mot.changeAddress(0x09);
    Serial.println(mot.getAddress(), HEX);
}

void loop() {
    // Выводим текущее положение в тиках (или оборотах, которые сейчас равны тикам)
    Serial.print("Position: ");
    Serial.println(mot.getSum(MOT_REV));
    mot.setSpeed(100, MOT_RPM, 1, MOT_REV);
    delay(2000);
}
