from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QTimer, QEvent
from PySide6.QtGui import QIcon

from game_settings import game_settings
from settings_rw import settings_writer
from interface import Interface
from menu import Menu

class Window (QMainWindow):
	def __init__ (self):
		super().__init__(parent = None, flags = Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowTitleHint)
		self.setWindowTitle ("Sweet Catch")
		self.setWindowIcon (QIcon(game_settings.all_textures_dict["Leaf"].path))
		
		self.inter = Interface()
		self.setCentralWidget (self.inter.make())
		
		self.menu = Menu(self.inter, self)
		self.setMenuBar (self.menu.make())

		self.adjustSize()
		self.setFixedSize(self.size())

		self.move_timer = QTimer(self)
		self.move_timer.setInterval(250)
		self.move_timer.setSingleShot(True)
		self.move_timer.timeout.connect(self.menu.unpause)
		
	def moveEvent(self, e):
		self.menu.pause()
		self.move_timer.start()
		super().moveEvent(e)
		
	def changeEvent(self, e):
		if e.type() == QEvent.WindowStateChange or e.type() == QEvent.ActivationChange:
			if self.isMinimized():
				self.menu.pause()
				
			elif self.isActiveWindow():
				self.menu.unpause()
				
			else:
				self.menu.pause()
		
		super().changeEvent(e)

	def closeEvent (self, e):
		settings_writer(game_settings.settings_dict, game_settings.settings_dir)
		super().closeEvent(e)
