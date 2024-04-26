void setup() {
	Serial.begin(115200);
}

void loop() {
	int infraval = analogRead(0);
	Serial.println(infraval);
	delay(500);
}
