from PySide6 import QtWidgets, QtCore, QtGui
from game_objects import Player, Apple, Lemon, Leaf
from random import choice

class Interface (QtWidgets.QWidget):
	def __init__ (self):
		super().__init__()
		self.player_x = 0
		self.player_y = 288
		
		self.falling_obj_coords = [i for i in range (0, 480, 48)]
		self.falling_obj = None
		self.vbox = None
		self.stop_box = None
		
		self.bg_color = QtGui.QColor(0, 181, 226)
		self.player_img = QtGui.QImage ("./textures/basket.png")
		self.apple_img = QtGui.QImage ("./textures/apple.png")
		self.lemon_img = QtGui.QImage ("./textures/lemon.png")
		self.leaf_img = QtGui.QImage ("./textures/leaf.png")
		self.stop_color = QtGui.QColor (127, 127, 127, 170)
		
		self.falling_obj_speed = None
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
		
		if self.falling_obj == None :
			self.falling_obj_x = choice (self.falling_obj_coords)
			self.falling_obj = choice([Apple(self.apple_img, (48,48)), Lemon(self.lemon_img, (48,48)), Leaf(self.leaf_img, (48,48))])
			self.scene.addItem (self.falling_obj)
			self.falling_obj.setX (self.falling_obj_x)
			self.falling_obj.setY (-48)
			
			if self.falling_obj_speed == None:
				self.falling_obj_speed = self.falling_obj.speed
			
		elif self.falling_obj.collidesWithItem(self.player):
			self.show_score(self.falling_obj.score_add)
			self.scene.removeItem (self.falling_obj)
			self.falling_obj = None
			
			if self.falling_obj_speed < 8:
				self.falling_obj_speed += 2
			
		elif self.falling_obj.pos().y() >= self.scene.height():
			self.scene.removeItem (self.falling_obj)
			self.falling_obj = None
			self.show_score(0)
			
			if self.falling_obj_speed > 2:
				self.falling_obj_speed -= 2
		else:
			self.falling_obj.setY (self.falling_obj.pos().y() + self.falling_obj_speed)
			
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
		
		self.scene.removeItem (self.falling_obj)
		self.falling_obj = None
		
		self.player_x = 0
		self.player.setPos (self.player_x, self.player_y)
		
		self.score_num = 0
		self.show_score(0)
		self.falling_obj_speed = None
		
		self.start_game()