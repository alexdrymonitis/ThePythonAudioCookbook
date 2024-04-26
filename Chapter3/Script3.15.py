from pyo import *
import random

s = Server(audio="jack").boot()

base_freq = 100

sines = [Sine(freq=((random.random()*10)*base_freq),
         mul=random.random()) for i in range(10)]
mixer = Mixer(outs=1, chnls=1)

for i in range(10):
	mixer.addInput("additive"+str(i), sines[i])
	mixer.setAmp("additive"+str(i), 0, .5)

sig = Sig(mixer[0], mul=.2).mix(2).out()


def set_rand_freqs():
	for i in range(10):
		sines[i].setFreq((random.random()*10)*base_freq)


def set_rand_amps():
	for i in range(10):
		sines[i].mul = random.random()

sc = Scope(sig)
sp = Spectrum(sig)

s.gui(locals())
