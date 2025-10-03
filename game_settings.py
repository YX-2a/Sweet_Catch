from PySide6 import QtWidgets, QtCore, QtGui
from os import path
from settings_rw import settings_reader, settings_writer, make_to_string

class Game_Settings:
	settings_dict = settings_reader("game.settings")
	all_controls_dict = settings_dict["Controls"]
	all_audio_dict = settings_dict["Audio"]
	
class SettingsTab(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.tab_name = ""
	
	def tabAction(self):
		pass

class AudioTab(SettingsTab):
	def __init__(self):
		super().__init__()
		self.tab_name = "Audio"
		self.vbox = QtWidgets.QVBoxLayout(self)
		self.hbox_audio = QtWidgets.QHBoxLayout()
		self.audio_buffer = Game_Settings.all_audio_dict.copy()
		self.audio_buttons = {}
		
		self.audio_label = QtWidgets.QLabel("Volume : ")
		self.audio_slider = QtWidgets.QSlider()
		
		self.audio_slider.setRange(0, 100)
		self.audio_slider.setSliderPosition(self.audio_buffer["Volume"] * 100)
		self.audio_slider.setOrientation(QtCore.Qt.Horizontal)
		
		self.hbox_audio.addWidget(self.audio_label, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
		self.hbox_audio.addWidget(self.audio_slider)
		self.vbox.addLayout (self.hbox_audio)
		
		for audio in self.audio_buffer:
			if audio != "Volume":
				hbox_audio = QtWidgets.QHBoxLayout()
				audio_label = QtWidgets.QLabel(f"{audio} : ")
				audio_button = QtWidgets.QPushButton(str(self.audio_buffer[audio]))
				audio_button.setFixedSize(350, 22)
				audio_button.clicked.connect(self.setPath)
				
				self.audio_buttons[audio_button] = audio_label
				
				hbox_audio.addWidget(audio_label, alignment=QtCore.Qt.AlignLeft)
				hbox_audio.addWidget(audio_button, alignment=QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
				self.vbox.addLayout (hbox_audio)
				
	def setPath(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(self,f"Set The {self.audio_buttons[self.sender()].text().replace(' : ','')} Audio File","", "Audio Files (*.mp3 *.wav *.ogg *.flac *.wma);;MP3 Audio (*.mp3);;WAV Audio (*.wav);;OGG Audio (*.ogg);;FLAC Audio (*.flac);;WMA Audio (*.wma)")
		if fname[0]:
			self.sender().setText(path.relpath(fname[0], "."))
			self.audio_buffer[self.audio_buttons[self.sender()].text().replace(" : ","")] = self.sender().text()
		else:
			self.sender().setText("")
			self.audio_buffer[self.audio_buttons[self.sender()].text().replace(" : ","")] = ""
			
	def tabAction(self):
		self.audio_buffer["Volume"] = self.audio_slider.value() / 100
		Game_Settings.all_audio_dict = self.audio_buffer
		Game_Settings.settings_dict["Audio"] = Game_Settings.all_audio_dict

class ControlsTab(SettingsTab):
	def __init__(self):
		super().__init__()
		self.tab_name = "Controls"
		self.vbox = QtWidgets.QVBoxLayout(self)
		self.controls_buffer = Game_Settings.all_controls_dict.copy()
		self.control_dict = {}
		
		for control in self.controls_buffer:
			hbox_control = QtWidgets.QHBoxLayout()
			control_label = QtWidgets.QLabel(f"{control} : ")
			control_button = QtWidgets.QKeySequenceEdit()
			control_button.setKeySequence(self.controls_buffer[control])
			control_button.setMaximumSequenceLength(1)
			control_button.setFixedSize(150, 22)
			control_button.editingFinished.connect(self.controlSet)
			self.control_dict[control_button] = control
			
			hbox_control.addWidget(control_label, alignment=QtCore.Qt.AlignLeft)
			hbox_control.addWidget(control_button, alignment=QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
			self.vbox.addLayout (hbox_control)

	def controlSet (self):
		the_control = self.sender()
		key = the_control.keySequence()[0]
		if key.keyboardModifiers() == QtCore.Qt.NoModifier:
			key = key.key()
			
		self.controls_buffer[self.control_dict[the_control]] = key
	
	def tabAction(self):
		Game_Settings.all_controls_dict = self.controls_buffer
		Game_Settings.settings_dict["Controls"] = Game_Settings.all_controls_dict
		
class SettingsDialog(QtWidgets.QDialog):
	def __init__ (self, parent, child):
		super().__init__(parent)
		self.child = child
		
		self.resize (600,300)
		self.vbox = QtWidgets.QVBoxLayout(self)
		self.setWindowTitle (f"Settings - {self.child.tab_name}")
		
		self.vbox.addWidget(self.child)
		self.bottom_buttons()
	
	def bottom_buttons (self):
		self.frame_buttons = QtWidgets.QFrame()
		self.frame_buttons.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
		self.frame_buttons.setFrameShape(QtWidgets.QFrame.StyledPanel)
		
		self.hbox_btns = QtWidgets.QHBoxLayout(self.frame_buttons)
		self.confirm = QtWidgets.QPushButton("Confirm")
		self.cancel = QtWidgets.QPushButton("Cancel")
		
		self.confirm.clicked.connect(self.confirm_settings)
		self.cancel.clicked.connect(self.destroy)
		
		self.confirm.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
		self.cancel.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)

		self.hbox_btns.addWidget(self.cancel, alignment=QtCore.Qt.AlignRight)
		self.hbox_btns.addWidget(self.confirm)
		self.vbox.addWidget (self.frame_buttons, alignment=QtCore.Qt.AlignBottom)

	def confirm_settings(self):
		self.child.tabAction()
		self.destroy()
		
class SettingsWindow(QtWidgets.QDialog):
	def __init__ (self, parent):
		super().__init__(parent)
		self.audio_tab = AudioTab()
		self.controls_tab = ControlsTab()
		
		self.resize (600,300)
		self.vbox = QtWidgets.QVBoxLayout(self)
		self.settings_tabs = QtWidgets.QTabWidget()
		self.settings_tabs.addTab(self.audio_tab, self.audio_tab.tab_name)
		self.settings_tabs.addTab(self.controls_tab, self.controls_tab.tab_name)
		self.settings_tabs.currentChanged.connect(self.set_title)
		
		self.settings_tabs.setCurrentWidget(self.audio_tab)
		self.setWindowTitle (f"Settings - {self.settings_tabs.currentWidget().tab_name}")
		
		self.vbox.addWidget(self.settings_tabs)
		self.bottom_buttons()
	
	def set_title(self, i):
		self.setWindowTitle (f"Settings - {self.settings_tabs.widget(i).tab_name}")
	
	def bottom_buttons (self):
		self.frame_buttons = QtWidgets.QFrame()
		self.frame_buttons.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
		self.frame_buttons.setFrameShape(QtWidgets.QFrame.StyledPanel)
		
		self.hbox_btns = QtWidgets.QHBoxLayout(self.frame_buttons)
		self.confirm = QtWidgets.QPushButton("Confirm")
		self.cancel = QtWidgets.QPushButton("Cancel")
		
		self.confirm.clicked.connect(self.confirm_settings)
		self.cancel.clicked.connect(self.destroy)
		
		self.confirm.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
		self.cancel.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)

		self.hbox_btns.addWidget(self.cancel, alignment=QtCore.Qt.AlignRight)
		self.hbox_btns.addWidget(self.confirm)
		self.vbox.addWidget (self.frame_buttons, alignment=QtCore.Qt.AlignBottom)

	def confirm_settings(self):
		for widget_index in range(self.settings_tabs.count()):
			tab = self.settings_tabs.widget(widget_index)
			tab.tabAction()
		
		self.destroy()