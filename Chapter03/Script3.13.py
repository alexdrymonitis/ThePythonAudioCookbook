from pyo import *

s = Server(audio="jack").boot()

base_freq = 100

sines = [Sine(freq=(i*base_freq),mul=(1/pow(i,2)))
         for i in range(1,80,2)]
mixer = Mixer(outs=1, chnls=2)

for i in range(40):
	sines[i].mul *= ((((i+1)%2) * 2) - 1)
	mixer.addInput("additive"+str(i), sines[i])
	mixer.setAmp("additive"+str(i), 0, .5)

sig = Sig(mixer[0], mul=.5).out()

sc = Scope(sig)
sp = Spectrum(sig)

s.gui(locals())
