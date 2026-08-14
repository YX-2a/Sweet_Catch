from PySide6 import QtWidgets, QtGui
from pygame.mixer import Sound
import game_settings

class Game_View (QtWidgets.QGraphicsView):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	def keyPressEvent (self, e):
		e.ignore()
	
	def keyReleaseEvent (self, e):
		e.ignore()

class Game_Sprite (QtGui.QImage):
	def __init__(self, path):
		super().__init__(path)
		self.path = path

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

class Game_Sound_Index:
	G_NEWRS = 0
	G_PAUSE = 1
	R_APPLE = 2
	R_LEMON = 3
	S_APPLE = 4
	S_LEMON = 5
	SPECIAL = 6

class Game_Sound (Sound):
	def __init__ (self, filename):
		super().__init__(filename)
		self.set_volume (game_settings.game_settings.all_audio_dict["Volume"])

	def update(self):
		self.set_volume (game_settings.game_settings.all_audio_dict["Volume"])

	@property
	def volume(self):
		return self.get_volume()

class Game_Sound_Management:
	def __init__(self):
		self.all_sounds = [None] * 7
		self.update_sounds()
		
	def update_sounds (self):
		self.all_sounds[Game_Sound_Index.G_NEWRS] = Game_Sound(game_settings.game_settings.all_audio_dict["New Game"])
		self.all_sounds[Game_Sound_Index.G_PAUSE] = Game_Sound(game_settings.game_settings.all_audio_dict["Pause/Continue Game"])
		self.all_sounds[Game_Sound_Index.R_APPLE] = Game_Sound(game_settings.game_settings.all_audio_dict["Apple Hit"])
		self.all_sounds[Game_Sound_Index.R_LEMON] = Game_Sound(game_settings.game_settings.all_audio_dict["Lemon Hit"])
		self.all_sounds[Game_Sound_Index.S_APPLE] = Game_Sound(game_settings.game_settings.all_audio_dict["Special Apple Hit"])
		self.all_sounds[Game_Sound_Index.S_LEMON] = Game_Sound(game_settings.game_settings.all_audio_dict["Special Lemon Hit"])
		self.all_sounds[Game_Sound_Index.SPECIAL] = Game_Sound(game_settings.game_settings.all_audio_dict["Special Hit"])
	
	def play_sound (self, index):
		if index > -1:
			self.all_sounds[index].play()

	def stop_sound (self, index):
		if index > -1:
			self.all_sounds[index].stop()

	def the_sound (self, index):
		if index > -1:
			return self.all_sounds[index]

class Game_Text (QtWidgets.QGraphicsTextItem):
	def __init__ (self):
		super().__init__()
		self.setZValue(0.1)
		self.text_font = QtGui.QFont("Sans")
		self.text_font.setBold(True)
		self.plain_text = ""
		self.text_color = None
		self.text_size = 0

		self.setFont(self.text_font)
		self.adjustSize()

	def setSize (self, size):
		self.text_font.setPixelSize(size)
		self.text_size = size
		self.setFont(self.text_font)
		self.adjustSize()

	def setText (self, text):
		self.setPlainText(text)
		self.plain_text = text
		self.adjustSize()

	def setColor (self, color):
		self.setDefaultTextColor(color)
		self.text_color = color

class Player (Game_Object):
	def __init__ (self, sizeXY):
		super().__init__( game_settings.game_settings.all_textures_dict["Player"], sizeXY )
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
		self.s_index = -1
	
	def shape (self):
		path = QtGui.QPainterPath()
		path.addRect(0, 0, self.w, self.h)
		
		return path
		
	def setSound (self, index):
		self.s_index = index

class Apple (Faller):
	def __init__ (self, sizeXY):
		super().__init__( game_settings.game_settings.all_textures_dict["Apple"], sizeXY )
		self.type = "Apple"
		self.score_add = 10
		self.speed = 4
		self.setSound(Game_Sound_Index.R_APPLE)

class Lemon (Faller):
	def __init__ (self, sizeXY):
		super().__init__( game_settings.game_settings.all_textures_dict["Lemon"], sizeXY )
		self.type = "Lemon"
		self.score_add = -10
		self.speed = 3
		self.setSound(Game_Sound_Index.R_LEMON)

class Leaf (Faller):
	def __init__ (self, sizeXY):
		super().__init__( game_settings.game_settings.all_textures_dict["Leaf"], sizeXY )
		self.type = "Leaf"
		
class Special (Faller):
	def __init__ (self, sizeXY):
		super().__init__( game_settings.game_settings.all_textures_dict["Special"], sizeXY )
		self.type = "Special"
		self.sub_type = "Generic"
		self.speed = 5
		self.setSound(Game_Sound_Index.SPECIAL)
	
	def __str__ (self):
		return f"{self.type} [{self.sub_type}] Object : \nheight: {self.height}\nwidth: {self.width}\nx: {self.x()}\ny: {self.y()}\nspeed: {self.speed}\nscore add: {self.score_add}\n"
		
	def __repr__ (self):
		return self.__str__()
	
class Pear (Special):
	def __init__ (self, sizeXY):
		super().__init__( sizeXY )
		self.sub_type = "Pear"
		
class Citrus (Special):
	def __init__ (self, sizeXY):
		super().__init__( sizeXY )
		self.sub_type = "Citrus"
