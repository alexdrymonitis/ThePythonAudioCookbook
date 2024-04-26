from pyo import *

s = Server(audio="jack").boot()

sigs = SigTo([0, 0, 0, 0, 0])

def ctrl_xfm(address, *args):
	if "/1/fader" in address:
		index = int(address[-1:]) - 1
		sigs[index].setValue(args[0])


addresses = []
for i in range(5):
	addresses.append("/1/fader"+str(i+1))

for i in range(4):
	addresses.append("/1/toggle"+str(i+1))

for i in range(16):
	addresses.append("/2/push"+str(i+1))

for i in range(4):
	addresses.append("/2/toggle"+str(i+1))

addresses.append("/3/xy")

for i in range(4):
	addresses.append("/3/toggle"+str(i+1))

for i in range(8):
	for j in range(8):
		addr_str = "/4/multitoggle/"+str(i+1)+"/"+str(j+1)
		addresses.append(addr_str)

for i in range(4):
	addresses.append("/4/toggle"+str(i+1))

osc_recv = OscDataReceive(9020, addresses, ctrl_xfm)

sine = CrossFM(carrier=sigs[0]*200, ratio=sigs[1],
               ind1=sigs[2]*8, ind2=sigs[3]*8,
               mul=sigs[4]*0.5).mix(2).out()

s.gui(locals())
