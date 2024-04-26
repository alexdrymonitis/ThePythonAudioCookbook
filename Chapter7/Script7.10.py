from pyo import *
import random
from pynput import mouse, keyboard
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import time, os

AUGSIZE = 200
NUMGENS = 4
POLLFR = 0.05

nn = Sequential()
nn.add(keras.Input(shape=(2,)))
nn.add(Dense(64, activation="sigmoid"))
nn.add(Dense(64, activation="sigmoid"))
nn.add(Dense(NUMGENS*5, activation="linear"))

nn.compile(optimizer='adam',loss="mean_squared_error",
           metrics=['accuracy'])

s = Server(audio="jack").boot()

t = HarmTable([1, 0.1])

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

	def setnew(self, fcar, ratio1, ratio2, ndx1, ndx2):
		self.fcar.setValue(float(fcar*denoms[0]))
		self.fmod.setValue(float(ratio1))
		self.fmod.setMul(float(fcar)*denoms[0])
		self.fmodmod.setValue(float(ratio2)*denoms[2])
		self.amod.setValue(int(ndx1*denoms[3]))
		self.amodmod.setValue(int(ndx2*denoms[4]))

	def setrand(self):
		fcar = random.randrange(100, 300)
		ratio1 = random.random()
		ratio2 = random.random() * 3 + 1
		ndx1 = random.randrange(1, 12)
		ndx2 = random.randrange(1, 8)
		self.fcar.setValue(fcar)
		self.fmod.setValue(ratio1)
		self.fmod.setMul(fcar)
		self.fmodmod.setValue(ratio2)
		self.amod.setValue(ndx1)
		self.amodmod.setValue(ndx2)
		return [fcar, ratio1, ratio2, ndx1, ndx2]

param_lists = [[125.00, 0.33001, 2.9993, 8, 4, 0],
               [125.08, 0.33003, 2.9992, 8, 4, 1],
               [249.89, 0.33004, 2.9995, 8, 4, 0],\
               [249.91, 0.33006, 2.9991, 8, 4, 1]]
fm3 = [FM3(*param_lists[i]) for i in range(NUMGENS)]

poll_stamp = time.time()

mouse_x = 0
mouse_y = 0

mouse_coords = []
synth_params = []
temp_synth_params = []
training_data= []
# create two variable to store numpy arrays later
training_input_data = None
training_output_data = None

# boolean to determine if we want to predict
predicting = False

# denominators for parameter normalization
denoms = [300, 1, 4, 12, 8]

def setrand():
	l = []
	for i in range(NUMGENS):
		l.append(fm3[i].setrand())
	return l

def augment_data():
	global training_input_data, training_output_data
	training_input_data = np.empty((len(mouse_coords)*\
                                   AUGSIZE,2))
	training_output_data=np.empty((len(mouse_coords)*\
                                  AUGSIZE, NUMGENS*5))
	for i in range(len(mouse_coords)):
		for j in range(AUGSIZE):
			training_data.append([])
			mouse_x_rand = mouse_coords[i][0] + \
                           random.randrange(20)
			mouse_y_rand = mouse_coords[i][1] + \
                           random.randrange(20)
			# normalize according to screen resolution
			mouse_x_rand /= 1919
			mouse_y_rand /= 1079
			# make sure values don’t exceed 1
			if mouse_x_rand > 1.0: mouse_x_rand = 1.0
			if mouse_y_rand > 1.0: mouse_y_rand = 1.0
			training_data[(i*AUGSIZE)+j].append(mouse_x_rand)
			training_data[(i*AUGSIZE)+j].append(mouse_y_rand)
			# normalize target output based on denoms list
			for group in synth_params[i]:
				for n, param in enumerate(group):
					training_data[(i*AUGSIZE)+\
                                  j].append(param/denoms[n])
	# shuffle the training data set for better training
	random.shuffle(training_data)
	# then separate the input from the output data
	for ndx1, item in enumerate(training_data):
		for ndx2, num in enumerate(item):
			if ndx2 < 2:
				training_input_data[ndx1][ndx2] = num
			else:
				training_output_data[ndx1][ndx2-2] = num

def on_move(x, y):
	global mouse_x, mouse_y, poll_stamp
	mouse_x = x
	mouse_y = y
	if predicting:
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
			for i in range(NUMGENS):
				# call each FM object
				# with the correct array portion
				fm3[i].setnew(*predictions[0][i*5:(i*5)+5])

def on_press(key):
	global temp_synth_params, predicting
	try:
		if key.char == 'r':
			temp_synth_params = setrand()
		elif key.char == 's':
			synth_params.append(temp_synth_params)
			mouse_coords.append([mouse_x, mouse_y])
		elif key.char == 'd':
			# when we press the d key
			# we augment the training data
			augment_data()
			# we stop listening to the keyboard
			keyboard_listener.stop()
			# and we train the neural network
			# using 10% for validation
			nn.fit(training_input_data,
                   training_output_data,
                   batch_size=32, epochs=300,
                   validation_split=.1)
			print("training done!")
			predicting = True
	# except errors from certain keys
	except AttributeError:
		pass

mouse_listener = mouse.Listener(on_move=on_move)
mouse_listener.start()

keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# when done training we can save the model
def save_model(net_name):
	path_to_file = os.getcwd() + "/" + net_name
	nn.save(path_to_file)
	print(f"saved network model in {path_to_file}")

s.gui(locals())
