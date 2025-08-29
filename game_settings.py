from PySide6 import QtWidgets, QtCore
from settings_rw import settings_reader, settings_writer, make_to_string

class Game_Settings:
	settings_dict = settings_reader("game.settings")
	audio_vol = settings_dict["Volume"]
	player_left_k = [settings_dict["Move Player Left"], "Move Player Left"]
	player_right_k = [settings_dict["Move Player Right"], "Move Player Right"]
	settings_set_act_k = [settings_dict["Open Game Settings"], "Open Game Settings"]
	game_new_act_k = [settings_dict["New Game"], "New Game"]
	game_pause_act_k = [settings_dict["Pause/Continue Game"], "Pause/Continue Game"]
	game_quit_act_k = [settings_dict["Quit Game"], "Quit Game"]
	help_about_act_k = [settings_dict["About Game"], "About Game"]
	all_controls = [player_left_k, player_right_k, settings_set_act_k, game_new_act_k, game_pause_act_k, game_quit_act_k, help_about_act_k]

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
		
		self.audio_label = QtWidgets.QLabel("Audio : ")
		self.audio_slider = QtWidgets.QSlider()
		
		self.audio_slider.setRange(0, 100)
		self.audio_slider.setSliderPosition(Game_Settings.audio_vol * 100)
		self.audio_slider.setOrientation(QtCore.Qt.Horizontal)
		
		self.hbox_audio.addWidget(self.audio_label, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
		self.hbox_audio.addWidget(self.audio_slider)
		self.vbox.addLayout (self.hbox_audio)

	def tabAction(self):
		Game_Settings.audio_vol = self.audio_slider.value() / 100
		Game_Settings.settings_dict["Volume"] = Game_Settings.audio_vol

class ControlsTab(SettingsTab):
	def __init__(self):
		super().__init__()
		self.tab_name = "Controls"
		self.vbox = QtWidgets.QVBoxLayout(self)
		
		for control in Game_Settings.all_controls:
			hbox_control = QtWidgets.QHBoxLayout()
			control_label = QtWidgets.QLabel(f"{control[1]} : ")
			control_button = QtWidgets.QPushButton(make_to_string(control[0]))
			
			hbox_control.addWidget(control_label, alignment=QtCore.Qt.AlignLeft)
			hbox_control.addWidget(control_button)
			self.vbox.addLayout (hbox_control)


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