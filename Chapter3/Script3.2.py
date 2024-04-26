from pyo import *

s = Server(audio="jack").boot()

a = Phasor(freq=440)
b = Round(a, mul=2, add=-1)
sc = Scope(b, gain=1)

s.gui(locals())
