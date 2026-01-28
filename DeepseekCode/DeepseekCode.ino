#include <Servo.h>
#include <ServoSmooth.h>

// пины платформы
#define PIN_MOT1_PLUS A0
#define PIN_MOT1_MINUS A1
#define PIN_MOT2_PLUS A2
#define PIN_MOT2_MINUS A3
#define PIN_MOT3_PLUS A4
#define PIN_MOT3_MINUS A5
#define PIN_MOT4_PLUS 12
#define PIN_MOT4_MINUS 13

// пины манипулятора
#define PIN_HORSENS A6 // сенсор горизонтального движения
#define PIN_VERSENS A7 // сенсор вертикального движения

class yellowMotor {
  protected:
  int pinPlus;
  int pinMinus;
  static const int pinSpeed = 5;

  public:
  void attach(int plus, int minus) {
    pinPlus = plus;
    pinMinus = minus;
    pinMode(pinPlus, OUTPUT);
    pinMode(pinMinus, OUTPUT);
  }
};

class reykaMotor : public yellowMotor {
  private:
    int pinSensor;
    int movementSpeed;
    int stoppingSpeed;
    int del;
    
    // Переменные для пошагового движения
    int targetSteps = 0;
    int currentSteps = 0;
    bool isMovingForward = true;
    bool isMoving = false;
    
    // Переменные для отслеживания состояния датчика
    bool lastSensorState;
    bool currentSensorState;
    int stepCounter = 0;
    
    // Состояние мотора в текущем шаге
    enum MotorState {
      IDLE,
      START_MOVING,
      MOVING,
      STOPPING,
      FINISHED
    };
    MotorState state = IDLE;

  public:
    void attach(int plus, int minus, int sensor, int msp, int ssp, int d) {
      pinPlus = plus;
      pinMinus = minus;
      pinSensor = sensor;
      movementSpeed = msp;
      stoppingSpeed = ssp;
      del = d;
      
      pinMode(pinPlus, OUTPUT);
      pinMode(pinMinus, OUTPUT);
      pinMode(pinSensor, INPUT);
      
      lastSensorState = analogRead(pinSensor) > 500;
      currentSensorState = lastSensorState;
    }
    
    // Задать цель движения в шагах
    void setTarget(int steps, bool forward) {
      if (steps <= 0) return;
      
      targetSteps = steps;
      currentSteps = 0;
      isMovingForward = forward;
      isMoving = true;
      state = START_MOVING;
      stepCounter = 0;
      
      // Инициализируем состояние датчика
      lastSensorState = analogRead(pinSensor) > 500;
      currentSensorState = lastSensorState;
      
      Serial.print("Setting target: ");
      Serial.print(steps);
      Serial.print(" steps, direction: ");
      Serial.println(forward ? "forward" : "backward");
    }
    
    // Выполнить один шаг движения (вызывать в каждом loop)
    bool step() {
      if (!isMoving || targetSteps <= 0) {
        return false;
      }
      
      bool stepCompleted = false;
      
      switch(state) {
        case START_MOVING:
          // Начинаем движение
          analogWrite(yellowMotor::pinSpeed, movementSpeed);
          
          if (isMovingForward) {
            digitalWrite(pinPlus, HIGH);
            digitalWrite(pinMinus, LOW);
          } else {
            digitalWrite(pinPlus, LOW);
            digitalWrite(pinMinus, HIGH);
          }
          
          state = MOVING;
          break;
          
        case MOVING:
          // Двигаемся и следим за датчиком
          currentSensorState = analogRead(pinSensor) > 500;
          
          // Если состояние датчика изменилось
          if (currentSensorState != lastSensorState) {
            lastSensorState = currentSensorState;
            stepCounter++;
            
            // Если сделали полный шаг (2 изменения состояния)
            if (stepCounter >= 2) {
              stepCounter = 0;
              state = STOPPING;
            }
          }
          break;
          
        case STOPPING:
          // Останавливаем двигатель
          analogWrite(yellowMotor::pinSpeed, stoppingSpeed);
          
          if (!isMovingForward) {
            digitalWrite(pinPlus, HIGH);
            digitalWrite(pinMinus, LOW);
          } else {
            digitalWrite(pinPlus, LOW);
            digitalWrite(pinMinus, HIGH);
          }
          
          delay(del);
          
          // Полностью останавливаем двигатель
          digitalWrite(pinPlus, LOW);
          digitalWrite(pinMinus, LOW);
          analogWrite(yellowMotor::pinSpeed, 0);
          
          currentSteps++;
          stepCompleted = true;
          
          Serial.print("Step ");
          Serial.print(currentSteps);
          Serial.print(" of ");
          Serial.println(targetSteps);
          
          if (currentSteps >= targetSteps) {
            state = FINISHED;
            isMoving = false;
          } else {
            state = START_MOVING;
          }
          break;
          
        case FINISHED:
          // Движение завершено
          digitalWrite(pinPlus, LOW);
          digitalWrite(pinMinus, LOW);
          analogWrite(yellowMotor::pinSpeed, 0);
          isMoving = false;
          stepCompleted = false;
          break;
          
        case IDLE:
          // Ничего не делаем
          break;
      }
      
      return stepCompleted;
    }
    
