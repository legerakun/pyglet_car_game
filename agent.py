import pyglet 
import math 
import os

from pyglet.window import Window
from pyglet import image
from pyglet import shapes
from pyglet.window import key
from pyglet.gl import *

from physobj import PhysicalObject

car_image = pyglet.resource.image('car.png')

def clip(x, a ,b):
	if x < a:
		return a
	elif x >= b:
		return b
	return x

def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy	

class Player(PhysicalObject):
	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(img=car_image, *args, **kwargs)

		self.rotate_speed = 150.0
		self.max_velocity = 1500
		self.acceleration = 2000
		self.force_friction = 0.9

		self.radars =[]
		self.collision_points = []

		self.scale = 0.7

		self.is_alive = True

		self.key_handler = key.KeyStateHandler()

	def forward_velocity(self):
		velocity_x = self.velocity_x
		velocity_y = self.velocity_y

		speed = math.sqrt(velocity_x * velocity_x) + math.sqrt(velocity_y * velocity_y)

		return math.floor(speed)

	def car_rotation(self):
		angle_radians = -math.radians(self.rotation) 

		return angle_radians	

	def comp_center(self):
		self.car_xy = [self.x, self.y]
		self.car_ij = [self.x + 60*self.scale/2,self.y + 40*self.scale/2]
		self.car_center = rotate(self.car_xy,self.car_ij, self.car_rotation())

	def draw_center(self, taken_batch):
		self.comp_center()
		self.circle = shapes.Circle(math.floor(self.car_center[0]), math.floor(self.car_center[1]), 5, color=(0,72,186), batch=taken_batch)

	def comp_radars(self, deg, road):
		length = 0

		a = (GLubyte * 1)(0)
		x = int(self.car_center[0] + math.cos(math.radians(360 - (self.rotation + deg))) * length)
		y = int(self.car_center[1] + math.sin(math.radians(360 - (self.rotation + deg))) * length)

		while not road.check_color(x, y) == 104 and length < 300:
			length = length + 1
			x = int(self.car_center[0] + math.cos(math.radians(360 - (self.rotation + deg))) * length)
			y = int(self.car_center[1] + math.sin(math.radians(360 - (self.rotation + deg))) * length)

		dist = int(math.sqrt(math.pow(x - self.car_center[0], 2) + math.pow(y - self.car_center[1], 2)))
		self.radars.append([(x, y), dist]) 

	def draw_radars(self, taken_batch):
		r = self.radars

		p1, d1 = r[0] # Sry for busy code
		p2, d2 = r[1]
		p3, d3 = r[2]
		p4, d4 = r[3]
		p5, d5 = r[4]

		self.line_1 = shapes.Line(self.car_center[0], self.car_center[1], p1[0],p1[1], width=1, color = (183,235,70), batch=taken_batch) 
		self.circle_1 = shapes.Circle(p1[0],p1[1], 5, color=(183,235,70), batch=taken_batch)
		self.line_2 = shapes.Line(self.car_center[0], self.car_center[1], p2[0],p2[1], width=1, color = (183,235,70), batch=taken_batch) 
		self.circle_2 = shapes.Circle(p2[0],p2[1], 5, color=(183,235,70), batch=taken_batch)
		self.line_3 = shapes.Line(self.car_center[0], self.car_center[1], p3[0],p3[1], width=1, color = (183,235,70), batch=taken_batch) 
		self.circle_3 = shapes.Circle(p3[0],p3[1], 5, color=(183,235,70), batch=taken_batch)
		self.line_4 = shapes.Line(self.car_center[0], self.car_center[1], p4[0],p4[1], width=1, color = (183,235,70), batch=taken_batch) 
		self.circle_4 = shapes.Circle(p4[0],p4[1], 5, color=(183,235,70), batch=taken_batch)
		self.line_5 = shapes.Line(self.car_center[0], self.car_center[1], p5[0],p5[1], width=1, color = (183,235,70), batch=taken_batch) 
		self.circle_5 = shapes.Circle(p5[0],p5[1], 5, color=(183,235,70), batch=taken_batch)

	def comp_collision_points(self):
		#self.comp_center()
		lw = 36 * self.scale
		lh = 56 * self.scale

		self.car_xy = [self.x, self.y]
		self.car_ij = [self.x + 60*self.scale/2, self.y + 40*self.scale/2]
		self.car_center = rotate(self.car_xy,self.car_ij, self.car_rotation())

		lt = [self.x, self.y]
		rt = rotate(lt,(self.x + (self.scale * 60), self.y + (self.scale * 40)), self.car_rotation())
		lb = rotate(lt,(self.x + (self.scale * 60), self.y), self.car_rotation())
		rb = rotate(lt,(self.x, self.y + (self.scale * 40)), self.car_rotation())

		self.collision_points = [lt, rt, lb, rb]

	def draw_collision_points(self, road, taken_batch):
		self.comp_collision_points()

		p = self.collision_points
		x1, y1 = p[0]
		x2, y2 = p[1]
		x3, y3 = p[2]
		x4, y4 = p[3]
		rc1 = road.check_color(int(x1), int(y1))
		rc2 = road.check_color(int(x2), int(y2))
		rc3 = road.check_color(int(x3), int(y3))
		rc4 = road.check_color(int(x4), int(y4))

		if(rc1 == 104) or(rc2 == 104) or(rc3 == 104) or(rc4 == 104):
			self.circle1 = shapes.Circle(x1,y1, 5, color=(255,0,0), batch=taken_batch)
			self.circle2 = shapes.Circle(x2,y2, 5, color=(255,0,0), batch=taken_batch)
			self.circle3 = shapes.Circle(x3,y3, 5, color=(255,0,0), batch=taken_batch)
			self.circle4 = shapes.Circle(x4,y4, 5, color=(255,0,0), batch=taken_batch)

		elif(rc1 == 27) or(rc2 == 27) or(rc3 == 27) or(rc4 == 27):
			self.circle1 = shapes.Circle(x1,y1, 5, color=(15,255,15), batch=taken_batch)
			self.circle2 = shapes.Circle(x2,y2, 5, color=(15,255,15), batch=taken_batch)
			self.circle3 = shapes.Circle(x3,y3, 5, color=(15,255,15), batch=taken_batch)
			self.circle4 = shapes.Circle(x4,y4, 5, color=(15,255,15), batch=taken_batch)

		else:
			self.circle1 = shapes.Circle(x1,y1, 5, color=(15,192,252), batch=taken_batch)
			self.circle2 = shapes.Circle(x2,y2, 5, color=(15,192,252), batch=taken_batch)
			self.circle3 = shapes.Circle(x3,y3, 5, color=(15,192,252), batch=taken_batch)
			self.circle4 = shapes.Circle(x4,y4, 5, color=(15,192,252), batch=taken_batch)


	def check_collision(self, road):
		p = self.collision_points
		x1, y1 = p[0]
		x2, y2 = p[1]
		x3, y3 = p[2]
		x4, y4 = p[3]
		rc1 = road.check_color(int(x1), int(y1))
		rc2 = road.check_color(int(x2), int(y2))
		rc3 = road.check_color(int(x3), int(y3))
		rc4 = road.check_color(int(x4), int(y4))

		if(rc1 == 104) or(rc2 == 104) or(rc3 ==104) or(rc4 == 104):
			self.is_alive = False		

	def update(self, dt, key_handler, taken_batch):
		super(Player, self).update(dt)

		if key_handler[key.LEFT]:
			if (self.forward_velocity() > 140) or (self.forward_velocity() < -140):
				self.rotation -= self.rotate_speed * dt	

		if key_handler[key.RIGHT]:
			if (self.forward_velocity() > 140) or (self.forward_velocity() < -140):
				self.rotation += self.rotate_speed * dt

		if key_handler[key.UP]:
			force_x = math.cos(self.car_rotation()) * self.acceleration * dt
			force_y = math.sin(self.car_rotation()) * self.acceleration * dt
			self.velocity_x += force_x
			self.velocity_y += force_y

		if key_handler[key.DOWN]:
			force_x = math.cos(self.car_rotation()) * (self.acceleration/2) * dt
			force_y = math.sin(self.car_rotation()) * (self.acceleration/2) * dt
			self.velocity_x -= force_x
			self.velocity_y -= force_y	

		mv = self.max_velocity

		self.velocity_x = clip(self.velocity_x, -mv,mv) * self.force_friction
		self.velocity_y = clip(self.velocity_y, -mv,mv)	* self.force_friction			
	
	def delete(self):
		super(Player, self).delete()