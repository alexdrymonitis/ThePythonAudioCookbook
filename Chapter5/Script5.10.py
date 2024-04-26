from pyfirmata import Arduino
from pyo import *

board = Arduino("/dev/ttyACM1")
s = Server().boot()

sine = Sine(freq=.5, mul=.5, add=.5)

pwm = board.get_pin("d:3:p")

def lightup():
	pwm.write(sine.get())

pat = Pattern(lightup, time=.01).play()

s.gui(locals())
