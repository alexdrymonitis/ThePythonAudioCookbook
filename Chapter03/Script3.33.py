from pyo import *

s = Server(audio="jack").boot()

sine = Sine(freq=440, mul=.2).mix(2).out()
sine.setFreq(660)

s.gui(locals())
