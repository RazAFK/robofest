#define SEPARATOR '#'
#define ARM_PREFIX "data#arm#"
#define WHEELS_PREFIX "data#whe#"
#define ALL_PREFIX "data#all#"


String message, command, arm_pr = ARM_PREFIX, whe_pr = WHEELS_PREFIX, all_pr = ALL_PREFIX;
int index, args[5], i, stop_list[1]={0};
char sep = SEPARATOR;
bool move_flag = false;
unsigned long start_time = millis(), moving_time = millis();

void executeCommand(String cmd, int args[]) {
  if (cmd == "Stop") {
    Serial.println(all_pr+"Stop");
  }
  else if (cmd == "moveStop") {
    move_flag = false;
    Serial.println(whe_pr+"moveDone");
  }
  else if (cmd == "moveStop") {
    Serial.println(whe_pr+"moveDone");
  }
  else if (cmd == "moveForward") {
    move_flag = true;
    start_time = millis();
    moving_time = args[0];
  }
}

void setup() {
  Serial.begin(115200);
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