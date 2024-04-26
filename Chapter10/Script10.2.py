from pyo import *
s = Server(audio="jack").boot()

def clipfreq(val):
	if val > 60:
		return val
	else:
		return 60

event = Events(
	midinote=EventCall(
		clipfreq,EventNoise().rescale(-1,1,48,72,1)
	),
	beat= 1/4,
	db=-12,
	attack=0.001,
	decay=0.05,
	sustain=0.5,
	release=0.005,
).play()

s.gui(locals())
