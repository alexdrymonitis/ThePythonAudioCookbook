from pyo import *

s = Server(audio="jack").boot()

tri = LFO(freq=440, sharp=1, type=3)
saw = Phasor(freq=440, mul=2, add=-1)
sel = Selector(inputs=[tri, saw], voice=0.0)

sc = Scope(sel)

s.gui(locals())
