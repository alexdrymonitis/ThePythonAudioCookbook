from pyo import *

s = Server(audio="jack").boot()

mic = Input()
follower = Follower(mic)
p = Print(follower, interval=0.5)

s.gui(locals())
