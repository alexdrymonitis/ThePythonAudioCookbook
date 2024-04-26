from pyo import *

s = Server(audio="jack").boot()

freq = Sig(80)

saw = Phasor(freq, mul=2, add=-1)
sqr = Round(saw)
filt = MoogLP(sqr, freq=freq*5, res=1.25)

outsig = Mix(filt.mix(1), voices=2, mul=.2).out()

filt.ctrl(map_list=[SLMap(0, 2, 'lin', 'res', 1.25)])

sc = Scope(outsig, gain=1)
sp = Spectrum(outsig)
s.gui(locals())
