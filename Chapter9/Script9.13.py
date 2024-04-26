import music21 as m21
import pyo
import random

s = pyo.Server(audio="jack").boot()

metro = pyo.Metro()
pyocounter = pyo.Counter(metro)
select = pyo.Select(pyocounter)

class BachOsc(pyo.PyoObject):
	def __init__(self,num_parts=1,parsed_notes=None,
                 masklist=None,mul=1,add=0):
		pyo.PyoObject.__init__(self, mul, add)
		# convert arguments to lists
		mul,add,lmax = pyo.convertArgsToLists(mul,add)
		self._mask = pyo.Iter(metro, choice=masklist)
		self._select_on = pyo.Select(self._mask, value=1)
		self._select_off = pyo.Select(self._mask, value=2)
		self._adsr = pyo.Adsr(mul=1/num_parts)
		self._tf_on = pyo.TrigFunc(self._select_on,
                                   self._adsr.play)
		self._tf_off = pyo.TrigFunc(self._select_off,
                                    self._adsr.stop)
		self._freqs = pyo.Iter(self._select_on,
                               choice=parsed_notes)
		self._out = pyo.FM(carrier=self._freqs,ratio=.5012,
                           index=1,mul=self._adsr)
		self._base_objs = self._out.getBaseObjects()


def parse_score(num_parts, part_stream):
	parsed_notes = [[]for i in range(num_parts)]
	parsed_durs = [[]for i in range(num_parts)]
	# set a whole note as a starting point
	metro_time = 4
	for i in range(num_parts):
		for note in part_stream[i].flat.notesAndRests:
			if type(note) == m21.note.Note:
				parsed_notes[i].append(note.pitch.frequency)
			elif type(note) == m21.note.Rest:
				parsed_notes[i].append(-1)
			if note.duration.quarterLength < metro_time:
				metro_time = note.duration.quarterLength
			parsed_durs[i].append(
							note.duration.quarterLength
						   )
	return parsed_notes, parsed_durs, metro_time


def get_num_steps(parsed_durs,metro_time):
	# all parts have the same number of steps
	# so we query the first one only
	num_steps = 0
	for i in parsed_durs[0]:
		num_steps += int(i/metro_time)
	return num_steps


def add_stop_vals(l):
	# store the indexes with a 1
	ones_ndx = []
	if l[0] == 1:
		ones_ndx.append(0)
	for i in range(len(l)):
		for j in range(i, len(l)):
			if l[i] == 1 and j > i and l[j] == 1:
				ones_ndx.append(j)
				break
	# then double the size of the list
	for i in range(len(l)):
		l.append(0)
	# and double the values of the stored indexes
	for i in range(len(ones_ndx)):
		ones_ndx[i] *= 2
	# place the ones in the new indexes
	for i in range(len(l)):
		l[i] = 0
		if i in ones_ndx:
			l[i] = 1
	# and a 2 (the stop value) before each 1
	for i in ones_ndx:
		if i > 0:
			l[i-1] = 2
	return l


def get_mask(num_parts, num_steps, metro_time):
	part_events = [[] for i in range(num_parts)]
	masklist = [[] for i in range(num_parts)]
	for i in range(num_parts):
		event = 0
		part_events[i].append(0)
		for j in parsed_durs[i]:
			event += j/metro_time
			part_events[i].append(int(event))
	for i in range(num_parts):
		for j in range(num_steps):
			if j in part_events[i]:
				masklist[i].append(1)
			else:
				masklist[i].append(0)
	# iterate through the list and zero any entry with a rest
	ndx = 0
	for i in range(len(masklist)):
		if masklist[i] == 1:
			if parsed_notes[ndx] < 0:
				masklist[i] = 0
				ndx += 1
	# double masklist to include a 2
	# for stopping the envelope
	# we need to double so that even
	# the minimum duration can work
	for part in range(num_parts):
		masklist[part] = add_stop_vals(masklist[part])
		# add a 2 at the end to stop when done
		masklist[part][len(masklist[part])-1] = 2
	return masklist


if __name__ == "__main__":
	allBach = m21.corpus.search('bach')
	x = allBach[random.randrange(len(allBach))]

	bach = x.parse()
	part_stream = bach.parts.stream()
	parts = []
	num_parts = len(part_stream)
	# get the tempo from the score
	tempo = bach.metronomeMarkBoundaries()[0][2].number
	# parse the notes from the score
	parsed_notes,parsed_durs,metro_time=parse_score(
											num_parts,
											part_stream
										)
	# get the total number of steps of the sequencer
	num_steps = get_num_steps(parsed_durs,metro_time)

	masklist = get_mask(num_parts,num_steps,metro_time)
	# halve the time to stay in tempo with the new mask list
	metro_time /= 2
	metro.setTime(pyo.beatToDur(1/(1/metro_time),tempo))
	pyocounter.setMax(len(masklist[0])+1)
	select.setValue(len(masklist[0]))
	tf = pyo.TrigFunc(select, metro.stop)

	bach_osc = [BachOsc(num_parts,parsed_notes[i],
                        masklist[i]) for i in range(num_parts)]
	mix = pyo.Mix(bach_osc, voices=2).out()

	s.start()

	ca = pyo.CallAfter(metro.play, time=5)
	bach.show()
