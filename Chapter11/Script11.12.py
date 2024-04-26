from pyo import *

s = Server(audio="jack").boot()

expression = """
(var #freq 440)
(var #fb 0.1)
(define triangle (
		(let #ph (wrap (+ (~ #freq) (* $1 #fb))))
		(- (* (min #ph (- 1 #ph)) 4) 1)
	)
)
(triangle $y[-1])
"""

expr = Expr(Sig(0), expression, mul=0.5)
sc = Scope(expr)

mix = Mix(expr, voices=2).out()

s.gui(locals())
