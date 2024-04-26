from pyo import *

s = Server(audio="jack").boot()

adsr = Adsr(attack=.05,decay=.1,sustain=.6,release=.1,dur=0)
fm = FM(carrier=200, ratio=.248, index=adsr*8,
        mul=adsr*0.3).mix(2).out()

counter = 0
def playenv():
	global counter
	if not counter:
		adsr.play()
	else:
		adsr.stop()
	counter += 1
	if counter == 2:
		counter = 0

pat = Pattern(playenv, time=.2).play()

s.gui(locals())
