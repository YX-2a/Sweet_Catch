from PySide6 import QtWidgets, QtCore, QtGui
from random import choice

class Interface (QtWidgets.QWidget):
	def __init__ (self):
		super().__init__()
		self.x1, self.y1, self.x2, self.y2 = 200,300,100,100
		self.gen_celin = [i for i in range (0, 401, 50)]
		self.fall = None
		
	def make (self):
		self.scene = QtWidgets.QGraphicsScene (0,0,self.width(),self.height())	
		self.view = QtWidgets.QGraphicsView (parent = self,scene = self.scene)		
		
		self.squr = self.scene.addRect(self.x1, self.y1, self.x2, self.y2, QtGui.QPen(QtGui.QColor(255, 0, 0)), QtGui.QBrush(QtGui.QColor(255, 0, 0)))
		self.timer = QtCore.QTimer()
		self.tee = 0
		self.timer.setInterval (950 - self.tee)
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
			
			if self.tee == 800:
				self.tee = self.tee
				self.timer.stop()
				self.timer.setInterval (1000 - self.tee)
				self.timer.start()

			else:
				self.tee += 100
				self.timer.stop()
				self.timer.setInterval (1000 - self.tee)
				self.timer.start()	
				
		elif self.fall.y() == self.height() - 50 :
			self.scene.removeItem (self.fall)
			self.fall = None
	
			if self.tee == 800:
				self.tee = self.tee
				self.timer.stop()
				self.timer.setInterval (1000 - self.tee)
				self.timer.start()
			else:
				self.tee += 100
				self.timer.stop()
				self.timer.setInterval (1000 - self.tee)
				self.timer.start()							
		else:
			self.fall.moveBy (0,50)