from pyo import *

s = Server(audio="jack").boot()

expression = """
(var #cutoff 100)
(define lowpass (
	(let #coef (exp (/ (* (neg twopi) #cutoff) sr)))
	(rpole (* $1 (- 1 #coef)) #coef)
	)
)
(lowpass $x[0])
"""

expr = Expr(Noise(), expression)
sp = Spectrum(expr)
mix = Mix(expr, voices=2).out()

s.gui(locals())
