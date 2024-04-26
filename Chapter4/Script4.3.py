from pyo import *

s = Server(audio="jack").boot()

sl = SineLoop(freq=[100,101], feedback=0.12, mul=.5)
sf = SfPlayer(SNDS_PATH+"/transparent.aif", loop=True, mul=.5)
pva1 = PVAnal(sl)
pva2 = PVAnal(sf)
pvm = PVMorph(pva1, pva2, fade=.5)
pvs = PVSynth(pvm).out()

pvm.ctrl()

s.gui(locals())
