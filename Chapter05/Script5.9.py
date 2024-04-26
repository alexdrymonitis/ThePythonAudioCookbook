import serial
from pyo import *

ser = serial.Serial('/dev/ttyACM1', 115200)
s = Server().boot()

sine = Sine(freq=.5, mul=.5, add=.5)

def lightup():
	b = bytes(str(int(sine.get()*255))+"v", 'utf-8')
	ser.write(b)

pat = Pattern(lightup, time=.01).play()

s.gui(locals())
