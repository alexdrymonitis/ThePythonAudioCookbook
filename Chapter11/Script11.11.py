from pyo import *

s = Server(audio="jack").boot()

expression = """
(load generators.expr)
(load filters.expr)
(var #freq 200)
(var #cutoff 100)
(lowpass (square #freq) #cutoff)
"""

expr = Expr(Sig(0), expression)
sc = Scope(expr)
mix = Mix(expr, voices=2).out()

s.gui(locals())
