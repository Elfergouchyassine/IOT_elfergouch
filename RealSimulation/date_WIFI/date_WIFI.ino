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
char pass[] = "72Hin@R*";

// serveur NTP (routeur de la salle)
IPAddress serveurNTP(192, 168, 1, 254);
WiFiUDP udp;
NTPClient ntp(udp, serveurNTP, 7200);   // +2 h (heure d'ete), 3600 en hiver

rgb_lcd lcd;
DHT dht(A0, DHT22);

float t = 0;
float h = 0;

int compteur = 0;   // +1 toutes les 500 ms
bool etatLed = false;
bool synchroOK = false;

void deuxChiffres(int valeur)
{
  if (valeur < 10) lcd.print("0");
  lcd.print(valeur);
}

// a) connexion WiFi : true si OK, false sinon
bool setup_wifi()
{
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Module WiFi absent");
    return false;
  }

  for (int essai = 0; essai < 3; essai++) {
    Serial.print("Connexion a ");
    Serial.println(ssid);

    if (WiFi.begin(ssid, pass) == WL_CONNECTED) {
      // on attend que la carte recoive son adresse IP
      for (int i = 0; i < 20 && WiFi.localIP() == IPAddress(0, 0, 0, 0); i++) {
        delay(250);
      }
      Serial.println("WiFi connecte");
      return true;
    }
    delay(1000);
  }

  Serial.println("Echec connexion WiFi");
  return false;
}

// e) synchronisation NTP puis mise a jour du RTC
bool synchro_ntp()
{
  ntp.begin();
  if (ntp.forceUpdate()) {
    RTCTime heureNTP(ntp.getEpochTime());
    RTC.setTime(heureNTP);
    Serial.println("Synchro NTP OK");
    return true;
  }
  Serial.println("Echec synchro NTP");
  return false;
}

void setup()
{
  Serial.begin(9600);
  pinMode(LED_VIE, OUTPUT);
  dht.begin();

  lcd.begin(16, 2);
  lcd.setRGB(0, 0, 255);

  // date par defaut, utilisee seulement si la synchro echoue
  RTC.begin();
  RTCTime depart(1, Month::JANUARY, 2026, 0, 0, 0,
                 DayOfWeek::THURSDAY, SaveLight::SAVING_TIME_INACTIVE);
  RTC.setTime(depart);

  lcd.print("Connexion WiFi..");

  // b) appel de la fonction WiFi
  bool wifiOK = setup_wifi();

  if (wifiOK) {
    synchroOK = synchro_ntp();
  }

  // d) ecran d'accueil : version + date / adresse IP
  RTCTime maintenant;
  RTC.getTime(maintenant);

  lcd.clear();
  lcd.print(VERSION);
  lcd.print("  ");
  deuxChiffres(maintenant.getDayOfMonth());
  lcd.print("/");
  deuxChiffres(Month2int(maintenant.getMonth()));
  lcd.print("/");
  lcd.print(maintenant.getYear());

  lcd.setCursor(0, 1);
  if (wifiOK) lcd.print(WiFi.localIP());
  else lcd.print("Pas de WiFi");

  Serial.print(VERSION);
  Serial.print("  IP : ");
  Serial.println(WiFi.localIP());

  delay(3000);
  lcd.clear();
}

void loop()
{
  delay(500);
  compteur++;

  // LED de vie
  etatLed = !etatLed;
  digitalWrite(LED_VIE, etatLed);

  // toutes les secondes : date et heure (ou message si pas de synchro)
  if (compteur % 2 == 0) {
    lcd.setCursor(0, 0);

    if (synchroOK) {
      RTCTime maintenant;
      RTC.getTime(maintenant);

      lcd.print(maintenant.getDayOfMonth());
      lcd.print("/");
      lcd.print(Month2int(maintenant.getMonth()));
      lcd.print("/");
      lcd.print(maintenant.getYear() % 100);
      lcd.print(" ");
      deuxChiffres(maintenant.getHour());
      lcd.print(":");
      deuxChiffres(maintenant.getMinutes());
      lcd.print(":");
      deuxChiffres(maintenant.getSeconds());
    } else {
      lcd.print("Pas de synchro  ");
    }
  }

  // toutes les 2 secondes : temperature et humidite
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