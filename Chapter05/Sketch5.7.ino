// create an array with the LED and switch pins
int ledPins[4] = {6, 7, 8, 9};
int switchPins[4] = {2, 3, 4, 5};
// and an index for the array above
int whichLed = 0;

void setup() {
	Serial.begin(115200);

	for (int i = 0; i < 4; i++) {
		pinMode(switchPins[i], INPUT);
		pinMode(ledPins[i], OUTPUT);
	}
}

void loop() {
	// read incoming data to control the LEDs
	while (Serial.available()) {
		static int val = 0;
		byte in = Serial.read();
		if (isDigit(in)) {
			val = val * 10 + in - '0';
		}
		// a byte ending with 'l' denotes which LED to control
		else if (in == 'l') {
			whichLed = val;
			val = 0;
		}
		// a byte ending with 'v' denotes an LED state
		else if (in == 'v') {
			digitalWrite(ledPins[whichLed], val);
			val = 0;
		}
	}
	// send the potentiometer values first
	Serial.print("pots");
	for (int i = 0; i < 6; i++) {
		Serial.print(" ");
		Serial.print(analogRead(i));
	}
	Serial.println();
	// then send the switches
	Serial.print("switches");
	for (int i = 0; i < 4; i++) {
		Serial.print(" ");
		Serial.print(digitalRead(switchPins[i]));
	}
	Serial.println();
	delay(10);
}
