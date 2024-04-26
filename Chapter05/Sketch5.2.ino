 void setup() {
	pinMode(LED_BUILTIN, OUTPUT);
	Serial.begin(115200);
}

void loop() {
	if (Serial.available()) {
		int val = Serial.read() - '0';
		digitalWrite(LED_BUILTIN, val);
	}
}
