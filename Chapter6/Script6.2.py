from pyo import *

s = Server(audio="jack").boot()

def print_osc_data(address, *args):
	if address == "/3/xy":
		print(f"{address}: {args[0]}, {args[1]}")
	else:
		print(f"{address}: {args[0]}")


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

osc_recv = OscDataReceive(9020, addresses, print_osc_data)

s.gui(locals())
