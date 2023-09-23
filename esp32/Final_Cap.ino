//HTTPs
//Change this according to your IPv4 : "http://xxx.xxx.xxx.xxx:5000//data"
const char* URL = "http://192.168.2.7:5000//data";
//
#include<ArduinoJson.h>
#include "time.h"
#include <Adafruit_SSD1306.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <driver/adc.h>
#include<HTTPClient.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define I2C_SDA 22
#define I2C_SCL 21

Adafruit_SSD1306 oled(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
#define OLED_Address 0x3C


//const char* ssid     ="POCO M5";
//const char* password = "duykhanh";
//////////////////////////
//Wifi corresponding
const char *ssid = "O2_108";
const char* password = "O2.108wifi";

const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 6*3600;
const int   daylightOffset_sec = 3600;

//const int but = 23;
#define but 23
#define si 3000
//const uint8_t but = 23;
//const uint16_t si = 3000;
//const int si = 3000;
//int arr[si];

uint16_t sample;
uint8_t Rpeak;

int lastState = HIGH; // the previous state from the input pin
int currentState;    // the current reading from the input pin
char datetime[50];

bool flag;
uint8_t lastDebounceTime = 0;
uint8_t debounceDelay = 500; 

uint32_t count;
uint32_t now;

void setup(){
  pinMode(but, INPUT_PULLUP);
  //pinMode(A0, INPUT);
  adc1_config_width(ADC_WIDTH_BIT_12);
  adc1_config_channel_atten(ADC1_CHANNEL_0, ADC_ATTEN_DB_11);
  //adc1_ulp_enable();
  Serial.begin(9600);

  oled.begin(SSD1306_SWITCHCAPVCC, OLED_Address);
  oled.clearDisplay();
  
  oled.setTextSize(2);
  oled.setTextColor(WHITE, BLACK);
  oled.setCursor(0, 0);
  oled.println("DEVICE");
  oled.setCursor(0, 20);
  oled.println("IS ON");
  oled.display();
  delay(500);
  oled.clearDisplay();
  delay(500);

  // Connect to Wi-Fi
  oled.setCursor(0, 0);
  oled.print("Connecting");
  oled.println(ssid);
  oled.display();
  delay(500);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    oled.clearDisplay();
    oled.setCursor(0, 0);
    oled.print(".");
    oled.display();
  }
  Serial.println("");
  oled.clearDisplay();
  oled.setCursor(0, 0);
  oled.println("WiFi connected.");
  oled.display();
  delay(500);
  oled.clearDisplay();
  // Init and get the time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
}

void loop(){
  currentState = digitalRead(but); 
  
  if(lastState == LOW && currentState == HIGH){
    if ( (millis() - lastDebounceTime) > debounceDelay) {
    oled.clearDisplay();
    flag = 1;
    Serial.println("The button is pressed");
    oled.setCursor(0, 0);
    //oled.print("The button is pressed");
    oled.print("Proceed");
    oled.display(); 
    delay(1000);
    oled.clearDisplay();
    mainfunction();
  }
  lastDebounceTime = millis();
  }
  if(flag){
    flag = 0;
    lastDebounceTime = 0;
  }
  lastState = currentState;
  //oled.clearDisplay();
  oled.setCursor(0, 0);
  oled.print("Press BUT");
  oled.display();
  delay(500);
}
 
