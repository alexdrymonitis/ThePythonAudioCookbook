from pyo import *

s = Server(audio="jack")
s.setMidiInputDevice(3)

s.boot()

notes = Notein(poly=10, scale=1, mul=.5)
adsr=MidiAdsr(notes['velocity'],attack=.005,decay=.1,
              sustain=.4, release=1)
ratio = Midictl(21, channel=1, mul=.5)
index1 = Midictl(22, channel=1, mul=5)
index2 = Midictl(23, channel=1, mul=5)
xfm = CrossFM(carrier=notes['pitch'], ratio=ratio,
              ind1=index1, ind2=index2, mul=adsr).out()

s.gui(locals())
