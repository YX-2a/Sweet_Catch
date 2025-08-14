from PySide6 import QtWidgets, QtGui, QtCore, QtMultimedia
import game_settings

class Game_Object (QtWidgets.QGraphicsPixmapItem):
	def __init__ (self, img, sizeXY):
		super().__init__( QtGui.QPixmap(img.scaled(sizeXY[0], sizeXY[1])) )
		self.setShapeMode(QtWidgets.QGraphicsPixmapItem.BoundingRectShape)
		self.og_image = img
		self.w = sizeXY[0]
		self.h = sizeXY[1]
		self.speed = 0
		self.score_add = 0
		self.type = "Default"
	
	@property
	def width (self):
		return self.w
	
	@property
	def height (self):
		return self.h
	
	def setSpeed (self, num):
		self.speed = num
		
	def setScoreAdd (self, num):
		self.score_add = num
	
	def __str__ (self):
		return f"{self.type} Object : \nheight: {self.height}\nwidth: {self.width}\nx: {self.x()}\ny: {self.y()}\nspeed: {self.speed}\nscore add: {self.score_add}\n"
		
	def __repr__ (self):
		return self.__str__()

class Game_Sound (QtMultimedia.QSoundEffect):
	def __init__ (self, filename):
		super().__init__()
		self.setSource (QtCore.QUrl.fromLocalFile(filename))
		self.setLoopCount (1)
		self.setVolume (game_settings.Game_Settings.audio_vol)

	def update(self):
		self.setVolume (game_settings.Game_Settings.audio_vol)
	
class Player (Game_Object):
	def __init__ (self, img, sizeXY):
		super().__init__( img, sizeXY )
		self.speed = 10
		self.type = "Player"
		
	def shape (self):
		path = QtGui.QPainterPath()
		path.addRect(0, 0, self.w, 4)
		
		return path

class Faller (Game_Object):
	def __init__ (self, img, sizeXY):
		super().__init__( img, sizeXY )
		self.speed = 2
		self.type = "Faller"
		self.fname = ""
		self.sound = None
	
	def shape (self):
		path = QtGui.QPainterPath()
		path.addRect(0, 0, self.w, self.h)
		
		return path
		
	def setSound (self, fname):
		self.fname = fname
		self.sound = Game_Sound(self.fname)
	
class Apple (Faller):
	def __init__ (self, img, sizeXY):
		super().__init__( img, sizeXY )
		self.type = "Apple"
		self.score_add = 10
		self.speed = 4
		self.setSound("./sounds/apple_hit.wav")
	
class Lemon (Faller):
	def __init__ (self, img, sizeXY):
		super().__init__( img, sizeXY )
		self.type = "Lemon"
		self.score_add = -10
		self.speed = 3
		self.setSound("./sounds/lemon_hit.wav")

class Leaf (Faller):
	def __init__ (self, img, sizeXY):
		super().__init__( img, sizeXY )
		self.type = "Leaf"
		self.setSound("")
		
class Special (Faller):
	def __init__ (self, img, sizeXY):
		super().__init__( img, sizeXY )
		self.type = "Special"
		self.sub_type = "Generic"
		self.speed = 5
		self.setSound("./sounds/special_hit.wav")
	
	def __str__ (self):
		return f"{self.type} [{self.sub_type}] Object : \nheight: {self.height}\nwidth: {self.width}\nx: {self.x()}\ny: {self.y()}\nspeed: {self.speed}\nscore add: {self.score_add}\n"
		
	def __repr__ (self):
		return self.__str__()
	
class Pear (Special):
	def __init__ (self, img, sizeXY):
		super().__init__( img, sizeXY )
		self.sub_type = "Pear"
		
class Citrus (Special):
	def __init__ (self, img, sizeXY):
		super().__init__( img, sizeXY )
		self.sub_type = "Citrus"
		
