import serial
from time import sleep

ser = serial.Serial("/dev/ttyACM1", 115200)

while True:
	ser.write(b'1')
	sleep(1)
	ser.write(b'0')
	sleep(1)
