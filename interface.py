from PySide6 import QtWidgets, QtCore, QtGui
from random import choice

class Interface (QtWidgets.QWidget):
	def __init__ (self):
		super().__init__()
		self.squr_x = 0
		self.squr_y = 288
		
		self.fall_coords = [i for i in range (0, 385, 50)]
		self.fall = None
		self.vbox = None
		self.stop_box = None
		
		self.bg_color = QtGui.QColor(0, 181, 226)
		self.squr_img = QtGui.QImage ("./textures/basket.png").scaled(96,96)
		self.fall_img = QtGui.QImage ("./textures/apple.png").scaled(48,48)
		self.stop_color = QtGui.QColor (127, 127, 127, 170)
		
		self.score_boost = 0
		self.speed = 2
		self.current_key = None
		self.score_num = 0
		self.display_text = f"<font size=5>Score : {self.score_num}</font>"
		
	def make (self):
		self.make_widgets ()
		
		self.game_timer = QtCore.QTimer()
		self.game_timer.setInterval (16)
		self.game_timer.timeout.connect (self.game_tick)
		
		self.start_game()
		
		return self
		
	def make_widgets (self):
		self.vbox = QtWidgets.QVBoxLayout (self)
		
		self.score = QtWidgets.QLabel ()
		self.score.setText (self.display_text)
		self.score.setTextFormat (QtCore.Qt.RichText)
		self.score.setAlignment (QtCore.Qt.AlignHCenter)
		
		self.scene = QtWidgets.QGraphicsScene (0,0,480,384)
		self.scene.setBackgroundBrush(QtGui.QBrush(self.bg_color))
		self.view = QtWidgets.QGraphicsView (scene = self.scene)
		self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		
		self.squr = self.scene.addPixmap(QtGui.QPixmap(self.squr_img))
		self.squr.setShapeMode(QtWidgets.QGraphicsPixmapItem.BoundingRectShape) 	
		self.vbox.addWidget (self.score)
		self.squr.setPos (self.squr_x, self.squr_y)
		
		self.vbox.addWidget (self.view)
		
	def keyPressEvent (self, e):
		self.current_key = e.key()
	
	def keyReleaseEvent (self, e):
		self.current_key = None

	def show_score (self, negative = 1):
		self.score_num = self.score_num + (self.score_boost * negative)
		self.display_text = f"<font size=5>Score : {self.score_num}</font>"
		self.score.setText (self.display_text)
		self.score.update ()
		
	def game_tick (self):
		if (self.current_key == QtCore.Qt.Key_Q or self.current_key == QtCore.Qt.Key_A) and self.squr_x > 0:
			self.squr_x -= 10

		elif self.current_key == QtCore.Qt.Key_D and self.squr_x < (self.scene.width() - 96):
			self.squr_x += 10
		
		self.squr.setX(self.squr_x)
		
		if self.fall == None :
			self.fall_x = choice (self.fall_coords)
			self.fall = self.scene.addPixmap(QtGui.QPixmap(self.fall_img))
			self.fall.setShapeMode(QtWidgets.QGraphicsPixmapItem.BoundingRectShape)
			self.fall.setX (self.fall_x)
			self.fall.setY (-48)
			
		elif self.fall.collidesWithItem(self.squr):
			self.scene.removeItem (self.fall)
			self.fall = None
			self.score_boost += 1
			self.show_score()
			
			if self.speed < 8:
				self.speed += 2
			
		elif self.fall.pos().y() >= self.scene.height():
			self.scene.removeItem (self.fall)
			self.fall = None
			self.show_score(negative = -1)
			
			if self.speed > 2:
				self.speed -= 2
		else:
			self.fall.setY (self.fall.pos().y() + self.speed)
			
	def stop_game (self):
		self.game_timer.stop()
		
		if self.stop_box == None:
			self.stop_box = self.scene.addRect(0, 0, self.scene.width(), self.scene.height(), QtGui.QPen(self.stop_color), QtGui.QBrush(self.stop_color))
		
	def start_game (self):
		self.game_timer.start()
		
		if self.stop_box != None:
			self.scene.removeItem (self.stop_box)
			self.stop_box = None
		
	def reset_game (self):
		self.game_timer.stop()
		
		if self.stop_box != None:
			self.scene.removeItem (self.stop_box)
			self.stop_box = None
			
		self.scene.removeItem (self.fall)
		self.fall = None
		
		self.scene.removeItem (self.squr)
		
		self.squr_x = 0
		
		self.squr = self.scene.addPixmap(QtGui.QPixmap(self.squr_img))
		self.squr.setShapeMode(QtWidgets.QGraphicsPixmapItem.BoundingRectShape) 	
		self.squr.setPos (self.squr_x, self.squr_y)
		
		self.score_boost = 0
		self.score_num = 0
		self.show_score()
		
		self.speed = 2
		
		self.start_game()