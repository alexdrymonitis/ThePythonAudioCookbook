from pyfirmata import Arduino, util
from pyo import *

board = Arduino('/dev/ttyACM1')
s = Server().boot()

# create an iterator thread to not constantly
# send data to serial until it overflows
it = util.Iterator(board)
it.start()
# initialize the pin you want to read
# 'a' means analog, 0 is the pin nr
# and 'i' means input
analog_pin = board.get_pin('a:0:i')

amp = SigTo(0)
a = Sine(freq=440, mul=amp).out()

min_thresh = 0.2
max_thresh = 0.65
sensor_range = max_thresh - min_thresh

def readval():
	val = analog_pin.read()
	if val > max_thresh: val = max_thresh
	val -= min_thresh
	if val < 0: val = 0
	val /= sensor_range
	amp.setValue(val)
    
def close():
	pat.stop()
	board.exit()

pat = Pattern(readval, time=.01).play()
s.gui(locals())
