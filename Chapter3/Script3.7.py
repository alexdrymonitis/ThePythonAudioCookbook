from pyo import *

s = Server(audio="jack").boot()

ndx = Sig(150)
mod = Sine(freq=200, mul=ndx)
car = Sine(800+mod, mul=.2).mix(2).out()

sp = Spectrum(car, size=4096)

s.gui(locals())
