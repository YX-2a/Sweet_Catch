from PySide6 import QtWidgets, QtCore, QtGui
from game_objects import Player, Apple, Lemon, Leaf, Pear, Citrus, Game_Sound
from random import choice, randint

class Interface (QtWidgets.QWidget):
	def __init__ (self):
		super().__init__()
		self.player_x = 0
		self.player_y = 288
		
		self.stop_sound = Game_Sound("./sounds/pause_game.wav")
		self.start_sound = Game_Sound("./sounds/new_game.wav")
		self.blu_bg_color = QtGui.QColor(0, 181, 226)
		self.red_bg_color = QtGui.QColor(255, 0, 0)
		self.yel_bg_color = QtGui.QColor(255, 255, 0)
		self.player_img = QtGui.QImage ("./textures/basket.png")
		self.apple_img = QtGui.QImage ("./textures/apple.png")
		self.lemon_img = QtGui.QImage ("./textures/lemon.png")
		self.leaf_img = QtGui.QImage ("./textures/leaf.png")
		self.special_img = QtGui.QImage ("./textures/special.png")
		self.stop_color = QtGui.QColor (127, 127, 127, 170)
		
		self.falling_obj_coords = [i for i in range (0, 480, 48)]
		self.falling_objs = [None for i in range(5)]
		self.falling_obj_sound = None
		self.stop_box = None
		self.special_state = False
		self.special_type = None
		
		self.current_key = None
		self.score_num = 0
		self.display_text = f"<font size=5>Score : {self.score_num}</font>"
		
	def make (self):
		self.make_widgets ()
		
		self.game_timer = QtCore.QTimer()
		self.game_timer.setInterval (16)
		self.game_timer.timeout.connect (self.game_tick)
		
		self.special_timer = QtCore.QTimer()
		self.special_timer.setInterval (10000)
		self.special_timer.timeout.connect (self.special_efx_stop)
		self.special_timer.setSingleShot (True)
		
		self.start_game()
		
		return self
		
	def make_widgets (self):
		self.vbox = QtWidgets.QVBoxLayout (self)
		
		self.score = QtWidgets.QLabel ()
		self.score.setText (self.display_text)
		self.score.setTextFormat (QtCore.Qt.RichText)
		self.score.setAlignment (QtCore.Qt.AlignHCenter)
		
		self.scene = QtWidgets.QGraphicsScene (0,0,480,384)
		self.scene.setBackgroundBrush(QtGui.QBrush(self.blu_bg_color))
		self.view = QtWidgets.QGraphicsView (scene = self.scene)
		self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		
		self.vbox.addWidget (self.score)
		
		self.player = Player (self.player_img, (96,96))
		self.player.setPos (self.player_x, self.player_y)
		
		self.scene.addItem (self.player)
		self.vbox.addWidget (self.view)
		
	def keyPressEvent (self, e):
		self.current_key = e.key()
	
	def keyReleaseEvent (self, e):
		self.current_key = None

	def show_score (self, score_add):
		self.score_num = self.score_num + score_add
		self.display_text = f"<font size=5>Score : {self.score_num}</font>"
		self.score.setText (self.display_text)
		self.score.update ()
		
	def game_tick (self):
		if (self.current_key == QtCore.Qt.Key_Q or self.current_key == QtCore.Qt.Key_A) and self.player_x > 0:
			self.player_x -= self.player.speed
		elif self.current_key == QtCore.Qt.Key_D and self.player_x < (self.scene.width() - 96):
			self.player_x += self.player.speed
		self.player.setX(self.player_x)
		
		for index, falling_obj in enumerate(self.falling_objs):
			fallen_obj = self.falling_obj_tick(falling_obj)
			self.falling_objs[index] = fallen_obj
			
	def falling_obj_tick (self, falling_obj):
		if falling_obj == None:
			falling_objs_classes = [Apple(self.apple_img, (48,48)), Lemon(self.lemon_img, (48,48)), Leaf(self.leaf_img, (48,48))] 
			falling_obj = choice(falling_objs_classes)
			
			if self.score_num % 100 == 0 and self.score_num > 0 and self.special_state == False:
				falling_obj = choice([Pear(self.special_img, (48,48)), Citrus(self.special_img, (48,48))])
			
			falling_obj_x = choice (self.falling_obj_coords)
			self.scene.addItem (falling_obj)
			falling_obj.setX (falling_obj_x)
			falling_obj.setY (-48 - randint (0, 48))
			if self.special_state:
				self.special_efx_tick (falling_obj)
				return falling_obj
			else:
				return falling_obj
			
		elif falling_obj.collidesWithItem(self.player):
			if falling_obj.type == "Special": 
				self.special_type = falling_obj.sub_type
				self.special_state = True
				self.special_timer.start()
				if self.special_type == "Citrus":
					self.scene.setBackgroundBrush(QtGui.QBrush(self.yel_bg_color))
				elif self.special_type == "Pear":
					self.scene.setBackgroundBrush(QtGui.QBrush(self.red_bg_color))
			
			if self.falling_obj_sound:
				self.falling_obj_sound.stop()
				
			self.falling_obj_sound = falling_obj.sound 
			self.falling_obj_sound.play()
			self.show_score(falling_obj.score_add)
			self.scene.removeItem (falling_obj)
			falling_obj = None
			return falling_obj
			
		elif falling_obj.pos().y() >= self.scene.height():
			self.scene.removeItem (falling_obj)
			falling_obj = None
			self.show_score(0)
			return falling_obj
			
		else:
			falling_obj.setY (falling_obj.pos().y() + falling_obj.speed)
			return falling_obj
	
	def special_efx_tick (self, obj):
		if self.special_type == "Pear":
			if obj.type == "Apple":
				obj.setScoreAdd (50)
				obj.setSpeed (6)
				obj.setSound ("./sounds/special_apple_hit.wav")
				
			elif obj.type == "Lemon":
				obj.setScoreAdd (0)
				obj.setSpeed (3)
				
		elif self.special_type == "Citrus":
			if obj.type == "Apple":
				obj.setScoreAdd (0)
				obj.setSpeed (3)
				
			elif obj.type == "Lemon":
				obj.setScoreAdd (-50)
				obj.setSpeed (6)
				obj.setSound ("./sounds/special_lemon_hit.wav")
	
	def special_efx_stop (self):
		self.special_type = None
		self.special_state = False	
		self.bg_color = QtGui.QColor(0, 181, 226)
		self.scene.setBackgroundBrush(QtGui.QBrush(self.bg_color))
	
	def stop_game (self):
		self.game_timer.stop()
		if self.stop_box == None:
			self.stop_box = self.scene.addRect(0, 0, self.scene.width(), self.scene.height(), QtGui.QPen(self.stop_color), QtGui.QBrush(self.stop_color))
		
		if self.falling_obj_sound:
			if self.falling_obj_sound.isPlaying():
				self.falling_obj_sound.stop()
		self.stop_sound.play()
		
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
		
		for i, obj in enumerate(self.falling_objs):
			if obj:
				self.scene.removeItem (obj)
				self.falling_objs[i] = None
		
		if self.special_timer.isActive():
			self.special_timer.stop()
			self.special_efx_stop ()
			
		if self.falling_obj_sound:
			if self.falling_obj_sound.isPlaying():
				self.falling_obj_sound.stop()
			self.falling_obj_sound = None
		
		self.player_x = 0
		self.player.setPos (self.player_x, self.player_y)
		
		self.score_num = 0
		self.show_score(0)
		
		self.start_sound.play()
		self.start_game()