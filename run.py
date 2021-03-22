import pyglet 
import math 
import os

from pyglet.window import Window
from pyglet.window import key

from physobj import PhysicalObject
from road import Road
from agent import Player       

class GameWindow(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super(GameWindow, self).__init__(1300, 1000, *args, **kwargs)

		self.game_batch = pyglet.graphics.Batch()
		game_objects = self.create_game_objects(self.game_batch)
		self.game_objects, self.player_car, self.game_road= game_objects

		self.key_handler = key.KeyStateHandler()
		self.push_handlers(self.key_handler)

		pyglet.clock.schedule_interval(self.update, 1.0 / 120.0)

	def create_game_objects(self, game_batch):
		game_road = Road(x=0,y=0,batch=game_batch)
		player_car = Player(x=380,y=870,batch=game_batch)
		player_car.draw_center(taken_batch=game_batch)

		game_objects = [game_road] + [player_car]

		return game_objects, player_car, game_road

	def on_draw(self):

		self.clear()

		self.game_batch.draw()

	def on_mouse_press(self, x, y, button, modifiers):

		a = (GLuint * 1)(0)
		glReadPixels(x, y, 1, 1, GL_GREEN, GL_UNSIGNED_BYTE, a)

		print(a[0])	

	def update(self, dt):
		if(self.player_car.is_alive == True):
			self.player_car.update(dt, self.key_handler, taken_batch=self.game_batch)

			self.player_car.draw_center(self.game_batch)

			self.player_car.radars.clear()
			for d in range(-90, 120, 45):
				self.player_car.comp_radars(d, self.game_road)
			self.player_car.draw_radars(self.game_batch)

			self.player_car.draw_collision_points(self.game_road, self.game_batch)

			self.player_car.check_collision(self.game_road)
		else:
			self.player_car.x = 380
			self.player_car.y = 870
			self.player_car.rotation = 0
			self.player_car.velocity_x = 0
			self.player_car.velocity_y = 0
			self.player_car.is_alive = True	

		self.game_road.update(dt)

def start_gen():
	win = GameWindow()
	pyglet.app.run()

start_gen()	