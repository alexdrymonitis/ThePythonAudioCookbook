 void setup() {
	Serial.begin(115200);
}

void loop() {
	for (int i = 0; i < 2; i++) {
		int sensVal = analogRead(i);
		Serial.print("sens");
		Serial.print(i);
		Serial.print(" ");
		Serial.println(sensVal);
	}
	delay(10);
}
