from PySide6.QtWidgets import QMainWindow
from interface import Interface

class Window (QMainWindow):
	def __init__ (self):
		super().__init__()
		self.setWindowTitle ("Fallers")
		
		inter = Interface()
		self.setCentralWidget (inter.make())