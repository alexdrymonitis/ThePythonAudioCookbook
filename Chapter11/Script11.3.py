from pyo import *

NUM_VOICES = 2

s = Server(audio="jack").boot()

seq = """
A = o?{4,6} (?[c e g] ?[c e g] ?[c e g])5 \
    ?[c e g]7 ?[c e g]5
B = o?{4,6} (?[d f a] ?[d f a] ?[d f a] ?[d f a] ?[d f a])7 \
    |: ?[d f+ a]5 :|
#0 t120 v60 x.02 A B
BEAT = o7 |: a5 :|4
#1 t120 v60 x.08 BEAT
"""

mml = MML(seq, voices=NUM_VOICES, loop=True).play()

tab = CosTable([(0,0),(64,1),(1024,1),(4096, 0.5),(8191,0)])
envs = [TrigEnv(mml.getVoice(i), table=tab,
                dur=mml.getVoice(i, "dur"),
                mul=mml.getVoice(i, "amp"))
        for i in range(NUM_VOICES)]
voices = [SineLoop(freq=mml.getVoice(i, "freq"),
                   feedback=mml.getVoice(i, "x"),
                   mul=envs[i]).mix(2).out()
          for i in range(NUM_VOICES)]

s.gui(locals())
