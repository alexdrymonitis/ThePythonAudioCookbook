import pyo
import music21 as m21
import random

s = pyo.Server(audio="jack").boot()

class BachOsc(pyo.EventInstrument):
	def __init__(self, **kwargs):
		pyo.EventInstrument.__init__(self, **kwargs)
		self.output=pyo.FM(carrier=self.freq,
						   ratio=.5012,index=1,
						   mul=self.env*self.mul).mix(2).out()


def parse_score(num_parts, part_stream):
	parsed_notes = [[] for i in range(num_parts)]
	parsed_durs = [[] for i in range(num_parts)]
	for i in range(num_parts):
		for note in part_stream[i].flat.notesAndRests:
			if type(note) == m21.note.Note:
				parsed_notes[i].append(note.pitch.frequency)
			elif type(note) == m21.note.Rest:
				parsed_notes[i].append(-1)
			parsed_durs[i].append(note.duration.quarterLength)
	return parsed_notes, parsed_durs


if __name__ == "__main__":
	allBach = m21.corpus.search('bach')
	x = allBach[random.randrange(len(allBach))]

	bach = x.parse()
	part_stream = bach.parts.stream()
	num_parts = len(part_stream)
	# get the tempo from the score
	tempo = bach.metronomeMarkBoundaries()[0][2].number
	# parse the notes from the score
	parsed_notes,parsed_durs=parse_score(
								num_parts,part_stream
							 )

	events = [pyo.Events(
		instr=BachOsc,
		mul=1/num_parts,
		freq=pyo.EventSeq(parsed_notes[i]),
		beat=pyo.EventSeq(parsed_durs[i], occurrences=1),
		bpm=tempo
	).play(delay=5) for i in range(num_parts)]

	s.start()

	bach.show()
