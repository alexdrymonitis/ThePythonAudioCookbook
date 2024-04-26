from pyo import *
s = Server(audio="jack").boot()

event = Events(
	midinote=EventSeq(
		[
			EventSeq([60, 62, 63], occurrences=2),
			EventSeq([62, 67], occurrences=3),
			EventSeq([65, 64, 62, 66], occurrences=1),
			EventSeq([67, 62], occurrences=2),
		],
		occurrences=inf,
	),
	beat= 1/4
).play()

s.gui(locals())
