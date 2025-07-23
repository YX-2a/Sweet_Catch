from PySide6.QtWidgets import QApplication
from window import Window
from sys import exit as Qkill

if __name__ == "__main__":
	app = QApplication ([])
	app.setStyle("Fusion")
	win = Window ()
	win.show()
	Qkill(app.exec()) 