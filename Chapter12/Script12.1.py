import tkinter as tk
import pyo

s = pyo.Server(audio="jack").boot()

sig = pyo.SigTo(200)
osc = pyo.LFO(freq=sig, mul=.2)
mix = pyo.Mix(osc, voices=2).out()

class TkWidgets(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.tickbox_var = tk.IntVar()
		self.tickbox = tk.Checkbutton(
			master, text="DSP",
			variable=self.tickbox_var,
			command=self.tickbox_action,
			font=("Liberation Mono", 10)
		)
		self.tickbox.place(x=50, y=20)

		self.freq_label=tk.Label(
			master,text="Frequency",
			font=("Liberation Mono",15)
		)
		self.freq_label.place(x=50, y=70)
		
		self.slider = tk.Scale(
			master, from_=0.00, to=300.0,
			orient=tk.HORIZONTAL,
			length=300,
			tickinterval=0,resolution=0.01,
			font=("Liberation Mono",10),
			command=self.set_freq
		)
		self.slider.set(200)
		self.slider.place(x=50, y=100)

		self.entry = tk.Entry(
			master, font=("Liberation Mono", 12)
		)
		self.entry.place(x=50, y=150)
		self.entry.bind('<Return>', self.get_freq)

		self.radio_label = tk.Label(
			master, text= " Waveform",
			font=("Liberation Mono", 20)
		)
		self.radio_label.place(x=50, y=200)
		self.waveforms = ["Saw up         ",
						  "Saw down       ",
						  "Square         ",
						  "Triangle       ",
						  "Pulse          ",
						  "Bipolar Pulse  ",
						  "Sample and Hold",
						  "Modulated Sine "]
		self.radio_var = tk.IntVar()
		self.radio=[tk.Radiobutton(
						master,
						text=self.waveforms[i],
						variable=self.radio_var,
						value=i,
						font=("Liberation Mono", 10),
						command=self.radio_func).place(
							x=50,y=210+((i+1)*20)
						) for i in range(len(self.waveforms))]

	############## Tick box ################
	def tickbox_action(self):
		if self.tickbox_var.get()== 1:
			s.start()
		else:
			s.stop()

	################ Slider #################
	def set_freq(self, value):
		sig.setValue(float(value))

	############## Number entry #############
	def get_freq(self, arg):
		sig.setValue(float(self.entry.get()))
		self.entry.delete(0, tk.END)

	################# Radio #################
	def radio_func(self):
		osc.setType(self.radio_var.get())


if __name__ == "__main__":
	root = tk.Tk()
	root.configure(background='light grey')
	root.geometry('400x440')
	TkWidgets(root)
	root.mainloop()
