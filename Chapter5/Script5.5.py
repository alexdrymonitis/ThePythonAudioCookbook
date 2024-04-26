import serial
from pyo import *

ser = serial.Serial('/dev/ttyACM1', 115200)
s = Server().boot()

sigs = SigTo([0, 0])
a = SineLoop(freq=MToF(sigs[0]),feedback=.1,mul=sigs[1]).out()

min_thresh = 80
max_thresh = 600
sensor_range = max_thresh - min_thresh

def readvals():
	while ser.in_waiting:
		serbytes = ser.readline()
		serstr = str(serbytes)[2:-1]
		if serstr.startswith("sens"):
			index = int(serstr[4:5])
			# strip "sens " from the beginning
			# and "\r\n" from the end
			val = int(serstr[6:-4])
			if val > max_thresh: val = max_thresh
			val -= min_thresh
			if val < 0: val = 0
			val /= sensor_range
			if index == 0:
				val *= 127
			sigs[index].setValue(val)
    
def close():
	pat.stop()
	ser.close()

pat = Pattern(readvals, time=.01).play()
s.gui(locals())
