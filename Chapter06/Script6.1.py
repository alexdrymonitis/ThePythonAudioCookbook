from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

def default_handler(address, *args):
	print(f"{address}: {args}")

dispatcher = Dispatcher()

dispatcher.set_default_handler(default_handler)

ip = "192.168.43.207"
port = 9020

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()
