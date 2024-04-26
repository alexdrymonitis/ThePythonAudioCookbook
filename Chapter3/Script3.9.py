from pyo import *

s = Server(audio="jack").boot()

ndx = Sine(freq=0.5, mul=2, add=3)
fm = FM(carrier=800,ratio=0.25,index=ndx,mul=.2).mix(2).out()

sp = Spectrum(fm, size=4096)
s.gui(locals())
