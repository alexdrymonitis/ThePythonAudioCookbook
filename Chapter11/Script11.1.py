from pyo import *

s = Server(audio="jack").boot()

seq = """
A = o5 c3 d e f+ g a b o+ c
B = o4 b3 o+ c5 o-2 d3 e5 f+3 g
#0 t92 v60 A B
"""

mml = MML(seq, voices=1).play()

tab = CosTable([(0,0),(64,1),(1024,1),(4096, 0.5),(8191,0)])
env = TrigEnv(mml.getVoice(0), table=tab,
              dur=mml.getVoice(0, "dur"),
              mul=mml.getVoice(0, "amp"))
sine = Sine(freq=mml.getVoice(0, "freq"),mul=env).mix(2).out()

s.gui(locals())
