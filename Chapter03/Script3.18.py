from pyo import *

s = Server(audio="jack").boot()

snd = SndTable(SNDS_PATH+"/transparent.aif")
env = HannTable()
pos = Randi(min=0, max=1, freq=[0.25, .3], mul=snd.getSize())
dur = Noise(.001, .1)

grn1 = Granulator(snd, env, pitch=[1, 1.001], pos=pos,
                  dur=dur, grains=24, mul=.1)
grn2 = Granule(snd, env, pitch=[1, 1.001], pos=pos, dur=dur,
               dens=24, mul=.1)

selvoice = SigTo(0, time=5)
sel = Selector(inputs=[grn1, grn2], voice=selvoice).out()

grn1.ctrl()
grn2.ctrl()

sc = Scope(sel)

s.gui(locals())
