import serial
from pyo import *

ser = serial.Serial('/dev/ttyACM1', 115200)
s = Server().boot()

potvals = [0, 0, 0, 0, 0, 0]
switchvals = [0, 0, 0, 0]
prev_switchvals = [0, 0, 0, 0]
prev_led = 0
prev_grains = 8
prev_basedur = 10

sigs = SigTo([0, 0, 0, 0, 0, 0])

snd_paths = ["./samples/audio_file1.wav",
			 "./samples/audio_file2.wav",
			 "./samples/audio_file3.wav",
			 "./samples/audio_file4.wav"]

snds = [SndTable(snd_paths[i]) for i in range(len(snd_paths))]

env = HannTable()
gran = Granulator(snds[0], env, pitch=sigs[0]/512,
				  pos=(sigs[1]/1023)*snds[0].getSize(),
				  dur=sigs[2]/1023, mul=sigs[5]/1023).out()

def init_leds():
	# turn all LEDs off
	for i in range(4):
		b = bytes(str(i)+"l0v", 'utf-8')
		ser.write(b)
	# light up first LED
	b = bytes("0l1v", 'utf-8')
	ser.write(b)


def readvals():
	global prev_led, potvals, prev_grains, prev_basedur
	while ser.in_waiting:
		# read bytes until newline
		serbytes = ser.readline()
		# strip "b'" and "'" from bytes and convert to string
		serstr = str(serbytes)[2:-1]
		# read potentiometer values
		if serstr.startswith("pots"):
			# trim the "pots " part and split items
			vals = serstr[5:-4].split()
			try:
				# convert strings to integers
				potvals = [eval(i) for i in vals]
				#potvals = list(map(int, vals))
				sigs.setValue(potvals)
				# set attributes that don't take PyoObjects
				if int((potvals[3]/1023)*20+2) != prev_grains:
					prev_grains = int((potvals[3]/1023)*20+2)
					gran.setGrains(prev_grains)
				if int((potvals[4]/1023)*10+1)!=prev_basedur:
					prev_basedur = int((potvals[4]/1023)*10+1)
					gran.setBaseDur(prev_basedur/20)
			except NameError:
				pass
			except SyntaxError:
				pass

		# read switch values
		elif serstr.startswith("switches"):
			# strip "switches " and split items
			vals = serstr[9:-4].split()
			# convert strings to integers
			switchvals = [eval(i) for i in vals]
			for i in range(len(switchvals)):
				# test against previous value of each switch
				if switchvals[i] != prev_switchvals[i]:
					# if value changed and switch is pressed
					if switchvals[i] == 1:
						# turn previous LED off
						b_str = str(prev_led)+"l0v"
						# and current on
						b_str += str(i)+"l1v"
						b = bytes(b_str, 'utf-8')
						ser.write(b)
						# update prev_led
						prev_led = i
						# set table to granulator
						gran.setTable(snds[i])
						# update pos to get right size
						gran.setPos((sigs[1]/1023)*\
									snds[i].getSize())
					# update previous switch value
					prev_switchvals[i] = switchvals[i]

# light up the first LED
ca = CallAfter(init_leds, time=.5)

pat = Pattern(readvals, time=.01).play()

s.gui(locals())
