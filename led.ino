//IOT Based Flood Monitoring And Alerting System.
#include<LiquidCrystal.h>
LiquidCrystal lcd(2,3,4,5,6,7);

// const int lm35_pin = A0;
const int in=8;
const int out=9;
const int green=10;
const int orange=11;
const int red=12;
const int buzz=13;

void setup(){
  Serial.begin(9600);
  lcd.begin(16,2)
  pinMode(in, INPUT);
  pinMode(out, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(orange, OUTPUT);
  pinMode(red, OUTPUT);
  pinMode(buzz, OUTPUT);
  digitalWrite(green,LOW);
  digitalWrite(orange,LOW);
  digitalWrite(red,LOW);
  digitalWrite(buzz,LOW);
  lcd.setCursor(0,0);
  lcd.print("Flood Monitoring");
  lcd.setCursor(0,1);
  lcd.print("Alerting System");
  delay(5000);
  lcd.clear();
}

void loop()
{
  long dur;
  long dist;
  long per;
  digitalWrite(out,LOW);
  delayMicroseconds(2);
  digitalWrite(out,HIGH);
  delayMicroseconds(10);
  digitalWrite(out,LOW);
  dur=pulseIn(in,HIGH);
  dist=(dur*0.034)/2;
  per=map(dist,10.5,2,0,100);

  int waterLevel = digitalRead(10);
  Serial.println(waterLevel);

  // Read analog voltage from LM35 sensor
  // float voltage = analogRead(lm35_pin) * 5.0 / 1024.0;
    
  // Convert voltage to temperature in degrees Celsius
  // float temperature = voltage * 100.0;
    
  // Send temperature value as a string over serial port
  // Serial.println(String(temperature, 1));
  //map function is used to convert the distance into percentage.
  if(per<0)
  {
    per=0;
  }
  if(per>100)
  {
    per=100;
  }
  Serial.println(String(per));
  lcd.setCursor(0,0);
  lcd.print("Water Level:");
  lcd.print(String(per));
  lcd.print("%  ");
  if(per>=80)       //MAX Level of Water--Red Alert!
  {
    lcd.setCursor(0,1);
    lcd.print("Red Alert!   ");
    digitalWrite(red,HIGH);
    digitalWrite(green,LOW);
    digitalWrite(orange,LOW);
    digitalWrite(buzz,HIGH);
    delay(2000);
    digitalWrite(buzz,LOW);
    delay(2000);
    digitalWrite(buzz,HIGH);
    delay(2000);
    digitalWrite(buzz,LOW);
    delay(2000);
      
  }
  else if(per>=50)    //Intermedite Level of Water--Orange Alert!
  {
    lcd.setCursor(0,1);
    lcd.print("Orange Alert!  ");
    digitalWrite(orange,HIGH);
    digitalWrite(red,LOW);
    digitalWrite(green,LOW);
    digitalWrite(buzz,HIGH);
    delay(3000);
    digitalWrite(buzz,LOW);
    delay(3000);
    
  }
  else          //MIN/NORMAL level of Water--Green Alert!
  {
    lcd.setCursor(0,1);
    lcd.print("Green Alert!  ");
    digitalWrite(green,HIGH); 
    digitalWrite(orange,LOW);
    digitalWrite(red,LOW);
    digitalWrite(buzz,LOW);
  }

  delay(15000);
}