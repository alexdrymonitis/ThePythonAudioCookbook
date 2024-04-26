import music21 as m21
import pyo
import random

BASENOTE = 48
NUMOSC = 2
METER = 4
BASEDUR = 4
MINDUR = 16
BPM = 80

s = pyo.Server(audio="jack").boot()

t = pyo.HarmTable([1, 0.1])

metro = pyo.Metro(time=pyo.beatToDur(1/int(MINDUR/4),BPM))
pyocounter = pyo.Counter(metro)
select = pyo.Select(pyocounter)

param_lists = [[0.33001, 2.9993],
               [0.33003, 2.9992]]

class FM3(pyo.PyoObject):
	def __init__(self,fcar,ratio1,ratio2,mul=1,add=0):
		pyo.PyoObject.__init__(self, mul, add)
		fcar,ratio1,ratio2,\
		mul,add,lmax=pyo.convertArgsToLists(
							fcar,ratio1,
							ratio2,mul,add
						 )
		self._fcar = pyo.Sig(fcar)
		self._fmod = pyo.SigTo(ratio1, mul=self._fcar)
		self._fmodmod = pyo.SigTo(ratio2, mul=self._fmod)
		self._amod = pyo.SigTo(8, mul=self._fmod)
		self._amodmod = pyo.SigTo(4, mul=self._fmodmod)
		self._modmod=pyo.Sine(self._fmodmod,
                              mul=self._amodmod)
		self._mod=pyo.Sine(self._fmod+self._modmod,
                           mul=self._amod)
		self._car = pyo.Osc(t, fcar+self._mod, mul=0.2)
		self._eq=pyo.EQ(self._car,freq=fcar,
                        q=0.707,boost=-12)
		self._out = pyo.DCBlock(self._eq, mul=mul)
		self._base_objs = self._out.getBaseObjects()

class Schoenberg(pyo.PyoObject):
	def __init__(self,id=0,notelist=None,\
                 masklist=None,durlist=None,mul=1,add=0):
		pyo.PyoObject.__init__(self, mul, add)
		self._ratio1 = param_lists[id%2][0]
		self._ratio2 = param_lists[id%2][1]
		self._note_offset = id*12
		self._mask = pyo.Iter(metro, choice=masklist)
		self._beat = metro * self._mask
		self._notes = pyo.Iter(self._beat, choice=notelist)
		self._durs = pyo.Iter(self._beat, choice=durlist)
		self._adsr=pyo.Adsr(dur=pyo.beatToDur(1/MINDUR,BPM),
                            mul=(1/NUMOSC))
		self._tf = pyo.TrigFunc(self._beat, self.adsr_ctl)
		self._fm = FM3(pyo.MToF(self._notes+\
                                (BASENOTE+self._note_offset)),\
                                self._ratio1,self._ratio2,
                                mul=self._adsr)
		self._base_objs = self._fm.getBaseObjects()

	def adsr_ctl(self):
		self._adsr.setDur(pyo.beatToDur(self._durs.get()/\
                                        (MINDUR/4),BPM))
		self._adsr.play()


def rand_durs(n, total):
	dividers = sorted(random.sample(range(1, total), n - 1))
	return [a - b for a, b in zip(dividers + \
           [total], [0] + dividers)]


if __name__ == "__main__":
	# create a random twelve tone line
	serie = [i for i in range(12)]
	random.shuffle(serie)
	# create a string with twelve lines
	# with unique twelve tone lines
	# separated with \n
	series = m21.serial.rowToMatrix(serie)
	# separate the string above to twelve strings
	twelvetone_list = series.split('\n')
	# get a list with twelve lists with integers
	# from the strings above
	matrix = []
	counter = 0
	for line in twelvetone_list:
		matrix.append([])
		splitline = line.split(' ')
		for string in splitline:
			if len(string) > 0:
				matrix[counter].append(int(string))
		counter += 1
	# flatten the 2D list to one 1D list
	matrix_flat = []
	for serie in matrix:
		for note in serie:
			matrix_flat.append(note)

	listlen = int(len(matrix_flat)/NUMOSC)
	notelist = [matrix_flat[i*listlen:(i+1)*listlen]
                for i in range(NUMOSC)]

	durlist = []
	masklist = []
	for i in range(NUMOSC):
		masklist.append([])
		durlist.append([])
		for j in range(int(len(notelist[i])/METER)):
			masklocal = rand_durs(METER, MINDUR)
			for dur in masklocal:
				masklist[i].append(1)
				for k in range(dur-1):
					masklist[i].append(0)
				durlist[i].append(dur)

	# set the maximum count based on the mask list
	pyocounter.setMax(len(masklist[0]))
	select.setValue(len(masklist[0])-1)

	schoenberg = [Schoenberg(i,notelist[i],masklist[i],
                  durlist[i]) for i in range(NUMOSC)]
	mix = pyo.Mix(schoenberg, voices=2).out()

	tf = pyo.TrigFunc(select, metro.stop)

	metro.play()

	s.gui(locals())
