from pyo import *

s = Server(audio="jack").boot()

sf = SfPlayer(SNDS_PATH+"/transparent.aif",loop=True, mul=0.7)
pva = PVAnal(sf)
pvs = PVAddSynth(pva, pitch=1.25, num=100, first=0, inc=2)
mix = Mix(pvs.mix(1), 2).out()

s.gui(locals())
