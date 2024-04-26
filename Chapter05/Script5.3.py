import serial
from pyo import *

ser = serial.Serial('/dev/ttyACM1', 115200)
s = Server().boot()

amp = SigTo(0)
a = Sine(freq=440, mul=amp).out()

min_thresh = 80
max_thresh = 600
sensor_range = max_thresh - min_thresh

def readval():
	# check if there is data in the serial buffer
	while ser.in_waiting:
		# read bytes until a newline character '\n'
		serbytes = ser.readline()
		# strip b' from the beginning of the string
		# and the ' at the end of it
		serstr = str(serbytes)[2:-1]
		# if there is more than just the return and mewline
		if len(serstr) > 4:
			# strip "\r\n" from the end
			val = int(serstr[:-4])
			if val > max_thresh: val = max_thresh
			val -= min_thresh
			if val < 0: val = 0
			val /= sensor_range
			amp.setValue(val)
    
def close():
	pat.stop()
	ser.close()

pat = Pattern(readval, time=.01).play()
s.gui(locals())
