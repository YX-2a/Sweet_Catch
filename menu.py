from PySide6 import QtWidgets, QtCore

class Menu (QtWidgets.QMenuBar):
	def __init__ (self, parent, window):
		super().__init__(parent)
		self.game = None
		self.help = None
		self.parent = parent
		self.window = window
		
	def make (self):
		self.game = QtWidgets.QMenu ("Game")
		self.new_act = self.game.addAction ("New")
		self.pause_act = self.game.addAction ("Pause")
		self.game.addSeparator ()
		self.quit_act = self.game.addAction ("Quit")
		
		self.help = QtWidgets.QMenu ("Help")
		self.about_act = self.help.addAction ("About")
		
		self.new_act.setShortcut   (QtCore.QKeyCombination(QtCore.Qt.ControlModifier, QtCore.Qt.Key_N))
		self.pause_act.setShortcut (QtCore.QKeyCombination(QtCore.Qt.ControlModifier, QtCore.Qt.Key_P))
		self.quit_act.setShortcut  (QtCore.QKeyCombination(QtCore.Qt.ControlModifier, QtCore.Qt.Key_Q))
		self.about_act.setShortcut (QtCore.QKeyCombination(QtCore.Qt.ControlModifier, QtCore.Qt.Key_A))
		
		self.new_act.triggered.connect (self.new)
		self.pause_act.triggered.connect (self.pause)
		self.quit_act.triggered.connect (self.quit)
		
		self.about_act.triggered.connect (self.about)
		
		self.addMenu (self.game)
		self.addMenu (self.help)
		
		return self
	
	def new (self):
		self.parent.reset_game()
		
	def about (self):
		self.pause()
		msg_box = QtWidgets.QMessageBox(self.parent)
		msg_box.setWindowTitle ("About")
		msg_box.setText ("# Sweet Catch\n\nJust a Beta for now.")
		msg_box.setTextFormat (QtCore.Qt.MarkdownText)
		msg_box.exec()
		self.unpause()
	
	def unpause (self):
		self.pause_act.triggered.disconnect()
		if self.parent.falling_obj_sound:
			if self.parent.falling_obj_sound.isPlaying():
				self.parent.falling_obj_sound.stop()
		self.parent.stop_sound.play()
		self.parent.start_game()
		self.pause_act.setText ("Pause")
		self.pause_act.triggered.connect (self.pause)
		
	def pause (self):
		self.pause_act.triggered.disconnect()
		self.parent.stop_game()
		self.pause_act.setText ("Continue")
		self.pause_act.triggered.connect (self.unpause)
		
	def quit (self):
		self.parent.close()
		self.window.close()