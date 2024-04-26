from pyo import *

s = Server(audio="jack").boot()

expression = """
(let #rm (* $x0[0] $x1[0])) // Ring Modulation
(out 0 #rm)
(out 1 (* #rm (+ (* $x2[0] 0.5) 0.5)))
"""

rm_in1 = Sine(freq=200)
rm_in2 = SineLoop(freq=52.7, feedback=0.08)
rm_in3 = RCOsc(freq=180)
rm_in4 = SuperSaw(freq=53.2)
am_in = LFO(freq=.5, type=3)
expr_in = InputFader([rm_in1, rm_in2, am_in])
expr = Expr(expr_in, expression, outs=2, mul=0.5).out()
sc = Scope(expr)

s.gui(locals())
