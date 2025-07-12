from PySide6 import QtWidgets, QtCore, QtGui
from random import choice

class Interface (QtWidgets.QWidget):
	def __init__ (self):
		super().__init__()
		self.x1, self.y1, self.x2, self.y2 = 200,300,100,100
		self.fall_coords = [i for i in range (0, 401, 50)]
		self.fall = None
		self.squr_color = QtGui.QColor(255, 0, 0)
		self.fall_color = QtGui.QColor(0, 0, 255)
		self.score_boost = 0
		self.current_intv = 50
		self.current_key = None
				
	def make (self):
		self.vbox = QtWidgets.QVBoxLayout (self)
		
		self.score = QtWidgets.QLabel ("Score : 0")
		self.score_num = 0
		self.score.setText (f"Score : {self.score_num}")
		
		self.scene = QtWidgets.QGraphicsScene (0,0,500,400)	
		self.view = QtWidgets.QGraphicsView (scene = self.scene)		
		
		self.squr = self.scene.addRect(self.x1, self.y1, self.x2, self.y2, QtGui.QPen(self.squr_color), QtGui.QBrush(self.squr_color))
		
		self.vbox.addWidget (self.score)
		self.vbox.addWidget (self.view)
		
		self.mov_timer = QtCore.QTimer()
		self.mov_timer.setInterval (15)
		self.mov_timer.timeout.connect (self.player_move)
		self.mov_timer.start ()
		
		self.timer = QtCore.QTimer()
		self.speed = 0
		self.current_intv = self.current_intv - self.speed
		self.timer.setInterval (self.current_intv)
		self.timer.timeout.connect (self.fall_move)
		self.timer.start ()
		
		return self
										
	def keyPressEvent (self, e):
		self.current_key = e.key()
	
	def keyReleaseEvent (self, e):
		self.current_key = None
	
	def player_move (self):
		if self.current_key == QtCore.Qt.Key_Q or self.current_key == QtCore.Qt.Key_A:
			if self.squr.x() == -200:
				self.squr.moveBy (0,0)
			else:
				self.squr.moveBy (-5,0)
				
		elif self.current_key == QtCore.Qt.Key_D:
			if self.squr.x() == 200:
				self.squr.moveBy (0,0)
			else:
				self.squr.moveBy (5,0)
		
		else:
			self.squr.moveBy (0,0)
				
	def fall_move (self):
		self.speed = 5
		if self.fall == None :
			self.fall_x1,self.fall_y1,self.fall_x2,self.fall_y2 = choice (self.fall_coords),0,50,50
			self.fall = self.scene.addRect(self.fall_x1,self.fall_y1,self.fall_x2,self.fall_y2, QtGui.QPen(self.fall_color), QtGui.QBrush(self.fall_color))
		
		elif self.fall.collidesWithItem(self.squr):
			self.scene.removeItem (self.fall)
			self.fall = None
			self.score_boost += 1
			self.score_num = self.score_num + self.score_boost
			
			self.score.setText (f"Score : {self.score_num}")
			self.score.update ()
			
			if self.current_intv > 15:
				self.current_intv = self.current_intv - self.speed
				self.timer.setInterval (self.current_intv)
			
		elif self.fall.y() == self.scene.height() - 50 :
			self.scene.removeItem (self.fall)
			self.fall = None ## NULL it
			self.score_num = self.score_num - self.score_boost
			
			self.score.setText (f"Score : {self.score_num}")
			self.score.update ()
			
			if self.current_intv < 45:
				self.current_intv = self.current_intv + self.speed
				self.timer.setInterval (self.current_intv)
				
		else:
			self.fall.moveBy (0,5)