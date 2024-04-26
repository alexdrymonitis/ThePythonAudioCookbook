from pyo import *

s = Server(audio="jack").boot()

noise = Noise(mul=.2)
pan = Pan(noise, outs=2, pan=.5, spread=0).out()

pan.ctrl()

s.gui(locals())
