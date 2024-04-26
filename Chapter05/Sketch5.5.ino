void setup() {
	pinMode(3, OUTPUT);
	Serial.begin(115200);
}

void loop() {
	if (Serial.available()) {
		int val = Serial.read() - '0';
		if (val == 1) {
			digitalWrite(3, HIGH);
			delay(50);
			digitalWrite(3, LOW);
		}
	}
}
