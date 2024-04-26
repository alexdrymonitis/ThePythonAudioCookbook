import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import pyo

s = pyo.Server(audio="jack").boot()

sig = pyo.SigTo(200)
osc = pyo.LFO(freq=sig, mul=.2)
mix = pyo.Mix(osc, voices=2).out()

class PyoWidgets(QWidget):
	def __init__(self):
		super().__init__()

		fontid=QFontDatabase.addApplicationFont(
								"DroidSansMono.ttf"
							 )
		if fontid < 0:
			print("Error loading font, exiting . . . ")
			exit()
		fontstr = QFontDatabase.applicationFontFamilies(
									fontid

								)
		self.layout = QVBoxLayout()

		self.waveforms = ["Saw up",
						  "Saw down",
						  "Square",
						  "Triangle",
						  "Pulse",
						  "Bipolar Pulse",
						  "Sample and Hold",
						  "Modulated Sine"]

		self.tickbox = QCheckBox("DSP")
		self.tickbox.setChecked(False)
		self.tickbox.stateChanged.connect(self.tickbox_state)
		self.tickbox.setFont(QFont(fontstr[0], 10))
		self.layout.addWidget(self.tickbox)

		self.freqlabel = QLabel("Frequency")
		self.freqlabel.setAlignment(
						Qt.AlignmentFlag.AlignLeft
					   )
		self.freqlabel.setFont(QFont(fontstr[0], 20))
		self.layout.addWidget(self.freqlabel)

		self.slider = QSlider(Qt.Orientation.Horizontal)
		self.slider.setMinimum(0)
		self.slider.setMaximum(300)
		self.slider.setValue(200)
		self.layout.addWidget(self.slider)
		self.slider.valueChanged.connect(self.valuechange)

		self.freqentry = QLineEdit()
		self.freqentry.setPlaceholderText("Frequency")
		self.freqentry.returnPressed.connect(self.freqset)
		self.freqentry.setFont(QFont(fontstr[0], 12))
		self.layout.addWidget(self.freqentry)

		self.wavelabel = QLabel("Waveform")
		self.wavelabel.setAlignment(
						Qt.AlignmentFlag.AlignLeft
					   )
		self.wavelabel.setFont(QFont(fontstr[0], 20))
		self.layout.addWidget(self.wavelabel)

		self.radio = [QRadioButton(i)
					  for i in self.waveforms]
		for i in range(len(self.radio)):
			self.radio[i].setChecked(i == 0)
			self.radio[i].index = i
			self.radio[i].toggled.connect(self.set_waveform)
			self.radio[i].setFont(QFont(fontstr[0], 8))
			self.layout.addWidget(self.radio[i])

		self.setLayout(self.layout)
		self.setWindowTitle("Pyo")

	def valuechange(self):
		freq = self.slider.value()
		sig.setValue(freq)

	def freqset(self):
		freq = float(self.freqentry.text())
		self.freqentry.clear()
		sig.setValue(freq)

	def tickbox_state(self):
		if self.tickbox.isChecked():
			s.start()
		else:
			s.stop()

	def set_waveform(self):
		for r in self.radio:
			if r.isChecked():
				osc.setType(r.index)
				break


if __name__ == '__main__':
	app = QApplication(sys.argv)
	widgets = PyoWidgets()
	widgets.show()
	sys.exit(app.exec())
