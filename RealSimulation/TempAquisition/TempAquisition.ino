#include <Wire.h>
#include <rgb_lcd.h>
#include <DHT.h>

#define LED_VIE 13

rgb_lcd lcd;
DHT dht(A0, DHT22);

float t = 0;
float h = 0;

int compteur = 0;   
bool etatLed = false;

void setup()
{
  pinMode(LED_VIE, OUTPUT);
  dht.begin();

  lcd.begin(16, 2);
  lcd.setRGB(0, 0, 255);   

  lcd.setCursor(2, 0);
  lcd.print("IMT NE - PPI");
}

void loop()
{
  delay(500);
  compteur++;

  etatLed = !etatLed;
  digitalWrite(LED_VIE, etatLed);

  if (compteur % 4 == 0) {
    t = dht.readTemperature();
    h = dht.readHumidity();

    lcd.setCursor(0, 1);
    lcd.print("T ");
    lcd.print(t, 1);
    lcd.print("oC/H ");
    lcd.print(h, 1);
    lcd.print("%");
  }

  if (compteur == 4) compteur = 0;
}