from pyo import *
s = Server(audio="jack").boot()

def setamp(val):
	if val > 60:
		return -12
	else:
		return -24

event1 = Events(
	midinote=EventNoise().rescale(-1,1,48,72,1),
	beat= 1/4,
	db=EventCall(setamp,EventKey("midinote"))
).play()

event2 = Events(
	midinote=EventKey(
				"midinote",master=event1
			 ).rescale(48,72,72,48,1),
	beat=1/4,
	db=EventCall(setamp,EventKey("midinote"))
).play()

s.gui(locals())
