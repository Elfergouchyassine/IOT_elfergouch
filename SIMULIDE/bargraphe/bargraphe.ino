const int leds[] = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12};

void setup()
{
  for (int i = 0; i < 10; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], LOW);
  }

}

void loop(){
  for (int i = 0; i < 10; i++) {
    digitalWrite(leds[i], HIGH);
    delay(500);
    digitalWrite(leds[i], LOW);
  }
}
