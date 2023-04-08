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
unsigned long int emerg_vehicle_prev_time;
bool is_coming;


typedef struct {
    double lat;
    double lng;
} Point;

typedef struct {
    int num_points;
    Point* points;
} Polygon;

Point polygon[] = {
      {37.960577, 23.730252},
      {37.960654, 23.730751},
      {37.959852, 23.730482},
      {37.959981, 23.730981}
  };


struct dataStruct{
  double latitude;
  double longitude;
} gpsData;


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

  emerg_vehicle_prev_time = millis();
  
    
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

//          radio.read(&emerg, sizeof(emerg));
          radio.read(&gpsData, sizeof(gpsData));
          emerg = 'b';
          
//          // if gps coords are inside the desired polygon
//          Point p = { gpsData.latitude, gpsData.longitude };
//          int n = sizeof(polygon) / sizeof(Point);
//          
//          if (is_inside_polygon(p, polygon, n)){
//            emerg = 'b';
//          }
//          else {
//            emerg = 'n';
//          }

          if (emerg == 'b') {
            emerg_vehicle_prev_time = millis();

            if (times_sent == 0) {
              Serial.println(emerg);
              times_sent = 1;
             }
           }
  
      }
//        Serial.println(emerg_vehicle_prev_time);
        // if 5 seconds have passed since you last got an indication of emergency
        if (emerg== 'b' && (signed long)(millis() - emerg_vehicle_prev_time) >= 5000) {
          emerg = 'n';
          Serial.println(emerg);
          times_sent = 0;
        }
}


int winding_number(Point p, Point* polygon, int n) {
    int wn = 0;
    for (int i = 0; i < n; i++) {
        Point p1 = polygon[i];
        Point p2 = polygon[(i + 1) % n];
        if (p1.lat <= p.lat) {
            if (p2.lat > p.lat && (p2.lng - p1.lng) * (p.lat - p1.lat) > (p2.lat - p1.lat) * (p.lng - p1.lng)) {
                wn++;
            }
        } else {
            if (p2.lat <= p.lat && (p2.lng - p1.lng) * (p.lat - p1.lat) < (p2.lat - p1.lat) * (p.lng - p1.lng)) {
                wn--;
            }
        }
    }
    return wn;
}

// Checks if the given point is inside the given polygon
int is_inside_polygon(Point p, Point* polygon, int n) {
    int wn = winding_number(p, polygon, n);
    return wn != 0;
}
