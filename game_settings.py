from PySide6 import QtWidgets, QtCore

class Game_Settings:
    audio_vol = 1
	
class SettingsWindow(QtWidgets.QDialog):
	def __init__ (self, parent):
		super().__init__(parent)
		self.setWindowTitle ("Settings - Audio")
		self.resize (600,300)
		self.vbox = QtWidgets.QVBoxLayout(self)
		self.hbox_audio = QtWidgets.QHBoxLayout()
		
		self.audio_label = QtWidgets.QLabel("Audio : ")
		self.audio_slider = QtWidgets.QSlider()
		
		self.audio_slider.setRange(0, 100)
		self.audio_slider.setSliderPosition(Game_Settings.audio_vol * 100)
		self.audio_slider.setOrientation(QtCore.Qt.Horizontal)
		
		self.hbox_audio.addWidget(self.audio_label, alignment=QtCore.Qt.AlignLeft)
		self.hbox_audio.addWidget(self.audio_slider)
		self.vbox.addLayout (self.hbox_audio)
		
		self.bottom_buttons()
		
	def bottom_buttons (self):
		self.frame_buttons = QtWidgets.QFrame()
		self.frame_buttons.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
		self.frame_buttons.setFrameShape(QtWidgets.QFrame.StyledPanel)
		
		self.hbox_btns = QtWidgets.QHBoxLayout(self.frame_buttons)
		self.confirm = QtWidgets.QPushButton("Confirm")
		self.cancel = QtWidgets.QPushButton("Cancel")
		
		self.confirm.clicked.connect(self.setVolume)
		self.cancel.clicked.connect(self.destroy)
		
		self.confirm.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
		self.cancel.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)

		self.hbox_btns.addWidget(self.cancel, alignment=QtCore.Qt.AlignRight)
		self.hbox_btns.addWidget(self.confirm)
		self.vbox.addWidget (self.frame_buttons, alignment=QtCore.Qt.AlignBottom)

	def setVolume(self):
		Game_Settings.audio_vol = self.audio_slider.value() / 100
		self.destroy()