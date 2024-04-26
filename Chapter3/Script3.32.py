from pyo import *

s = Server(audio="jack").boot()

sineL = Sine(freq=440, mul=.2).out()
sineR = Sine(freq=660, mul=.2).out(1)

s.gui(locals())
