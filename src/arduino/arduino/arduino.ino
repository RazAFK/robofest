#define SEPARATOR '#'
#define ARM_PREFIX "data#arm#"
#define WHEELS_PREFIX "data#whe#"

#include <Wire.h>
#include <iarduino_I2C_Motor.h>

iarduino_I2C_Motor mot(0x09);


String message, command, arm_pr = ARM_PREFIX, whe_pr = WHEELS_PREFIX;
int index, args[5], i, stop_list[1]={0};
char sep = SEPARATOR;
bool move_flag = false;
unsigned long start_time = millis(), moving_time = millis();

void executeCommand(String cmd, int args[]) {
  if (cmd == "moveStop") {
    move_flag = false;
    Serial.println(whe_pr+"moveDone");
  }
  else if (cmd == "mf") {
    move_flag = true;
    start_time = millis();
    moving_time = args[0];
    mot.setSpeed(120, MOT_RPM);
  }
  else if (cmd == "command") {
    Serial.println(whe_pr+"command"+String(args[0]));
  }
  else{
    Serial.println("error");
  }
}

void setup() {
  Serial.begin(115200);

  mot.begin(&Wire);
  mot.setMagnet(7);
  mot.setInvGear(false, false);
  mot.setReducer(10.0);
  mot.setStopNeutral(true);
  mot.setError(20);
}

void loop() {
  if (Serial.available()) {
    message = Serial.readStringUntil('\n');
    
    index = message.indexOf(sep);
    command = message.substring(0, index);
    message.remove(0, index+1);
    index = message.indexOf(sep);

    i=0;
    while (index != -1){
      args[i] = message.substring(0, index).toInt();
      message.remove(0, index+1);
      index = message.indexOf(sep);
      i++;
    }
    args[i] = message.toInt();

    Serial.println(command);
    Serial.println(String(args[0])+" "+String(args[1])+" "+String(args[2])+" "+String(args[3])+" "+String(args[4]));

    executeCommand(command, args);
  }

  if (move_flag == true && millis()-start_time >= moving_time){

    executeCommand("moveStop", stop_list);
  }
}