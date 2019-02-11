int led1  =  2; int led2 = 3; int led3 = 4;     //use digital I/O pin 8
int val = 0;int LastPort = 2;

void setup() {
  // put your setup code here, to run once:
pinMode(led1,OUTPUT);   //set pin 8 to be an output output
pinMode(led2,OUTPUT);   //set pin 8 to be an output output
pinMode(led3,OUTPUT);   //set pin 8 to be an output output
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
 
   digitalWrite(led1,HIGH);   //set pin 8 HIGH, turning on LED
   digitalWrite(led2,LOW);   //set pin 8 HIGH, turning on LED
//   digitalWrite(led3,LOW);    //set pin 8 LOW, turning off LED
//   delay(1000);          //delay 1000 milliseconds 
for (int CycleNum=0;CycleNum<100;CycleNum++)
{
 for (int PortNum =0; PortNum < LastPort; PortNum++)
  {
    val = analogRead(PortNum);
    Serial.print(val);
    Serial.print(", ");
    delay(10);
    }
    val = analogRead(LastPort);
    Serial.println(val);   
}
   digitalWrite(led1,LOW);    //set pin 8 LOW, turning off LED
   digitalWrite(led2,HIGH);    //set pin 8 LOW, turning off LED
//   digitalWrite(led3,HIGH);    //set pin 8 LOW, turning off LED
//   delay(1000);          //delay 1000 milliseconds 
for (int CycleNum=0;CycleNum<100;CycleNum++)
{
 for (int PortNum =0; PortNum < LastPort; PortNum++)
  {
    val = analogRead(PortNum);
    Serial.print(val);
    Serial.print(", ");
    delay(10);
    }
    val = analogRead(LastPort);
    Serial.println(val);
}
}
