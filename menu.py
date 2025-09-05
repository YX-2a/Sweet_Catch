from PySide6 import QtWidgets, QtCore
import game_settings

class Menu (QtWidgets.QMenuBar):
	def __init__ (self, parent, window):
		super().__init__(parent)
		self.game = None
		self.help = None
		self.parent = parent
		self.window = window
		
	def make (self):
		self.game = QtWidgets.QMenu ("Game")
		self.game_new_act = self.game.addAction ("New")
		self.game_pause_act = self.game.addAction ("Pause")
		self.game.addSeparator ()
		self.game_quit_act = self.game.addAction ("Quit")
		
		self.settings = QtWidgets.QMenu ("Edit")
		self.settings_set_act = self.settings.addAction ("Settings...")
		self.settings.addSeparator ()
		volume = self.settings.addAction ("Volume")
		control = self.settings.addAction ("Controls")
		
		self.help = QtWidgets.QMenu ("Help")
		self.help_about_act = self.help.addAction ("About")
		
		self.set_shortcuts()
		
		self.game_new_act.triggered.connect (self.parent.reset_game)
		self.game_pause_act.triggered.connect (self.pause)
		self.game_quit_act.triggered.connect (self.window.close)
		self.settings_set_act.triggered.connect (self.set_diag)
		self.help_about_act.triggered.connect (self.about)
		volume.triggered.connect (self.volume_win)
		control.triggered.connect (self.control_win)
		
		self.addMenu (self.game)
		self.addMenu (self.settings)
		self.addMenu (self.help)
		
		return self
	
	def set_shortcuts(self):
		self.game_new_act.setShortcut (game_settings.Game_Settings.game_new_act_k[0])
		self.game_pause_act.setShortcut (game_settings.Game_Settings.game_pause_act_k[0])
		self.settings_set_act.setShortcut (game_settings.Game_Settings.settings_set_act_k[0])
		self.game_quit_act.setShortcut (game_settings.Game_Settings.game_quit_act_k[0])
		self.help_about_act.setShortcut (game_settings.Game_Settings.help_about_act_k[0])
		
	def about (self):
		msg_box = QtWidgets.QMessageBox(self.parent)
		msg_box.setWindowTitle ("About")
		msg_box.setText ("# Sweet Catch\n\nJust a Beta for now.")
		msg_box.setTextFormat (QtCore.Qt.MarkdownText)
		msg_box.exec()
	
	def unpause (self):
		self.game_pause_act.triggered.disconnect()
		if self.parent.falling_obj_sound:
			if self.parent.falling_obj_sound.isPlaying():
				self.parent.falling_obj_sound.stop()
		self.parent.start_game()
		self.parent.stop_sound.update()
		self.parent.stop_sound.play()
		self.game_pause_act.setText ("Pause")
		self.game_pause_act.triggered.connect (self.pause)
		
	def pause (self):
		self.game_pause_act.triggered.disconnect()
		if self.parent.falling_obj_sound:
			if self.parent.falling_obj_sound.isPlaying():
				self.parent.falling_obj_sound.stop()
		self.parent.stop_game()
		self.parent.stop_sound.update()
		self.parent.stop_sound.play()
		self.game_pause_act.setText ("Continue")
		self.game_pause_act.triggered.connect (self.unpause)

	def set_diag(self):
		settings_win = game_settings.SettingsWindow(self.parent)
		settings_win.exec()
		self.set_shortcuts()
	
	def volume_win(self):
		audio = game_settings.SettingsDialog(self.parent, game_settings.AudioTab())
		audio.exec()
	
	def control_win(self):
		control = game_settings.SettingsDialog(self.parent, game_settings.ControlsTab())
		control.exec()
		self.set_shortcuts()