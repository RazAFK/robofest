#include <iarduino_I2C_Software.h>
SoftTwoWire sWire(A4, A5); 

#include <iarduino_I2C_Motor.h>
iarduino_I2C_Motor mot(0x09); // Текущий адрес

void setup() {
    mot.begin(&sWire); // Инициализация на программной шине
    
    // Меняем адрес на 0x0A (диапазон от 0x07 до 0x7F)
    if(mot.changeAddress(0x0D)){
        // Адрес успешно изменен
    }
}

void loop() {}
