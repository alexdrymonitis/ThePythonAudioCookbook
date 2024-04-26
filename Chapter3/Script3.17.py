from pyo import *
import random

s = Server(audio="jack").boot()

amps = []

for i in range(10):
	amps.append(0)

randtab = HarmTable(amps)
randtab.autoNormalize(True)
lookup = Osc(table=randtab, freq=200, mul=.2).out()

def rand_amps():
	for i in range(10):
		amps[i] = random.random()
	randtab.replace(amps)

rand_amps()

sc = Scope(lookup, gain=1)

s.gui(locals())
