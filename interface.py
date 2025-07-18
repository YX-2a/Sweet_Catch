from PySide6 import QtWidgets, QtCore, QtGui
from random import choice

class Interface (QtWidgets.QWidget):
	def __init__ (self):
		super().__init__()
		self.x1, self.y1, self.x2, self.y2 = 200,300,100,100
		self.fall_coords = [i for i in range (0, 401, 50)]
		self.fall = None
		self.vbox = None
		self.stop_box = None
		
		self.bg_color = QtGui.QColor(0, 181, 226)
		self.squr_color = QtGui.QColor(255, 0, 0)
		self.fall_color = QtGui.QColor(0, 255, 0)
		self.stop_color = QtGui.QColor (127, 127, 127, 170)
		
		self.score_boost = 0
		self.current_intv = 50
		self.current_key = None
		self.score_num = 0
		self.display_text = f"<font size=5>Score : {self.score_num}</font>"
		
	def make (self):
		self.make_widgets ()
		
		self.mov_timer = QtCore.QTimer()
		self.mov_timer.setInterval (15)
		self.mov_timer.timeout.connect (self.player_move)
		
		self.fall_timer = QtCore.QTimer()
		self.speed = 0
		self.current_intv = self.current_intv - self.speed
		self.fall_timer.setInterval (self.current_intv)
		self.fall_timer.timeout.connect (self.fall_move)
		
		self.start_game()
		
		return self
		
	def make_widgets (self):
		self.vbox = QtWidgets.QVBoxLayout (self)
		
		self.score = QtWidgets.QLabel ()
		self.score.setText (self.display_text)
		self.score.setTextFormat (QtCore.Qt.RichText)
		self.score.setAlignment (QtCore.Qt.AlignHCenter)
		
		self.scene = QtWidgets.QGraphicsScene (0,0,500,400)
		self.scene.setBackgroundBrush(QtGui.QBrush(self.bg_color))
		self.view = QtWidgets.QGraphicsView (scene = self.scene)		
		
		self.squr = self.scene.addRect(self.x1, self.y1, self.x2, self.y2, QtGui.QPen(self.squr_color), QtGui.QBrush(self.squr_color))
		
		self.vbox.addWidget (self.score)
		self.vbox.addWidget (self.view)
		
	def keyPressEvent (self, e):
		self.current_key = e.key()
	
	def keyReleaseEvent (self, e):
		self.current_key = None
	
	def player_move (self):
		squr_x = self.x1
		
		if (self.current_key == QtCore.Qt.Key_Q or self.current_key == QtCore.Qt.Key_A) and squr_x > -((self.scene.width() - self.x2)//2):
			squr_x -= 10

		elif self.current_key == QtCore.Qt.Key_D and squr_x < ((self.scene.width() - self.x2)//2):
			squr_x += 10
		
		self.squr.setPos(squr_x, 0)
		self.x1 = squr_x
		
	def show_score (self, negative = 1):
		self.score_num = self.score_num + (self.score_boost) * negative
		self.display_text = f"<font size=5>Score : {self.score_num}</font>"
		self.score.setText (self.display_text)
		self.score.update ()
		
	def fall_move (self):
		self.speed = 5
		if self.fall == None :
			self.fall_x1,self.fall_y1,self.fall_x2,self.fall_y2 = choice (self.fall_coords),-50,50,50
			self.fall = self.scene.addRect(self.fall_x1,self.fall_y1,self.fall_x2,self.fall_y2, QtGui.QPen(self.fall_color), QtGui.QBrush(self.fall_color))
		
		elif self.fall.collidesWithItem(self.squr):
			self.scene.removeItem (self.fall)
			self.fall = None
			self.score_boost += 1
			self.show_score()
			
			if self.current_intv > 10:
				self.current_intv = self.current_intv - self.speed
				self.fall_timer.setInterval (self.current_intv)
			
		elif self.fall.y() == self.scene.height():
			self.scene.removeItem (self.fall)
			self.fall = None
			self.show_score(negative = -1)
			
			if self.current_intv < 45:
				self.current_intv = self.current_intv + self.speed
				self.fall_timer.setInterval (self.current_intv)
		else:
			self.fall.setPos (0,self.fall.pos().y() + 5)
			
	def stop_game (self):
		self.fall_timer.stop()
		self.mov_timer.stop()
		
		if self.stop_box == None:
			self.stop_box = self.scene.addRect(0, 0, self.scene.width(), self.scene.height(), QtGui.QPen(self.stop_color), QtGui.QBrush(self.stop_color))
		
	def start_game (self):
		self.fall_timer.start()
		self.mov_timer.start()
		
		if self.stop_box != None:
			self.scene.removeItem (self.stop_box)
			self.stop_box = None
		
	def reset_game (self):
		self.fall_timer.stop()
		self.mov_timer.stop()
		
		if self.stop_box != None:
			self.scene.removeItem (self.stop_box)
			self.stop_box = None
			
		self.scene.removeItem (self.fall)
		self.fall = None
		
		self.scene.removeItem (self.squr)
		self.x1, self.y1, self.x2, self.y2 = 200,300,100,100
		self.squr = self.scene.addRect(self.x1, self.y1, self.x2, self.y2, QtGui.QPen(self.squr_color), QtGui.QBrush(self.squr_color))
			
		self.score_boost = 0
		self.score_num = 0
		self.current_intv = 50
		
		self.fall_timer.setInterval (self.current_intv)
		self.show_score()
		
		self.start_game()