    // Проверить, выполняется ли движение
    bool isActive() {
      return isMoving;
    }
    
    // Остановить движение
    void stop() {
      digitalWrite(pinPlus, LOW);
      digitalWrite(pinMinus, LOW);
      analogWrite(yellowMotor::pinSpeed, 0);
      isMoving = false;
      state = IDLE;
    }
    
    // Получить прогресс движения (0.0 - 1.0)
    float getProgress() {
      if (targetSteps <= 0) return 0.0;
      return (float)currentSteps / (float)targetSteps;
    }
};

reykaMotor horMotor;
reykaMotor verMotor;

ServoSmooth reykaServo;
ServoSmooth manRotServo;
ServoSmooth manHvatServo;

// Пример использования:
void moveToPosition(int horSteps, bool horForward, int verSteps, bool verForward) {
  if (horSteps > 0) {
    horMotor.setTarget(horSteps, horForward);
  }
  if (verSteps > 0) {
    verMotor.setTarget(verSteps, verForward);
  }
}

void setup() {
  Serial.begin(9600);

  // настройка пинов
  pinMode(PIN_MOT1_PLUS, OUTPUT);
  pinMode(PIN_MOT1_MINUS, OUTPUT);
  pinMode(PIN_MOT2_PLUS, OUTPUT);
  pinMode(PIN_MOT2_MINUS, OUTPUT);
  pinMode(PIN_MOT3_PLUS, OUTPUT);
  pinMode(PIN_MOT3_MINUS, OUTPUT);
  pinMode(PIN_MOT4_PLUS, OUTPUT);
  pinMode(PIN_MOT4_MINUS, OUTPUT);
  pinMode(5, OUTPUT);
  
  // Обратите внимание: я изменил пины на корректные
  horMotor.attach(7, 8, PIN_HORSENS, 100, 30, 50);
  verMotor.attach(4, 9, PIN_VERSENS, 100, 30, 50);

  reykaServo.attach(6, 600, 2400);
  manRotServo.attach(3, 600, 2400); // Примерный пин
  manHvatServo.attach(2, 600, 2400); // Примерный пин

  reykaServo.setSpeed(50);
  reykaServo.setAccel(0.3);
  manRotServo.setSpeed(50);
  manRotServo.setAccel(0.3);
  manHvatServo.setSpeed(50);
  manHvatServo.setAccel(0.3);
  
  reykaServo.setAutoDetach(false);
  manRotServo.setAutoDetach(false);
  manHvatServo.setAutoDetach(false);
  
  Serial.println("System ready!");
  Serial.println("Commands:");
  Serial.println("h100f - horizontal 100 steps forward");
  Serial.println("h50b - horizontal 50 steps backward");
  Serial.println("v30f - vertical 30 steps forward");
  Serial.println("v20b - vertical 20 steps backward");
  Serial.println("s - stop all motors");
}

void loop() {
    // Обработка команд через Serial
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command.length() > 2) {
      char motor = command.charAt(0);
      char direction = command.charAt(command.length() - 1);
      String stepsStr = command.substring(1, command.length() - 1);
      int steps = stepsStr.toInt();
      
      if (steps > 0) {
        switch(motor) {
          case 'h':
            horMotor.setTarget(steps, direction == 'f');
            Serial.print("Horizontal motor: ");
            Serial.print(steps);
            Serial.print(" steps ");
            Serial.println(direction == 'f' ? "forward" : "backward");
            break;
            
          case 'v':
            verMotor.setTarget(steps, direction == 'f');
            Serial.print("Vertical motor: ");
            Serial.print(steps);
            Serial.print(" steps ");
            Serial.println(direction == 'f' ? "forward" : "backward");
            break;
        }
      }
    } else if (command == "s") {
      horMotor.stop();
      verMotor.stop();
      Serial.println("All motors stopped");
    }
    
  // Обработка сервоприводов
  reykaServo.tick();
  manRotServo.tick();
  manHvatServo.tick();
  
  // Выполняем по одному шагу для каждого мотора
  horMotor.step();
  verMotor.step();
  }
  
  delay(10); // Небольшая задержка для стабильности
}
