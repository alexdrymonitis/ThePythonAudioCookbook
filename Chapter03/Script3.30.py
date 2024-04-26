from pyo import *

s = Server(audio="jack")

s.setMidiInputDevice(3)
s.boot()

def ctl_scan(ctlnum):
	print(ctlnum)

a = CtlScan(ctl_scan)

s.gui(locals())
