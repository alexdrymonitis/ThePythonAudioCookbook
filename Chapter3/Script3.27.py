from pyo import *

s = Server(audio="jack").boot()

adsr=Adsr(attack=.04,decay=.08,sustain=.6,release=.06,dur=.2)
fm = FM(carrier=200, ratio=.248, index=adsr*8, mul=adsr*0.3)
mix = Mix(fm.mix(1), voices=2).out()

def func_0():
	fm.setCarrier(200)
	fm.setIndex(adsr*4)
	adsr.play()

def func_1():
	fm.setCarrier(250)
	fm.setIndex(adsr*6)
	adsr.play()

def func_2():
	fm.setCarrier(300)
	fm.setIndex(adsr*8)
	adsr.play()

metro = Metro(time=.2).play()
counter = Counter(metro, min=0, max=3)
score = Score(counter, fname="func_")

s.gui(locals())
