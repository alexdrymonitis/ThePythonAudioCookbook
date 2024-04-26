from pyo import *
s = Server(audio="jack").boot()

class EventTri(EventInstrument):
	def __init__(self, **kwargs):
		EventInstrument.__init__(self, **kwargs)
		self._brkpnt = Sig(self.brkpnt)
		self._invbrk = 1.0 - self._brkpnt
		self._phasor = Phasor(freq=self.freq)
		self._rising = (self._phasor/self._brkpnt) * \
			(self._phasor < self._brkpnt)
		self._falling = (((self._phasor-self._brkpnt)/\
			self._invbrk)*(-1)+1)*(self._phasor>=self._brkpnt)
		self._osc=Sig((self._rising+self._falling),
					  mul=2, add=-1)
		self.output = Sig(self._osc, mul=self.env).out()


event = Events(
	instr=EventTri,
	degree=EventSeq([5.00, 5.04, 5.07, 6.00]),
	brkpnt=EventSeq([0.2, 0.4, 0.6, 0.8]),
	beat= 1/2
).play()

s.gui(locals())
