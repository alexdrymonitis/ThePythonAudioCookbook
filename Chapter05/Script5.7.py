import serial
from pyo import *

ser = serial.Serial('/dev/ttyACM1', 115200)
s = Server().boot()

def lightup():
	ser.write(b'1')

mic = Input(0)
att = AttackDetector(mic)
tf = TrigFunc(att, lightup)

s.gui(locals())
