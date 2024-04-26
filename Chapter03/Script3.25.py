from pyo import *

s = Server(audio="jack").boot()

adsr = Adsr(attack=.05,decay=.2,sustain=.6,release=.1,dur=2)
fm = FM(carrier=200, ratio=.248, index=adsr*8,
        mul=adsr*0.3).mix(2).out()

s.gui(locals())
