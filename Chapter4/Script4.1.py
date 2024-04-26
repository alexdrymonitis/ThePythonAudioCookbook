from pyo import *

s = Server(audio="jack").boot()

sf1 = SfPlayer("samples/harm_sound.wav", loop=True, mul=.5)
sf2 = SfPlayer("samples/noisy_conv.wav", loop=True, mul=.5)
pva1 = PVAnal(sf1)
pva2 = PVAnal(sf2)
pvc = PVCross(pva1, pva2, fade=1)
pvs = PVSynth(pvc).out()

def size(x):
	pva1.setSize(x)
	pva2.setSize(x)

def olaps(x):
	pva1.setOverlaps(x)
	pva2.setOverlaps(x)

pvc.ctrl()

s.gui(locals())
