#include <Wire.h>
#include "nunchuck_funcs.h"

byte accx,accy,zbut,cbut;
int loop_cnt=0;
unsigned long currentMillis, startMillis;
unsigned long interval = 2000;
int ledPin = 13;

void setup()
{
  Serial.begin(9600);
  nunchuck_setpowerpins();
  nunchuck_init(); // send the initilization handshake
}

void loop()
{
  currentMillis = millis();
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if(incomingByte == 'B'){
      startMillis = millis();
    }
    Serial.print("I received: ");
    Serial.println(incomingByte, DEC);
    Serial.flush();
  }

  if(currentMillis - startMillis < interval){
    digitalWrite(ledPin, LOW);
  }else{
    digitalWrite(ledPin, HIGH);
  }
  
  // every 100 msecs get new data
  if( loop_cnt > 100 ) 
  { 
    loop_cnt = 0;

    nunchuck_get_data();

    accx  = nunchuck_accelx();
    accy  = nunchuck_accely();
    zbut = nunchuck_zbutton();
    cbut = nunchuck_cbutton(); 

    sendRawData();
  }
  loop_cnt++;
  delay(1);

}


void sendRawData()
{
  Serial.print((byte)accx,DEC);
  Serial.print(" ");
  Serial.print((byte)accy,DEC);
  Serial.print(" ");
  Serial.println((byte)zbut,DEC);
  //Serial.print(" ");
  //Serial.println((byte)cbut,DEC);

}


