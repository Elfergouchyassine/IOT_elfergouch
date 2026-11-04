#include <Wire.h>
#include <rgb_lcd.h>
#include <DHT.h>
#include "RTC.h"
#include <WiFiS3.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <ArduinoMqttClient.h>

#define LED_VIE 13
#define VERSION "V1.0"

char ssid[] = "IoT IMT Nord Europe";
// char ssid[] = "IoT IMT Nord Europe 5G";
char pass[] = "72Hin@R*";

// ----- NTP -----
WiFiUDP udp;
NTPClient ntp(udp, IPAddress(192, 168, 1, 254), 7200);  // +2h ete, 3600 hiver

const char broker[] = "192.168.1.1";
const int  port     = 1883;

String idPC = "42920";

String topicVersion = "/iot/VERSION_"     + idPC;
String topicTemp    = "/iot/TEMPERATURE_" + idPC;
String topicHumi    = "/iot/HUMIDITY_"    + idPC;
String topicDate    = "/iot/GET_DATE_"    + idPC;

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

rgb_lcd lcd;
DHT dht(A0, DHT22);

float t = 0;
float h = 0;
int  compteur  = 0;
bool etatLed   = false;
bool synchroOK = false;
bool mqttOK    = false;

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

// MQTT : retourne 0 si OK, sinon le code erreur
int setup_mqtt()
{
  mqttClient.setId("IdO_Client_" + idPC);
  mqttClient.setUsernamePassword("mos_user", "mos_user"); 

  if (!mqttClient.connect(broker, port)) {
    return mqttClient.connectError();
  }
  return 0;
}

// Envoie une valeur sur un topic
void publier(String topic, String valeur)
{
  mqttClient.beginMessage(topic);
  mqttClient.print(valeur);
  mqttClient.endMessage();
}

// Publie les 4 topics du paragraphe 3.2
void publier_mqtt()
{
  RTCTime now;
  RTC.getTime(now);
  char date[20];
  snprintf(date, sizeof(date), "%02d/%02d/%04d %02d:%02d:%02d",
           now.getDayOfMonth(), Month2int(now.getMonth()), now.getYear(),
           now.getHour(), now.getMinutes(), now.getSeconds());

  publier(topicVersion, "1.0");
  publier(topicTemp,    String(t, 1));
  publier(topicHumi,    String(h, 1));
  publier(topicDate,    String(date));
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

    int erreur = setup_mqtt();
    mqttOK = (erreur == 0);

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
    if (mqttOK) Serial.println("MQTT connecte");
    else        { Serial.print("Erreur MQTT : "); Serial.println(erreur); }
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

  if (mqttOK) mqttClient.poll();   // garde la connexion MQTT active

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

  // toutes les 2 secondes : mesure, affichage et publication
  if (compteur % 4 == 0) {
    compteur = 0;

    float nouvT = dht.readTemperature();
    float nouvH = dht.readHumidity();
    if (!isnan(nouvT)) t = nouvT;   // garde l'ancienne valeur si la lecture echoue
    if (!isnan(nouvH)) h = nouvH;

    lcd.setCursor(0, 1);
    lcd.print("T ");
    lcd.print(t, 1);
    lcd.print("oC/H ");
    lcd.print(h, 1);
    lcd.print("%");

    if (mqttOK) publier_mqtt();
  }
}