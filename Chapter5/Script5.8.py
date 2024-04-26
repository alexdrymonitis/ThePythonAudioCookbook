from pyfirmata import Arduino
from time import sleep
from pyo import *

board = Arduino("/dev/ttyACM1")
s = Server().boot()

def lightup():
	board.digital[3].write(1)
	sleep(.05)
	board.digital[3].write(0)

mic = Input(0)
att = AttackDetector(mic)
tf = TrigFunc(att, lightup)

s.gui(locals())
