from pyfirmata import Arduino
from time import sleep

board = Arduino("/dev/ttyACM1")

while True:
	board.digital[13].write(1)
	sleep(1)
	board.digital[13].write(0)
	sleep(1)
