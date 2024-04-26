from pyo import *

s = Server(audio="jack").boot()

sine = Sine(freq=.5, mul=.5, add=.5)

osc_send = OscSend(sine, port=9030, address="/1/fader1",
                   host="192.168.43.1")

s.gui(locals())
