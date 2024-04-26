from pyo import *

s = Server(audio="jack").boot()

sample_paths = ["./samples/kick-drum.wav",
                "./samples/snare.wav",
                "./samples/hi-hat.wav"]
# create a three-stream SndTable
snd_tabs = SndTable(sample_paths, chnl=0)
# get a list of the durations
durs = snd_tabs.getDur(all=True)

# create triggering lists
kick_list =  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
snare_list = [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
hat_list =   [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0]
# put all lists in one list
all_lists = [kick_list, snare_list, hat_list]

# get ms from BPM based on meter and pass it to Metro’s arg
metro = Metro(beatToDur(1/4, 120))
mask = Iter(metro, all_lists)
# create a dummy arithmetic object
beat = metro * mask

# create a three-stream TrigEnv()
player = TrigEnv(beat, snd_tabs, dur=durs, mul=.5).out()

def new_list(l, index=0):
	all_lists[index] = l
	mask.setChoice(all_lists)

metro.play()

s.gui(locals())
