# Copyright 2017 Alexandros Drymonitis
#
# This code is based on the Pyo Python module
# and code by Olivier Belanger
# Pyo is released under the GNU GPL 3 Licence,
# so is this file
# A Licence copy should come with this code
# If not, please check <http://www.gnu.org/licenses/>
#
# This is an oscillator with a settable breakpoint

from pyo import *

class BrkPntOsc(PyoObject):
	"""
	An oscillator with a settable breakpoint
	resulting in a waveform that goes from a backward
	sawtooth to a forward sawtooth.

	:Parent: :py:class:’PyoObject’

	:Args:

		freq: float or PyoObject, optional
			Frequency in cycles per second. Defaults to 100.
		phase: float or PyoObject, optional
			   Phase of sampling,
			   expressed as a fraction of a cycle (0 to 1).
			Defaults to 0.
		brkpnt: float or PyoObject, optional
			Point where the waveform breaks. From 0 to 1.
			Defaults to 0.5.

	>>> s = Server().boot()
	>>> s.start()
	>>> a = BrkPntOsc(200, brkpnt=.75, mul=.2).out()
	
	"""
	def __init__(self, freq=100, phase=0,
                 brkpnt=0.5, mul=1, add=0):
		PyoObject.__init__(self, mul, add)
		self._freq = freq
		self._phase = phase
		self._brkpnt = Sig(brkpnt)
		self._invbrk = 1.0 - self._brkpnt
		self._phasor=Phasor(freq=self._freq,
		phase=self._phase)
		self._rising = (self._phasor/self._brkpnt) * \
                       (self._phasor < self._brkpnt)
		self._falling = (((self._phasor - self._brkpnt)/\
                        self._invbrk) * (-1) + 1) * \
                        (self._phasor >= self._brkpnt)
		self._osc=Sig((self._rising+self._falling),
                      mul=2,add=-1)
		# A Sig is the best way to properly handle
		# “mul” and “add” arguments.
		self._output = Sig(self._osc, mul, add)
		# Create the “_base_objs” attribute.
		# This is the object’s audio output.
		self._base_objs = self._output.getBaseObjects()

	def setFreq(self, x):
		"""
		Replace the ‘freq’ attribute.
	
		:Args:
	
		x: float or PyoObject
		New ‘freq’ attribute.
	
		"""
		self._freq = x
		self._phasor.freq = x

	def setPhase(self, x):
		"""
		Replace the ‘phase’ attribute.
	
		:Args:
	
		x: float or PyoObject
		New ‘phase’ attribute.
	
		"""
		self._phase = x
		self._phasor.phase = x

	def setBrkPnt(self, x):
		"""
		Replace the ‘breakpoint’ attribute.

		:Args:

		x: float or PyoObject
		New ‘phase’ attribute.
	
		"""
		self._brkpnt.value = x

	def play(self, dur=0, delay=0):
		for key in self.__dict__.keys():
			if isinstance(self.__dict__[key], PyoObject):
				self.__dict__[key].play(dur, delay)
		return PyoObject.play(self, dur, delay)

	def stop(self):
		for key in self.__dict__.keys():
			if isinstance(self.__dict__[key], PyoObject):
				self.__dict__[key].stop()
		return PyoObject.stop(self)

	def out(self, chnl=0, inc=1, dur=0, delay=0):
		for key in self.__dict__.keys():
			if isinstance(self.__dict__[key], PyoObject):
				self.__dict__[key].play(dur, delay)
		return PyoObject.out(self, chnl, inc, dur, delay)

	@property
	def freq(self):
		"""float or PyoObject.
		Fundamental frequency in cycles per second."""
		return self._freq

	@freq.setter
	def freq(self, x): self.setFreq(x)

	@property
	def phase(self):
		"""float or PyoObject.
		Phase of sampling between 0 and 1."""
		return self._phase

	@phase.setter
	def phase(self, x): self.setPhase(x)

	@property
	def breakpoint(self):
		"""float or PyoObject.
		Breakpoint of oscillator between 0 and 1."""
		return self._brkpnt

	@breakpoint.setter
	def breakpoint(self, x): self.setBrkPnt(x)


if __name__ == "__main__":
	# Test case . . .
	s = Server(audio="jack").boot()
	
	a = Sine(freq=.2, mul=.25, add=.5)
	brk = BrkPntOsc(freq=200, brkpnt=a, mul=.2).out()
	
	sc = Scope(brk)
	
	s.gui(locals())
