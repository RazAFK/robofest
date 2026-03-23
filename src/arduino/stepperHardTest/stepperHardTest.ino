// Определяем пины
const int enPin = 1;
const int stepPin = 2; 
const int dirPin = 3; 

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enPin, OUTPUT);
}

void loop() {
  // Движение ВПЕРЕД
  digitalWrite(enPin, LOW);
  digitalWrite(dirPin, LOW); // Устанавливаем направление
  for(int x = 0; x < 200; x++) { // 200 шагов
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1000);    // Скорость (чем меньше пауза, тем быстрее)
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1000);
  }
  digitalWrite(enPin, HIGH);
  
  delay(2000); // Пауза 1 секунда

  // Движение НАЗАД
  digitalWrite(enPin, LOW);
  digitalWrite(dirPin, HIGH);  // Меняем направление
  for(int x = 0; x < 200; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1000);
  }
  digitalWrite(enPin, HIGH);

  delay(2000); // Пауза 1 секунда
}