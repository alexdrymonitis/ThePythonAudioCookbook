from pyo import *

class Square(PyoObject):
	"""
	A square wave oscillator with duty cycle control
	:Parent: :py:class:’PyoObject’

	:Args:
		freq: float or PyoObject
			Oscillator frequency
		phase: float or PyoObject
			Phase of the oscillator
		duty: float or PyoObject
			Duty cycle
	
	>>> s = Server().boot()
	>>> s.start()
	>>> lfo = Sine(.25, mul=.5, add=.5)
	>>> square = Square([200,202], duty=lfo, mul=.2).out()
	"""
	def __init__(self,freq=1000,phase=0,duty=0.5,mul=1,add=0):
		PyoObject.__init__(self, mul, add)
		self._freq = freq
		self._duty = duty
		self._phase = phase
		self._freq,self._phase,\
		self._duty,mul,add,lmax=convertArgsToLists(
									freq,phase,
									duty,mul,add
								)
		self._phasor = Phasor(freq=self._freq,
		phase=self._phase)
		self._comp = Compare(self._phasor, comp=self._duty,
                             mul=2, add=-1)
		self._sig = Sig(self._comp, mul=mul, add=add)
		self._base_objs = self._sig.getBaseObjects()

	def setFreq(self, freq):
		self._freq = freq
		self._phasor.setFreq(self._freq)

	def setPhase(self, phase):
		self._phase = phase
		self._phasor.setPhase(self._phase)

	def setDuty(self, duty):
		self._duty = duty
		self._comp.setComp(self._duty)

	@property
	def freq(self):
		return self._freq

	@freq.setter
	def freq(self, freq):
		self.setFreq(freq)

	@property
	def phase(self):
		return self._phase

	@phase.setter
	def phase(self, phase):
		self.setPhase(phase)

	@property
	def duty(self):
		return self._duty

	@duty.setter
	def duty(self, duty):
		self.setDuty(duty)


if __name__ == "__main__":
	s = Server(audio="jack").boot()
	lfo = Sine(freq=.25, mul=.4, add=.5)
	square = Square([200,202], duty=lfo, mul=.2).out()
	sc = Scope(square, gain=1)
	s.gui(locals())
