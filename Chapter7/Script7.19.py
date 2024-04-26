from pyo import *
import random
import librosa
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import os

NUM_MFCC = 13
PATTHRESH = 0.03
CONF = 0.8

vowels = ["a", "o", "i", "e", "u"]

nn = Sequential()
nn.add(Dense(32, input_shape=(NUM_MFCC,), activation="relu"))
nn.add(Dense(32, activation="relu"))
nn.add(Dense(5, activation="softmax"))

nn.compile(optimizer='adam',
           loss='categorical_crossentropy',
           metrics=['accuracy'])

s = Server(audio="jack").boot()
s.start()

mic = Input()
tab = DataTable(s.getBufferSize())
tabfill = TableFill(mic, tab)

prev_vowel = -1

def get_mfcc():
	mic_array = np.asarray(tab.getBuffer())
	mfcc = librosa.feature.mfcc(y=mic_array,n_mfcc=NUM_MFCC,
                                sr=s.getSamplingRate())
	return mfcc

def train_network(input_data, output_data):
	nn.fit(input_data, output_data,
           batch_size=32, epochs=100,
           validation_split=.1)

def predict():
	global prev_vowel
	# get only first column of MFCC 2D array inside an array
	pred_input = np.full((1, NUM_MFCC), get_mfcc()[:, 0])
	prediction = nn.predict(pred_input, verbose=0)
	predicted_vowel = np.argmax(prediction)
	if prediction[0][predicted_vowel] < CONF:
		pass
	else:
		if predicted_vowel != prev_vowel:
			print(f"prediction: {vowels[predicted_vowel]} ")
			prev_vowel = predicted_vowel

def poll_predictions():
	global prev_vowel
	prev_vowel = -1
	pat.play()

pat = Pattern(predict, time=.1)
follower = Follower(mic)
thresh1 = Thresh(follower, PATTHRESH, dir=0).stop()
thresh2 = Thresh(follower, PATTHRESH, dir=1).stop()
tf1 = TrigFunc(thresh1, poll_predictions)
tf2 = TrigFunc(thresh2, pat.stop)

def save_model(net_name):
	path_to_file = os.getcwd() + "/" + net_name
	nn.save(path_to_file)
	print(f"saved network model in {path_to_file}")

if __name__ == "__main__":
	vowel = None
	mfccs = []
	prompt = "Provide vowel or hit return for snapshot, "
	prompt += "'t' to train, or 'q' to quit: "
	training = True
	while training:
		user_input = input(prompt)
		if user_input == "q":
			exit()
		elif user_input in vowels:
			vowel = vowels.index(user_input)
		elif user_input == "":
			if vowel is None:
				print("No vowel provided yet!")
			else:
				mfccs.append([get_mfcc(), vowel])
		elif user_input == "t":
			if len(mfccs) == 0:
				print("No MFCCs stored yet!")
			else:
				in_data = np.empty((len(mfccs),
                                    mfccs[0][0].shape[0]))
				out_data=np.empty((len(mfccs),len(vowels)))
				random.shuffle(mfccs)
				for i in range(len(mfccs)):
					# get only first column of MFCC
					in_data[i] = mfccs[i][0][:, 0]
					# create one-hot array
					for j in range(len(vowels)):
						out_data[i][j] = 0
					out_data[i][mfccs[i][1]] = 1
				train_network(in_data, out_data)
				training = False

	thresh1.play()
	thresh2.play()
	prompt1 = "Training done, now detecting vowels . . . "
	prompt2 = "Is this a name for saving the model? (y/n): "
	while True:
		user_input = input(prompt1)
		if user_input == "q":
			exit()
		else:
			answer = input(prompt2)
			if answer == "y":
				save_model(user_input)
