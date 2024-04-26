from multiprocessing import Process
import googlemaps
from countryinfo import CountryInfo
import pycountry as cntry
from pythonosc.udp_client import SimpleUDPClient
import pyo
import random

RAMPTIME = 5
ENVDUR = .125

ip= '127.0.0.1'
port = 5100
client = SimpleUDPClient(ip, port)

# the key argument below is left blank as this is private
gmaps = googlemaps.Client(key="")

num_countries = len(cntry.countries)

# minimum and maximum values of latitude and longitude
latminmax = [-85.05115, 85]
lngminmax = [-180, 180]


def mapval(val, inmin, inmax, outmin, outmax):
	inspan = inmax - inmin
	outspan = outmax - outmin
	scaledval = float(val - inmin)/ float(inspan)
	return outmin + (scaledval * outspan)


def getloc_proc(ndx):
	city = None
	while city is None:
		try:
			country = list(cntry.countries)[ndx].name
			city = CountryInfo(country).capital()
		# some countries produce key errors
		# because the function call above results to NoneType
		except KeyError:
			pass
	try:
		geocode = gmaps.geocode(city)
		try:
			lat = geocode[0]['geometry']['location']['lat']
			lng = geocode[0]['geometry']['location']['lng']
			# map the coordinates to the MIDI range
			lat_mapped = mapval(lat, latminmax[0],
			latminmax[1], 0, 127)
			lng_mapped = mapval(lng, lngminmax[0],
			lngminmax[1], 0, 127)
			lat_lng_min = int(min(lat_mapped, lng_mapped))
			# get the difference of the original coords
			# wrapped around 12
			diff = abs(int(lat) - int(lng)) % 12
			feedback = mapval(diff, 0, 11, 0, 0.25)
			taps = int(mapval(diff,0, 11, 1, 24))
			# write the string that will be printed
			print_str = f"{city}: {lat}, {lng} " + \
						f"mapped to: {lat_lng_min} " + \
						f"{lat_lng_min+diff} " + \
						f"with feedback: {feedback} " + \
						f"and taps: {taps}"
			print(print_str)
			list_to_send = [lat_lng_min,
			lat_lng_min+diff,
			feedback, taps]
			client.send_message("/latlng", list_to_send)
		# some cities result in an empty list
		# returned by gmaps.geocode(city)
		except IndexError:
			print(f"Index error with {city}")
	except googlemaps.exceptions.HTTPError:
		print("HTTP error")


def get_latlng():
	proc=Process(
			target=getloc_proc,
			args=(random.randrange(num_countries),)
		 )
	proc.start()


def setvals(address, *args):
	# args is a tuple, so we convert it to a list
	midivals.setValue([args[0], args[1]])
	feedback.setValue(args[2])
	beat.setTaps(args[3])


s = pyo.Server(audio="jack").boot()
midivals = pyo.SigTo([0, 0], time=RAMPTIME/2)
feedback = pyo.SigTo(0, time=RAMPTIME/2)
freqs = pyo.MToF(midivals)
beat = pyo.Euclide(time=ENVDUR).play()
tab=pyo.CosTable([(0,0),(64,1),(1024,1),(4096,0.5),(8191,0)])
env = pyo.TrigEnv(beat, tab, dur=ENVDUR, mul=.5)
sines = pyo.SineLoop(freqs, feedback=feedback, mul=env).out()
oscrecv = pyo.OscDataReceive(5100, "/latlng", setvals)
pat = pyo.Pattern(get_latlng, time=RAMPTIME)
pat.play()
s.gui(locals())
