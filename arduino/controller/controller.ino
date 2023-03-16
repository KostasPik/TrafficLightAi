unsigned long int prev_time;
bool extended_time;
unsigned long int additional_time;
String heavy;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  extended_time = false;
  prev_time = millis();
  additional_time = 0;
  heavy="";
}

void loop() {
//  Serial.println(digitalRead(13));
  if(Serial.available() > 0 && digitalRead(13) == HIGH && digitalRead(2) == LOW && digitalRead(8) == LOW && !extended_time) {
    heavy = Serial.readStringUntil('\n');
    if (heavy == "heavy"){
      extended_time = true;
      heavy="";
      additional_time = 4000;
      Serial.println((signed long)(millis() - additional_time - prev_time));
    }
  }
  if (digitalRead(13) == HIGH && (signed long)(millis() - additional_time - prev_time) >= 5000 ) { // 5 sec green
    digitalWrite(13, LOW); // make green turn off
    digitalWrite(2, LOW);
    digitalWrite(8, HIGH); // turn orange on
    prev_time = millis();
    extended_time = false;
    heavy="";
    additional_time = 0;
    Serial.flush();
    Serial.end();   /*end serial communication*/
    Serial.begin(9600);  /*clear serial buffer*/

  }

  if (digitalRead(8) == HIGH && (signed long)(millis()- additional_time - prev_time) >= 2000) {
       digitalWrite(8, LOW); 
       digitalWrite(13, LOW);
       digitalWrite(2, HIGH);
       prev_time = millis();
       extended_time = false;
       heavy="";
       additional_time = 0;
    Serial.flush();
    Serial.end();   /*end serial communication*/
    Serial.begin(9600);  /*clear serial buffer*/

  }

    if (digitalRead(2) == HIGH && (signed long)(millis()- additional_time - prev_time) >= 5000) {
      digitalWrite(2, LOW); 
      digitalWrite(8, LOW);
      digitalWrite(13, HIGH);
      prev_time = millis();
      extended_time = false;
      heavy="";
      additional_time = 0;
      Serial.flush();
      Serial.end();   /*end serial communication*/
      Serial.begin(9600);  /*clear serial buffer*/
  }


  
}
