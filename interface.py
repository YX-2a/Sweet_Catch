from PySide6 import QtWidgets, QtCore, QtGui
from random import choice

class Interface (QtWidgets.QWidget):
	def __init__ (self):
		super().__init__()
		self.x1, self.y1, self.x2, self.y2 = 200,300,100,100
		self.gen_celin = [i for i in range (0, 401, 50)]
		self.fall = None
		self.inter_scr = 1
		
	def make (self):
		self.vbox = QtWidgets.QVBoxLayout (self)
		
		self.counter_score = QtWidgets.QLCDNumber ()
		self.num = 0
		self.counter_score.display (str(self.num))
		
		self.scene = QtWidgets.QGraphicsScene (0,0,500,400)	
		self.view = QtWidgets.QGraphicsView (scene = self.scene)		
		
		self.squr = self.scene.addRect(self.x1, self.y1, self.x2, self.y2, QtGui.QPen(QtGui.QColor(255, 0, 0)), QtGui.QBrush(QtGui.QColor(255, 0, 0)))
		
		self.vbox.addWidget (self.counter_score)
		self.vbox.addWidget (self.view)
		
		self.timer = QtCore.QTimer()
		self.tee = 0
		self.timer.setInterval (500 - self.tee)
		self.timer.timeout.connect (self.gen)
		
		self.timer.start ()
		
		return self
										
	def keyPressEvent (self, e):
		kpl = e.text().lower()
		
		if kpl == "q" or kpl == "a":
			if self.squr.x() == -200:
				self.squr.moveBy (0,0)
			else:
				self.squr.moveBy (-50,0)
		if kpl == "d":
			if self.squr.x() == 200:
				self.squr.moveBy (0,0)
			else:
				self.squr.moveBy (50,0)		
		else:
			pass
			
	def gen (self):
		if self.fall == None : 
			self.fall_x1,self.fall_y1,self.fall_x2,self.fall_y2 = choice (self.gen_celin),0,50,50
			self.fall = self.scene.addRect(self.fall_x1,self.fall_y1,self.fall_x2,self.fall_y2, QtGui.QPen(QtGui.QColor(255, 0, 0)), QtGui.QBrush(QtGui.QColor(0, 0, 255)))
		
		if self.fall.collidesWithItem(self.squr):
			self.scene.removeItem (self.fall)
			self.fall = None
			self.num = self.num + self.inter_scr
			print (self.num)
			
			self.counter_score.display (str(self.num))
			self.counter_score.update ()
			
			if self.tee == 430:
				self.tee = self.tee
				self.timer.stop()
				self.timer.setInterval (500 - self.tee)
				self.timer.start()

			else:
				self.tee += 10
				self.inter_scr += 1
				self.timer.stop()
				self.timer.setInterval (500 - self.tee)
				self.timer.start()	
				
		elif self.fall.y() == self.scene.height() - 50 :
			self.scene.removeItem (self.fall)
			self.fall = None
			self.num = self.num - self.inter_scr
			
			if self.num < 0:
				self.num = 0
				self.counter_score.display (str(self.num))
				self.counter_score.update ()
			
			else:
				self.counter_score.display (str(self.num))
				self.counter_score.update ()
			
			if self.tee == 430:
				self.tee = self.tee
				self.timer.stop()
				self.timer.setInterval (500 - self.tee)
				self.timer.start()
			else:
				self.tee += 10
				self.inter_scr += 1
				self.timer.stop()
				self.timer.setInterval (500 - self.tee)
				self.timer.start()							
		else:
			self.fall.moveBy (0,50)