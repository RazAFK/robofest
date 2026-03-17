// Определяем пины
const int stepPin = 2; 
const int dirPin = 1; 

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

void loop() {
  // Движение ВПЕРЕД
  digitalWrite(dirPin, HIGH); // Устанавливаем направление
  for(int x = 0; x < 200; x++) { // 200 шагов
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1000);    // Скорость (чем меньше пауза, тем быстрее)
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1000);
  }
  
  delay(1000); // Пауза 1 секунда

  // Движение НАЗАД
  digitalWrite(dirPin, LOW);  // Меняем направление
  for(int x = 0; x < 200; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1000);
  }

  delay(1000); // Пауза 1 секунда
}