void mainfunction(){
  int* arr = (int*)malloc(si* sizeof(int));
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    //datetime = strcpy(datetime, "Failed to obtain time");
    //datetime = "Failed to obtain time";
    oled.setCursor(0, 0);
    oled.println("Can not");
    oled.setCursor(0, 20);
    oled.println("get time");
    return;
  }
  //Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
  strftime(datetime, 50, "%A %B/%d/%Y %H:%M:%S", &timeinfo);
  oled.setCursor(0, 0);
  oled.println(&timeinfo,"%A");

  oled.setCursor(0, 20);
  oled.println(&timeinfo,"%B/%d");
  oled.setCursor(0, 40);
  oled.println(&timeinfo,"%H:%M:%S");
  
  Rpeak = 0;
  sample = 0;
  
  oled.display();
  delay(3000);
  oled.clearDisplay();
  
    now = millis();
    oled.setTextColor(WHITE);
    oled.setCursor(0, 0);
    oled.print("Recording");
    oled.display();
    while(millis()-now <= 12000){
      arr[sample] = analogRead(A0);
      //arr[sample] = adc1_get_raw(ADC1_CHANNEL_0);
      //Serial.println(arr[sample]);
    sample++;
    delay(6.5);
    }
    Rpeak = CountRpeak(arr, sample);
    
    oled.clearDisplay();
    //oled.setCursor(0, 0);
    count = millis() - now;
    //oled.print("time=");
    //oled.println((int) count/1000);
    //oled.print("sample=");
    //oled.println(sample);
    float sampa = (float) sample/count*1000;
    int sampling = (int) sampa;
    //oled.print("sampling=");
    //oled.println(sampling);
    //oled.print("Rpeak=");
    //oled.println(Rpeak);
    
    //oled.display();
    delay(2000);
    //oled.clearDisplay();
    if(Rpeak >= 10 && Rpeak <= 20){
      const size_t CAPACITY = JSON_ARRAY_SIZE(sample) + JSON_OBJECT_SIZE(1);
      DynamicJsonDocument doc(CAPACITY);
      doc["time"] = datetime;
      JsonArray ECGsignal = doc.createNestedArray("ECGsignal");

      //for(int j=0;j<sample-5;j++){
      for(int j=100;j<sample-5;j++){
        //doc["ECGsignal"][i] = arr[i];
        ECGsignal.add(arr[j]);
      }
      ECGsignal.add(sampling);
      String json;
      serializeJson(doc, json);
      //serializeJson(doc, Serial);
      oled.setCursor(0, 0);
      oled.println("Json file");
      oled.setCursor(0, 20);
      oled.println("is created");
      oled.display();
      delay(2000);
      oled.clearDisplay();

      if (WiFi.status() == WL_CONNECTED) { 
        HTTPClient http;
        WiFiClient client;
        //http.begin("http://192.168.128.124:5000//data"); //URL = "http://192.168.128.124:5000//data"
        http.begin(URL); //URL = "http://192.168.128.124:5000//data"
        http.addHeader("Content-Type", "application/json"); 
        
        int httpCode = http.POST(json);                        
 
      if (httpCode > 0) {
        String payload = http.getString();
        //oled.setCursor(0, 0);
        //oled.println(httpCode);
        //oled.display();
        //delay(2000);
        //oled.clearDisplay();
        
        Serial.println(httpCode);
        if(httpCode <=300){
          oled.setCursor(0, 0);
          oled.println("Predict:");
          oled.setCursor(0,20);
          oled.println(payload);
          Serial.println(payload);
        }
        
        oled.display();
        delay(5000);
        oled.clearDisplay();
        }
 
       else {
         oled.setCursor(0, 0);
         oled.println("Error HTTP");

         oled.setCursor(0, 20);
         oled.println(httpCode);
         oled.display();
         delay(3000);
         oled.clearDisplay();
        }

       http.end();
       }
          
    doc.clear();
    }
    
    else{
      oled.setCursor(0, 0);
      oled.println("Error on");
      oled.setCursor(0, 20);
      oled.println("Record!!");
      oled.setCursor(0, 40);
      oled.println("Try again");
      oled.display();
      delay(3000);
      oled.clearDisplay();
      }
  
  free(arr);
}

uint8_t CountRpeak(int arr[], int sample){
  uint8_t PeakCount = 0;
  //int i, j, k;
  uint16_t i, j, k;

  for(i=100;i<sample;i++){
    if(i<sample-5)
      j = i + 5;
    else
      j = i;
    if(i>5)
      k = i - 5;
    else 
      k = i;
    if(arr[i] > arr[j]+1500 && arr[i] > arr[k]+1500 && arr[i]>= 3500){
      PeakCount++;
      i = i+8;
    }
  }
  
  return PeakCount;
}
