from pyfirmata import Arduino, util
from pyo import *

board = Arduino('/dev/ttyACM1')
s = Server().boot()

it = util.Iterator(board)
it.start()

analog_pins = [board.get_pin('a:0:i'), board.get_pin('a:1:i')]

sigs = SigTo([0, 0])
a = SineLoop(freq=MToF(sigs[0]),feedback=.1,mul=sigs[1]).out()

min_thresh = 0.2
max_thresh = 0.65
sensor_range = max_thresh - min_thresh

def readvals():
	for i in range(2):
		val = analog_pins[i].read()
		if val > max_thresh: val = max_thresh
		val -= min_thresh
		if val < 0: val = 0
		val /= sensor_range
		if i == 0:
			val *= 127
		sigs[i].setValue(val)
    
def close():
	pat.stop()
	board.exit()

pat = Pattern(readvals, time=.01).play()
s.gui(locals())
