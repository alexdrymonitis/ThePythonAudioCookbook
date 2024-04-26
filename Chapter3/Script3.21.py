from pyo import *

s = Server(audio="jack").boot()

sample = SfPlayer(SNDS_PATH + "/transparent.aif", loop=True,
                  mul=.3).mix(2).out()
delay = Delay(sample,delay=[.15,.2],feedback=.5,mul=.4).out()

s.gui(locals())
