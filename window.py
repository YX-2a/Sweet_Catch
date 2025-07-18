from PySide6.QtWidgets import QMainWindow
from interface import Interface
from menu import Menu

class Window (QMainWindow):
	def __init__ (self):
		super().__init__()
		self.setWindowTitle ("Fallers")
		
		inter = Interface()
		self.setCentralWidget (inter.make())
		
		menu = Menu(inter, self)
		self.setMenuBar (menu.make())