from pyo import *

s = Server(audio="jack").boot()
s.start()

pm_list_devices()
