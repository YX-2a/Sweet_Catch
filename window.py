from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QTimer, QEvent
from PySide6.QtGui import QIcon
from interface import Interface
from menu import Menu

class Window (QMainWindow):
	def __init__ (self):
		super().__init__(parent = None, flags = Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowTitleHint)
		self.setWindowTitle ("Sweet Catch")
		self.setWindowIcon (QIcon("./textures/leaf.png"))
		self.setFixedSize(500, 466) 
		
		self.inter = Interface()
		self.setCentralWidget (self.inter.make())
		
		menu = Menu(self.inter, self)
		self.setMenuBar (menu.make())
		
		self.move_timer = QTimer(self)
		self.move_timer.setInterval(250)
		self.move_timer.setSingleShot(True)
		self.move_timer.timeout.connect(self.inter.start_game)
		
	def moveEvent(self, e):
		self.inter.stop_game()
		self.move_timer.start()
		super().moveEvent(e)
		
	def changeEvent(self, e):
		if e.type() == QEvent.WindowStateChange or e.type() == QEvent.ActivationChange:
			if self.isMinimized():
				self.inter.stop_game()
				
			elif self.isActiveWindow():
				self.inter.start_game()
				
			else:
				self.inter.stop_game()
		
		super().changeEvent(e)