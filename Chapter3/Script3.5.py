from pyo import *

s = Server(audio="jack").boot()

mod = Sine(freq=400)
car = Sine(freq=1000, mul=mod)
rm = Sig(car, mul=.2).mix(2).out()

sp = Spectrum(rm)
sc = Scope(rm)

s.gui(locals())
