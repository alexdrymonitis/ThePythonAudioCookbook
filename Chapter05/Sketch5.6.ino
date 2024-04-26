void setup() {
	pinMode(3, OUTPUT);
	Serial.begin(115200);
}

void loop() {
	if (Serial.available()) {
		static int val = 0;
		byte in = Serial.read();
		if (isDigit(in)) {
			val = val * 10 + in – '0';
		}
		else if (in == 'v') {
			analogWrite(3, val);
			val = 0;
		}
	}
}
