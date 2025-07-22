from PySide6 import QtWidgets, QtGui, QtCore

class Game_Object (QtWidgets.QGraphicsPixmapItem):
	def __init__ (self, img, sizeXY):
		super().__init__( QtGui.QPixmap(img.scaled(sizeXY[0], sizeXY[1])) )
		self.setShapeMode(QtWidgets.QGraphicsPixmapItem.BoundingRectShape)
		self.og_image = img
		self.w = sizeXY[0]
		self.h = sizeXY[1]
		self.speed = 0
		self.score_add = 0
	
	def width (self):
		return self.w
		
	def height (self):
		return self.h
	
	def setSpeed (self, num):
		self.speed = num
	
	def setScoreAdd (self, num):
		self.score_add = num
	
	def __str__ (self):
		return f"Game Object : \nheight: {self.h}\nwidth: {self.w}\nx: {self.x()}\ny: {self.y()}\nspeed: {self.speed}\nscore add: {self.score_add}\n"
		
	def __repr__ (self):
		return self.__str__()
	
		
class Player (Game_Object):
	def __init__ (self, img, sizeXY):
		super().__init__( img, sizeXY )
		self.speed = 10
		
	def shape (self):
		path = QtGui.QPainterPath()
		path.addRect(0, 0, self.w, self.h * (3/8))
		
		return path

class Fruit (Game_Object):
	def __init__ (self, img, sizeXY):
		super().__init__( img, sizeXY )
		self.speed = 2
	
	def shape (self):
		path = QtGui.QPainterPath()
		path.addRect(0, 0, self.w, self.h)
		
		return path

class Apple (Fruit):
	def __init__ (self, img, sizeXY):
		super().__init__( img, sizeXY )
		self.score_add = 10
	
class Lemon (Fruit):
	def __init__ (self, img, sizeXY):
		super().__init__( img, sizeXY )
		self.score_add = -10
	