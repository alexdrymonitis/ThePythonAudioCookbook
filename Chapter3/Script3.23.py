from pyo import *

s = Server(audio="jack").boot()

bal = SigTo(.75)

samp = SfPlayer(SNDS_PATH+"/transparent.aif",loop=True,mul=.4)
verb = Freeverb(samp, size=[.79,.8], damp=.9, bal=bal).out()

def restore_verb():
	bal.setTime(5)
	bal.setValue(.75)

ca = CallAfter(restore_verb, time=1)
ca.stop()

def reset_verb():
	verb.reset()
	bal.setTime(0)
	bal.setValue(0)
	ca.play()

s.gui(locals())
