#include "SPI.h"
#include "nRF24L01.h"
#include "RF24.h"

RF24 radio(9, 8);


byte GREEN_PIN = 2;
byte ORANGE_PIN = 3;
byte RED_PIN = 4;
String color;
char emerg = 'n';
int times_sent = 0;
int CHECK_TIMES_FOR_EMERGENCY_VEHICLE = 3;
void setup() {
   Serial.begin(9600);
   pinMode(GREEN_PIN, OUTPUT);
   pinMode(ORANGE_PIN, OUTPUT);
   pinMode(RED_PIN, OUTPUT);
   digitalWrite(GREEN_PIN, HIGH);
   digitalWrite(ORANGE_PIN, LOW);
   digitalWrite(RED_PIN, LOW);

   color = "";
    
  
  //  Setup receiver radio
  radio.begin();
  radio.openReadingPipe(1, 0xF0F0F0F0E1LL);
  radio.setChannel(0x76);
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_250KBPS);
  radio.startListening();
  radio.enableDynamicPayloads();
  radio.powerUp();
}

void loop() {
    if (Serial.available() > 0){
      color = Serial.readStringUntil('\n'); 
//      Serial.println(color);
      Serial.flush();
      Serial.end();   /*end serial communication*/
      Serial.begin(9600);  /*clear serial buffer*/
    }
   
   if (color == "green"){
      digitalWrite(GREEN_PIN, HIGH);
      digitalWrite(ORANGE_PIN, LOW);
      digitalWrite(RED_PIN, LOW);
   }

   if (color == "red"){
      digitalWrite(GREEN_PIN, LOW);
      digitalWrite(ORANGE_PIN, LOW);
      digitalWrite(RED_PIN, HIGH);

   }

   if (color == "orange"){
      digitalWrite(GREEN_PIN, LOW);
      digitalWrite(ORANGE_PIN, HIGH);
      digitalWrite(RED_PIN, LOW);
   }

   
      if (radio.available()){
        radio.read(&emerg, sizeof(emerg));
          if (!times_sent) Serial.println(emerg); // emerg
          ++times_sent;
//          Serial.flush();
//          Serial.end();   /*end serial communication*/
//          Serial.begin(9600);  /*clear serial buffer*/  
        
      }
      else {
        emerg = 'n';
        times_sent = 0;
      }
    
}
