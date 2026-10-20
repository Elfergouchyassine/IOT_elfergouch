 #include <DHT.h>

#define PIN_DHT     A0
#define TYPE_DHT    DHT22
#define LED_VERTE   3
#define LED_ROUGE   12
#define SEUIL       20.0  

DHT dht(PIN_DHT, TYPE_DHT);

void setup()
{
  Serial.begin(9600);
  pinMode(LED_VERTE, OUTPUT);
  pinMode(LED_ROUGE, OUTPUT);
  dht.begin();
}


void loop()
{
  delay(2000);
  float temperature = dht.readTemperature();
  if (temperature < SEUIL) {
    digitalWrite(LED_VERTE, HIGH);
    digitalWrite(LED_ROUGE, LOW);
  } else {
    digitalWrite(LED_VERTE, LOW);
    digitalWrite(LED_ROUGE, HIGH);
  }
}