#define PIN_HORSENS A5 // сенсор горизонтального движения
#define PIN_VERSENS A7 // сенсор вертикального движения

int counter = 0;
bool isOpened = false; 
bool lastState;
bool isForward;
float s;

String msg;

int target = 0;

int curPos = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  delay(1000);
  
  pinMode(5, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);

  analogWrite(5, 100);

  digitalWrite(7, LOW);
  digitalWrite(8, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    msg = Serial.readStringUntil('\n');

    if (msg == "get") {
      Serial.print("current == ");
      Serial.println(curPos);
      
      Serial.print("target == ");
      Serial.println(target);

      Serial.print("counter == ");
      Serial.println(counter);
    }
    else if (msg == "clear") {
      counter = 0;
      Serial.println("cleared");
    }
    else {
      target = msg.toInt();
      Serial.println(msg);
    }
  }
  if (curPos != target) {
    lastState = isOpened;
    
    s = analogRead(PIN_HORSENS);
  
    isOpened = s < 500;
  
    isForward = target > curPos;
    
    if (isForward) {
      digitalWrite(7, HIGH);
      digitalWrite(8, LOW);
    }
    else {
      digitalWrite(7, LOW);
      digitalWrite(8, HIGH);
    }
  
    if (isOpened != lastState) {
      counter++;
      if (isForward) {
        curPos++;
      }
      else {
        curPos--;
      }
    }
  }
  else {
    digitalWrite(7, LOW);
    digitalWrite(8, LOW);
  }
    
  delay(10);
}
