import pyglet 
import math 

class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)
        
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.dead = False
        self.new_objects = []

    def update(self, dt):
        """ update position """
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt