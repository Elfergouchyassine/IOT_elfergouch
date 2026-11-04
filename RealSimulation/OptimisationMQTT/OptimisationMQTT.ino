#include <Wire.h>
#include <rgb_lcd.h>
#include <DHT.h>
#include "RTC.h"
#include <WiFiS3.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <ArduinoMqttClient.h>

#define LED_VIE  2
#define VERSION  "V1.0"

const int bargraphe[] = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12};

char ssid[] = "IoT IMT Nord Europe";
// char ssid[] = "IoT IMT Nord Europe 5G";
char pass[] = "72Hin@R*";

// ----- NTP -----
WiFiUDP udp;
NTPClient ntp(udp, IPAddress(192, 168, 1, 254), 7200);  // +2h ete, 3600 hiver

// ----- MQTT -----
const char broker[] = "192.168.1.1";
const int  port     = 1883;

String idPC = "42920";

// topics publies
String topicVersion  = "/iot/VERSION_"     + idPC;
String topicTemp     = "/iot/TEMPERATURE_" + idPC;
String topicHumi     = "/iot/HUMIDITY_"    + idPC;
String topicDate     = "/iot/GET_DATE_"    + idPC;

// topics souscrits
String topicCommand  = "/iot/COMMAND_"     + idPC;
String topicBargraph = "/iot/BARGRAPH_"    + idPC;
String topicBlink    = "/iot/BLINK_"       + idPC;

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

rgb_lcd lcd;
DHT dht(A0, DHT22);

float t = 0;
float h = 0;
float ancienT = -1000;     // dernieres valeurs publiees (6.1.6)
float ancienH = -1000;

int  compteur  = 0;        // +1 toutes les 100 ms
bool etatLed   = false;
bool synchroOK = false;
bool mqttOK    = false;

bool mesureActive = true;  // commande 20 / 30
int  periodeLed   = 500;   // periode actuelle de la LED de vie (ms)
int  periodeBlink = 500;   // periode personnalisee recue sur BLINK (ms)
int  compteurLed  = 0;

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

// Envoie une valeur sur un topic
void publier(String topic, String valeur)
{
  mqttClient.beginMessage(topic);
  mqttClient.print(valeur);
  mqttClient.endMessage();
}

// Allume un nombre de LED proportionnel a la valeur (0 a 1023)
void afficherBargraphe(int valeur)
{
  valeur = constrain(valeur, 0, 1023);
  int nb = map(valeur, 0, 1023, 0, 10);

  for (int i = 0; i < 10; i++) {
    if (i < nb) digitalWrite(bargraphe[i], HIGH);
    else        digitalWrite(bargraphe[i], LOW);
  }
}

// Traitement des codes commande
void traiterCommande(int code)
{
  if (code == 10) {                 // forcer la mise a l'heure
    synchroOK = synchro_ntp();
    if (synchroOK) publier(topicVersion, "1.0");   // 6.1.6 a)
  }
  else if (code == 20) {            // demarrage mesure
    mesureActive = true;
  }
  else if (code == 30) {            // arret mesure
    mesureActive = false;
    lcd.setCursor(0, 1);
    lcd.print("Mesure arretee  ");
  }
  else if (code == 40) {            // clignotement lent
    periodeLed = 1000;
  }
  else if (code == 50) {            // clignotement rapide
    periodeLed = 200;
  }
  else if (code == 60) {            // clignotement personnalise
    periodeLed = periodeBlink;
  }
}

// Appelee a chaque message recu
void onMqttMessage(int tailleMessage)
{
  // acquisition du topic
  String topic = mqttClient.messageTopic();

  // acquisition du message
  String message = "";
  while (mqttClient.available()) {
    message += (char)mqttClient.read();
  }

  // conversion en entier
  int valeur = message.toInt();

  Serial.print("Recu ");
  Serial.print(topic);
  Serial.print(" : ");
  Serial.println(valeur);

  if (topic.indexOf("COMMAND") >= 0) {
    traiterCommande(valeur);
  }
  else if (topic.indexOf("BARGRAPH") >= 0) {
    afficherBargraphe(valeur);
  }
  else if (topic.indexOf("BLINK") >= 0) {
    periodeBlink = (valeur / 100) * 100;      // multiple de 100 ms
    if (periodeBlink < 100) periodeBlink = 100;
  }
}

// MQTT : retourne 0 si OK, sinon le code erreur
int setup_mqtt()
{
  mqttClient.setId("IdO_Client_" + idPC);
  mqttClient.setUsernamePassword("mos_user", "mos_user");

  if (!mqttClient.connect(broker, port)) {
    return mqttClient.connectError();
  }

  // callback + souscription aux 3 topics
  mqttClient.onMessage(onMqttMessage);
  mqttClient.subscribe(topicCommand);
  mqttClient.subscribe(topicBargraph);
  mqttClient.subscribe(topicBlink);

  return 0;
}

// Publie temperature, humidite et date (la version n'est plus publiee ici)
void publier_mqtt()
{
  RTCTime now;
  RTC.getTime(now);
  char date[20];
  snprintf(date, sizeof(date), "%02d/%02d/%04d %02d:%02d:%02d",
           now.getDayOfMonth(), Month2int(now.getMonth()), now.getYear(),
           now.getHour(), now.getMinutes(), now.getSeconds());

  publier(topicTemp, String(t, 1));
  publier(topicHumi, String(h, 1));
  publier(topicDate, String(date));
}

void setup()
{
  Serial.begin(9600);
  pinMode(LED_VIE, OUTPUT);

  for (int i = 0; i < 10; i++) {
    pinMode(bargraphe[i], OUTPUT);
    digitalWrite(bargraphe[i], LOW);
  }

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
  delay(100);
  compteur++;

  if (mqttOK) mqttClient.poll();   // recoit les messages + garde la connexion

  // LED de vie : change d'etat toutes les "periodeLed" ms
  compteurLed++;
  if (compteurLed * 100 >= periodeLed) {
    compteurLed = 0;
    etatLed = !etatLed;
    digitalWrite(LED_VIE, etatLed);
  }

  // toutes les secondes (10 x 100 ms) : date et heure
  if (compteur % 10 == 0) {
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

  // toutes les 2 secondes (20 x 100 ms) : mesure, affichage et publication
  if (compteur % 20 == 0) {
    compteur = 0;

    if (mesureActive) {
      float nouvT = dht.readTemperature();
      float nouvH = dht.readHumidity();
      if (!isnan(nouvT)) t = nouvT;
      if (!isnan(nouvH)) h = nouvH;

      lcd.setCursor(0, 1);
      lcd.print("T ");
      lcd.print(t, 1);
      lcd.print("oC/H ");
      lcd.print(h, 1);
      lcd.print("%");

      // 6.1.6 b) on publie seulement si T ou H a change (au dixieme pres)
      if (mqttOK && ((int)(t * 10) != (int)(ancienT * 10) ||
                     (int)(h * 10) != (int)(ancienH * 10))) {
        publier_mqtt();
        ancienT = t;
        ancienH = h;
      }
    }
  }
}