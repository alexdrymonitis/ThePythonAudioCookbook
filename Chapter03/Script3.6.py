from pyo import *

s = Server(audio="jack").boot()

mod = Sine(freq=15, mul=0.5, add=0.5)
car = Sine(freq=400, mul=mod)
am = Mix(car, voices=2, mul=.2).out()

sp = Spectrum(am)
sc = Scope(am)

s.gui(locals())
