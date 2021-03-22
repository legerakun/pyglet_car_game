import pyglet 
import math 
import os

from pyglet import image
from pyglet.gl import *

from physobj import PhysicalObject

game_path = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(game_path, "image/")

pyglet.resource.path.append(resources_path)
pyglet.resource.reindex()

road_image = pyglet.resource.image('road_f.png')

class Road(PhysicalObject):
	def __init__(self, *args, **kwargs):
		super(Road, self).__init__(img=road_image, *args, **kwargs)

	def check_color(self,x,y):
		a = (GLubyte * 1)(0)
		glReadPixels(x, y, 1, 1, GL_GREEN, GL_UNSIGNED_BYTE, a)

		return a[0]	

	def update(self, dt):
		super(Road, self).update(dt)