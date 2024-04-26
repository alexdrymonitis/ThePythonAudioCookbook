from pyo import *
from pynput import mouse
from tensorflow import keras
import numpy as np
import time
import sys, os

path_to_model = None

if len(sys.argv) == 1:
	path_to_model = input("Provide path to Keras model: ")
	path_to_model = os.getcwd() + "/" + path_to_model
elif len(sys.argv) > 2:
	print("This script takes one argument only")
	exit()
else:
	path_to_model = os.getcwd() + "/" + sys.argv[1]

NUMGENS = 4
POLLFR = 0.05

poll_stamp = time.time()

# denominators for parameter normalization
denoms = [300, 1, 4, 12, 8]

s = Server(audio="jack").boot()

t = HarmTable([1, 0.1])

param_lists = [[125.00, 0.33001, 2.9993, 8, 4, 0],
               [125.08, 0.33003, 2.9992, 8, 4, 1],
               [249.89, 0.33004, 2.9995, 8, 4, 0],
               [249.91, 0.33006, 2.9991, 8, 4, 1]]


class FM3:
	def __init__(self,fcar,ratio1,ratio2,ndx1,ndx2,out=0):
		self.fcar = SigTo(fcar, time=POLLFR)
		self.fmod = SigTo(ratio1, mul=fcar, time=POLLFR)
		self.fmodmod = SigTo(ratio2,mul=self.fmod,time=POLLFR)
		self.amod = SigTo(ndx1, mul=self.fmod, time=POLLFR)
		self.amodmod=SigTo(ndx2,mul=self.fmodmod,time=POLLFR)
		self.modmod = Sine(self.fmodmod, mul=self.amodmod)
		self.mod = Sine(self.fmod+self.modmod, mul=self.amod)
		self.car = Osc(t, fcar + self.mod, mul=0.2)
		self.eq = EQ(self.car, freq=fcar, q=0.707, boost=-12)
		self.out = DCBlock(self.eq).out(out)

	def setnew(self, fcar, ratio1, ratio2, index1, index2):
		self.fcar.setValue(float(fcar*denoms[0]))
		self.fmod.setValue(float(ratio1))
		self.fmod.setMul(float(fcar)*denoms[0])
		self.fmodmod.setValue(float(ratio2)*denoms[2])
		self.amod.setValue(int(index1*denoms[3]))
		self.amodmod.setValue(int(index2*denoms[4]))


# create the FM objects list
fm3 = [FM3(*param_lists[i]) for i in range(NUMGENS)]


def on_move(x, y):
	global poll_stamp
	# get current time stamp
	new_stamp = time.time()

	# make sure enough time has elapsed
	if (new_stamp - poll_stamp) > POLLFR:
		# update time stamp
		poll_stamp = new_stamp
		# create a numpy array with mouse coordinates
		pred_input = np.full((1, 2), [x/1919, y/1079])
		# ask network for predictions
		predictions = nn(pred_input).numpy()
		# call each FM object with the correct array portion
		for i in range(NUMGENS):
			fm3[i].setnew(*predictions[0][i*5:(i*5)+5])

# load the saved model
nn = keras.models.load_model(path_to_model)
print(f"loaded {path_to_model}")

mouse_listener = mouse.Listener(on_move=on_move)
mouse_listener.start()

s.gui(locals())
