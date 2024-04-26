from pyo import *

s = Server(audio="jack").boot()

mic = Input()
deltime = Sine(freq=[.1, .12], mul=.015, add=.04)
feedback = Sine(freq=[.09, .11], mul=.045, add=.855)
delay=Delay(mic,delay=deltime,feedback=feedback,mul=.2).out()

s.gui(locals())
