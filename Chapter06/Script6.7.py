from pyo import *

s = Server(audio="jack").boot()

sample_paths = ["./samples/kick-drum.wav",
                "./samples/snare.wav",
                "./samples/hi-hat.wav"]
# create a three-stream SndTable, and read only channel 0
snd_tabs = SndTable(sample_paths, chnl=0)
# get a list of the durations
durs = snd_tabs.getDur(all=True)

# create a single list for all three samples
all_lists = [[0 for i in range(16)] for i in range(3)]

# get ms from BPM based on meter
metro = Metro(beatToDur(1/4, 120))
mask = Iter(metro, all_lists)
# create a dummy arithmetic object
beat = metro * mask

# create a three-stream TrigEnv()
player = TrigEnv(beat, snd_tabs, durs, mul=.5)
mix = Mix(player.mix(1), 2).out()

def new_list(address, *args):
	all_lists[args[0]][args[1]] = args[2]
	mask.setChoice(all_lists)


counter = Counter(metro, max=16)

osc_recv = OscDataReceive(12345, "/seq", new_list)
osc_send = OscSend(counter, port=9030,
                   address="/seq",host="127.0.0.1")

metro.play()

s.gui(locals())
