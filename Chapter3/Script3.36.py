from pyo import *
import random

s = Server(audio="jack").boot()

def create_list():
	# create a list of ten random integers
	# from 0 to 512 without repetitions
	rand_idx = random.sample([i for i in range(512)], 10)
	# create a list of tuples with the random integers
	# and a random float
	rand_list = [(rand_idx[i], random.random())
                 for i in range(len(rand_idx))]
	# sort the list in ascending order
	rand_list.sort()
	list_w_zeros = []

	for i in range(len(rand_list)):
		# if the index of the first item
		# of the list is greater than 0
		if i == 0 and rand_list[i][0] > 0:
			# go half way between index and beginning
			index = int(rand_list[i][0] / 2)
			# add a 0 value to half way index
			list_w_zeros.append((index, 0))
		# if successive indexes are separated
		# with index difference greater than 1
		elif rand_list[i][0] - rand_list[i-1][0] > 1:
			# go half way between indexes
			index=int((rand_list[i][0]-rand_list[i-1][0])/2)
			# add offset to place index at correct spot
			index += rand_list[i-1][0]
			# add a zero value to that index
			list_w_zeros.append((index, 0))
		# add the tuple of the original list
		list_w_zeros.append(rand_list[i])
	# add a list tuple between last item and end of table
	if rand_list[-1:][0][0] < 511:
		index = int((512 - rand_list[-1:][0][0]) / 2)
		index += rand_list[-1:][0][0]
		list_w_zeros.append((index, 0))
	return list_w_zeros

list_w_zeros = create_list()

# create a list from a set() to remove duplicates
no_rep = [*set(list_w_zeros)]
# sort list as set() shuffles items
no_rep.sort()

noise = Noise(.25).mix(2)
fft = FFT(noise, size=1024, overlaps=4, wintype=2)
tab = ExpTable(no_rep, size=512)
amp = TableIndex(tab, fft["bin"])
real = fft["real"] * amp
imag = fft["imag"] * amp
ifft = IFFT(real, imag, size=1024, overlaps=4,
            wintype=2).mix(2).out()

tab.graph()

s.gui(locals())
