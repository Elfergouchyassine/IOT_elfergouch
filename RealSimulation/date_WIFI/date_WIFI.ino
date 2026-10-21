#include <Wire.h>
#include <rgb_lcd.h>
#include <DHT.h>
#include "RTC.h"
#include <WiFiS3.h>
#include <WiFiUdp.h>
#include <NTPClient.h>

#define LED_VIE 13
#define VERSION "V1.0"

char ssid[] = "IoT IMT Nord Europe";
//char ssid[] = "IoT IMT Nord Europe 5G";
char pass[] = "72Hin@R*";

WiFiUDP udp;
NTPClient ntp(udp, IPAddress(192, 168, 1, 254), 7200);  // +2h ete, 3600 hiver

rgb_lcd lcd;
DHT dht(A0, DHT22);

int  compteur  = 0;
bool etatLed   = false;
bool synchroOK = false;

// WiFi : true si OK, false sinon
bool setup_wifi()
{
  if (WiFi.begin(ssid, pass) == WL_CONNECTED) {
    delay(1000);   // laisse le temps de recevoir l'adresse IP
    return true;
  }
  return false;
}

// Synchro NTP + mise a jour du RTC
bool synchro_ntp()
{
  ntp.begin();
  if (!ntp.forceUpdate()) return false;
  RTCTime heure(ntp.getEpochTime());
  RTC.setTime(heure);
  return true;
}

void setup()
{
  Serial.begin(9600);
  pinMode(LED_VIE, OUTPUT);
  dht.begin();
  RTC.begin();

  lcd.begin(16, 2);
  lcd.setRGB(0, 0, 255);
  lcd.print("Connexion WiFi..");

  if (setup_wifi()) {
    synchroOK = synchro_ntp();

    // ecran d'accueil : version + date, puis adresse IP
    RTCTime now;
    RTC.getTime(now);
    char txt[17];
    snprintf(txt, sizeof(txt), "%s  %02d/%02d/%04d", VERSION,
             now.getDayOfMonth(), Month2int(now.getMonth()), now.getYear());
    lcd.clear();
    lcd.print(txt);
    lcd.setCursor(0, 1);
    lcd.print(WiFi.localIP());
    Serial.println(WiFi.localIP());
  } else {
    lcd.clear();
    lcd.print("WiFi echec");
    Serial.println("WiFi echec");
  }

  delay(3000);
  lcd.clear();
}

void loop()
{
  delay(500);
  compteur++;

  // LED de vie (2 Hz)
  etatLed = !etatLed;
  digitalWrite(LED_VIE, etatLed);

  // toutes les secondes : date et heure
  if (compteur % 2 == 0) {
    lcd.setCursor(0, 0);
    if (synchroOK) {
      RTCTime now;
      RTC.getTime(now);
      char txt[17];
      snprintf(txt, sizeof(txt), "%02d/%02d %02d:%02d:%02d",
               now.getDayOfMonth(), Month2int(now.getMonth()),
               now.getHour(), now.getMinutes(), now.getSeconds());
      lcd.print(txt);
    } else {
      lcd.print("Pas de synchro  ");
    }
  }

  // toutes les 2 secondes : temperature et humidite
  if (compteur % 4 == 0) {
    compteur = 0;
    lcd.setCursor(0, 1);
    lcd.print("T ");
    lcd.print(dht.readTemperature(), 1);
    lcd.print("oC/H ");
    lcd.print(dht.readHumidity(), 1);
    lcd.print("%");
  }
}