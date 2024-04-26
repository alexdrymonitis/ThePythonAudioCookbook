from pyfirmata import Arduino, util
from pyo import *

board = Arduino('/dev/ttyACM1')
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

it = util.Iterator(board)
it.start()
analog_pins = [board.get_pin('a:'+str(i)+':i') 
			   for i in range(6)]
switch_pins = [board.get_pin('d:'+str(i+2)+':i') 
			   for i in range(4)]
led_pins = [board.get_pin('d:'+str(i+6)+':o') 
			for i in range(4)]

env = HannTable()
gran = Granulator(snds[0], env, pitch=sigs[0]*2,
				  pos=sigs[1]*snds[0].getSize(),
				  dur=sigs[2], mul=sigs[5]).out()

# turn all LEDs off
for i in range(len(led_pins)):
	led_pins[i].write(0)
# light up first LED
led_pins[0].write(1)


def readvals():
	global prev_led, potvals, prev_grains, prev_basedur
	for i in range(6):
		potvals[i] = analog_pins[i].read()
	sigs.setValue(potvals)
	# set grains and basedur that don't take PyoObjects
	if int(potvals[3]*20+2) != prev_grains:
		prev_grains = int(potvals[3]*20+2)
		gran.setGrains(prev_grains)
	if int(potvals[4]*10+1) != prev_basedur:
		prev_basedur = int(potvals[4]*10+1)
		gran.setBaseDur(prev_basedur/20)
	for i in range(4):
		switchvals[i] = switch_pins[i].read()
		if switchvals[i] != prev_switchvals[i]:
			if switchvals[i] == 1:
				led_pins[i].write(1)
				led_pins[prev_led].write(0)
				prev_led = i
				# set table to granulator
				gran.setTable(snds[i])
				# update pos attribute to get right size
				gran.setPos(sigs[1]*snds[i].getSize())
			# update previous switch value
			prev_switchvals[i] = switchvals[i]


pat = Pattern(readvals, time=.01).play()

s.gui(locals())
