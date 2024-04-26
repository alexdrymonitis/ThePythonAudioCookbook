from pyo import *

NUM_VOICES = 3

s = Server(audio="jack").boot()

seq = """
; Title: Musica Ricercata III
; Composer: Gyorgi Ligeti
A0 = o6 |: r3 e-1 c e-3 c e-5 c :| \
     r3 e-1 c e-3 c e-5 g
B0 = r3 e-1 c e-3 c e- c o- g e- \
     c o- g o+ c e- g o+ c e- g
#0 t176 v80 x.08 |: A0 B0 :|
A1 = o4 |: c3 r3 r5 r7 :|4
B1 = r9
#1 t176 v80 x.15 |: A1 B1 :|
A2 = o3 |: c3 r3 r5 r7 :|4
B2 = r9
#2 t176 v80 x.15 |: A2 B2 :|
"""

mml = MML(seq, voices=NUM_VOICES).play()

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
