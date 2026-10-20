#include <Wire.h>
#include <LiquidCrystal_AIP31068_I2C.h>
#include <DHT.h>

#define LED_VIE 13

LiquidCrystal_AIP31068_I2C lcd(0x3E, 16, 2);
DHT dht(A0, DHT22);

int jour = 10, mois = 2, annee = 25;
int heure = 13, minute = 42, seconde = 29;

float t = 0;
float h = 0;

int compteur = 0;   

void deuxChiffres(int valeur)
{
  if (valeur < 10) lcd.print("0");
  lcd.print(valeur);
}

void setup()
{
  Serial.begin(9600);
  pinMode(LED_VIE, OUTPUT);
  dht.begin();
  lcd.init();
}

void loop()
{
  delay(100);
  compteur++;

  if (compteur % 5 < 2) digitalWrite(LED_VIE, HIGH);
  else digitalWrite(LED_VIE, LOW);

  if (compteur % 10 == 0) {
    seconde++;
    if (seconde == 60) { seconde = 0; minute++; }
    if (minute == 60)  { minute = 0;  heure++; }
    if (heure == 24)   { heure = 0;   jour++; }
    if (jour == 31)    { jour = 1;    mois++; }
    if (mois == 13)    { mois = 1;    annee++; }

    lcd.setCursor(0, 0);
    lcd.print(jour);
    lcd.print("/");
    lcd.print(mois);
    lcd.print("/");
    lcd.print(annee);
    lcd.print(" ");
    deuxChiffres(heure);
    lcd.print(":");
    deuxChiffres(minute);
    lcd.print(":");
    deuxChiffres(seconde);
  }

  if (compteur % 20 == 0) {
    t = dht.readTemperature();
    h = dht.readHumidity();

    lcd.setCursor(0, 1);
    lcd.print("T ");
    lcd.print(t, 1);
    lcd.print("oC/H ");
    lcd.print(h, 1);
    lcd.print("%");

    Serial.print(jour);    Serial.print("/");
    Serial.print(mois);    Serial.print("/");
    Serial.print(annee);   Serial.print(" ");
    Serial.print(heure);   Serial.print(":");
    Serial.print(minute);  Serial.print(":");
    Serial.print(seconde);
    Serial.print("  T = ");
    Serial.print(t, 1);
    Serial.print(" C  H = ");
    Serial.print(h, 1);
    Serial.println(" %");
  }

  if (compteur == 100) compteur = 0;
}