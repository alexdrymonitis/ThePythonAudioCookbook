int distance, time;

void setup() {
	pinMode(7,OUTPUT); //Trig Pin
	pinMode(6,INPUT); //Echo Pin

	Serial.begin(115200);
}

void loop() {
	digitalWrite(7,LOW); //Trig Off
	delayMicroseconds(20);
	digitalWrite(7,HIGH); //Trig ON
	delayMicroseconds(20);
	digitalWrite(7,LOW); //Trig Off
	delayMicroseconds(20);
	time = pulseIn(6, HIGH);//TO RECEIVE REFLECTED SIGNAL

	distance= time*0.0340/2;

	Serial.print("dist: ");
	Serial.println(distance);
	delay(10);
}
