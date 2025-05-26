from PySide6.QtWidgets import QApplication
from window import Window
from sys import exit as Qkill

if __name__ == "__main__":
	app = QApplication ([])
	ecran = app.primaryScreen ()
	win = Window ()
	winw, winh = 500,400
	win.setGeometry (ecran.geometry().width() // 2 - winw // 2,ecran.geometry().height() // 2 - winh // 2,winw,winh)
	win.show()
	Qkill(app.exec()) 