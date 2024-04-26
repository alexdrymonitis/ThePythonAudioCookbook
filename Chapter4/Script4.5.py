from pyo import *
import random

s = Server(audio="jack").boot()

def create_list():
	rand_idx = random.sample([i for i in range(512)], 10)
	rand_list = [(rand_idx[i], random.random()) for i in
                 range(len(rand_idx))]
	rand_list.sort()
	list_w_zeros = []

	for i in range(len(rand_list)):
		if i == 0 and rand_list[i][0] > 0:
			index = int(rand_list[i][0] / 2)
			list_w_zeros.append((index, 0))
		elif rand_list[i][0] - rand_list[i-1][0] > 1:
			index=int((rand_list[i][0]-rand_list[i-1][0])/2)
			index += rand_list[i-1][0]
			list_w_zeros.append((index, 0))
		list_w_zeros.append(rand_list[i])
	if rand_list[-1:][0][0] < 511:
		index = int((512 - rand_list[-1:][0][0]) / 2)
		index += rand_list[-1:][0][0]
		list_w_zeros.append((index, 0))
	return list_w_zeros

list_w_zeros = create_list()

no_rep = [*set(list_w_zeros)]
no_rep.sort()

noise = Noise(.25).mix(2)
pva = PVAnal(noise)
tab = ExpTable(no_rep, size=512)
pvf = PVFilter(pva, tab)
pvs = PVSynth(pvf).out()

tab.graph()

s.gui(locals())
