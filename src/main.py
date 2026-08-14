from PySide6.QtWidgets import QApplication
import pygame.mixer
from window import Window
from sys import exit as Qkill

if __name__ == "__main__":
	app = QApplication ([])
	pygame.mixer.init()
	app.setStyle("Fusion")
	win = Window ()
	win.show()
	Qkill(app.exec()) 