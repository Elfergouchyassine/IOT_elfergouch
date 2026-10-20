#include <Wire.h>
#include <LiquidCrystal_AIP31068_I2C.h>
#include <DHT.h>

#define PIN_DHT   A0
#define TYPE_DHT  DHT22

LiquidCrystal_AIP31068_I2C lcd(0x3E, 16, 2);
DHT dht(PIN_DHT, TYPE_DHT);

void setup()
{
  lcd.init();
  dht.begin();

  lcd.setCursor(2, 0);          
  lcd.print("IMT NE - PPI");
}

void loop()
{
  delay(2000);                 

  float t = dht.readTemperature();
  float h = dht.readHumidity();

  lcd.setCursor(0, 1);

  if (isnan(t) || isnan(h)) {
    lcd.print("Erreur capteur  ");
    return;
  }

  lcd.print("T ");
  lcd.print(t, 1);              
  lcd.print("oC/H ");
  lcd.print(h, 1);
  lcd.print("%");
}