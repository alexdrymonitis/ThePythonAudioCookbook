from pyo import *

s = Server(audio="jack").boot()

mod = Sine(freq=200, mul=.1, add=.4)
car = Sine(800, phase=mod, mul=.2).mix(2).out()

sp = Spectrum(car, size=4096)

s.gui(locals())
