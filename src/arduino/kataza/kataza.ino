#include <iarduino_I2C_Software.h>
SoftTwoWire sWire(A4, A5);

#include <iarduino_I2C_Motor.h>

// iarduino_I2C_Motor mot_test(0x09);
iarduino_I2C_Motor mot1(0x0D);
// iarduino_I2C_Motor mot2(0x0B);
// iarduino_I2C_Motor mot3(0x0C);
// iarduino_I2C_Motor mot4(0x0D);

void setup() {
    Serial.begin(9600);
    sWire.begin();

    // mot_test.begin(&sWire);

    // mot_test.setReducer(7);
    // mot_test.setMagnet(56);

    // mot_test.setSpeed(-60, MOT_RPM, 3, MOT_REV);

    mot1.begin(&sWire);
    // mot2.begin(&sWire);
    // mot3.begin(&sWire);
    // mot4.begin(&sWire);
    
    mot1.setReducer(56);
    mot1.setMagnet(7);

    // mot2.setReducer(56);
    // mot2.setMagnet(7);
    
    // mot3.setReducer(56);
    // mot3.setMagnet(7);
    
    // mot4.setReducer(56);
    // mot4.setMagnet(7);

    Serial.println("bebebe");

    mot1.setSpeed(-60, MOT_RPM, 3, MOT_REV);
    // mot2.setSpeed(60, MOT_RPM, 3, MOT_REV);
    // mot3.setSpeed(60, MOT_RPM, 3, MOT_REV);
    // mot4.setSpeed(-60, MOT_RPM, 3, MOT_REV);

    
    Serial.println("bububu");

}

void loop() {
}
