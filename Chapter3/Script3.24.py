from pyo import *

s = Server(audio="jack").boot()

bal = SigTo(.6)

samp = SfPlayer(SNDS_PATH+"/transparent.aif",loop=True,mul=.4)
verb = WGVerb(samp, feedback=[.74,.75], cutoff=5000,
              bal=bal,mul=.3).out()

def restore_verb():
	bal.setTime(5)
	bal.setValue(.6)

ca = CallAfter(restore_verb, time=1)
ca.stop()

def reset_verb():
	verb.reset()
	bal.setTime(0)
	bal.setValue(0)
	ca.play()

s.gui(locals())
