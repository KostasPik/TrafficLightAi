byte GREEN_PIN = 13;
byte ORANGE_PIN = 8;
byte RED_PIN = 2;
String color;

void setup() {
   Serial.begin(9600);
   pinMode(GREEN_PIN, OUTPUT);
   pinMode(ORANGE_PIN, OUTPUT);
   pinMode(RED_PIN, OUTPUT);
   digitalWrite(GREEN_PIN, HIGH);
   digitalWrite(ORANGE_PIN, LOW);
   digitalWrite(RED_PIN, LOW);

   color = "";
}

void loop() {
    if (Serial.available() > 0){
      color = Serial.readStringUntil('\n'); 
      Serial.println(color);
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
}
