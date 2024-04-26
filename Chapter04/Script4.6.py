from pyo import *

s = Server(audio="jack").boot()

sf = SfPlayer(SNDS_PATH+"/transparent.aif", loop=True, mul=.5)
pva = PVAnal(sf, size=2048)
pvv = PVVerb(pva, revtime=0.95, damp=0.95)
pvs = PVSynth(pvv).mix(2).out()

pvv.ctrl()

s.gui(locals())
