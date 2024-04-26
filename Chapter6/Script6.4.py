from pyo import *

s = Server(audio="jack").boot()

addresses = []
for i in range(5):
	addresses.append("/1/fader"+str(i+1))

osc_recv = OscReceive(9020, addresses)

sine = CrossFM(carrier=osc_recv[addresses[0]]*200,
               ratio=osc_recv[addresses[1]],
               ind1=osc_recv[addresses[2]]*8,
               ind2=osc_recv[addresses[3]]*8,
               mul=osc_recv[addresses[4]]*0.5).mix(2).out()

s.gui(locals())
