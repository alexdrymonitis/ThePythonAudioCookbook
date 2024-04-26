from pyo import *

s = Server(audio="jack").boot()

sine = Sine(freq=.5, mul=.5, add=.5)

osc_send=OscDataSend("f",9030,"/1/fader1",host="192.168.43.1")

def sendmsg():
	osc_send.send([sine.get()])


pat = Pattern(sendmsg, time=.01).play()

s.gui(locals())
