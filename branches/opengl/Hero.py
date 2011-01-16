import pygame, sys, os, Zombie, math, Util
from OpenGL.GL import *
from pygame.locals import *

#Stats
RUNSPEED = 24
WALKSPEED = 15

#Sprite Direction Indices
LEFT = 0
UPLEFT = 1
UP = 2
UPRIGHT = 3
RIGHT = 4
DOWNRIGHT = 5
DOWN = 6
DOWNLEFT = 7

#Shooting & Bullet Trails
MAX_ZOMBIES_HIT = 4

#Constants
SQRT_2 = math.sqrt(2)

class Hero:
	def __init__(self):
		self.MOVE = False
		self.RUN = False
		self.SHOOT = False
		self.speed = WALKSPEED

		self.frame = 0
		self.direction = 2
		
		self.shoot_tick = 0
		self.shoot_ang = 0
		self.TRAIL_LENGTH = 0

		self.posx, self.posy = Util.WINDOW_WIDTH/2, Util.WINDOW_HEIGHT/2
		self.angle = 0

		self.update()
	
	def getDisplayList(self):
		if self.MOVE:
			return Util.HERO_WALK_DISPLIST[self.frame]
		else:
			return Util.HERO_IDLE_DISPLIST[self.frame]
			
	def draw(self):
		if self.SHOOT:
			tmp = self.shoot_tick - 8
			if tmp < 1: tmp = 1
			
			glLoadIdentity()
			glTranslatef(self.posx, self.posy, 0)
			for i in xrange(tmp, self.shoot_tick+1):
				glTranslatef(5*i,0,0)
				glCallList(Util.BULLET_DISPLIST[0])
			glLoadIdentity()
			glTranslatef(self.posx, self.posy, 0)
			glRotatef(self.shoot_angle, 0,0,1)
			
			self.shoot_tick += 1
			if (self.shoot_tick == self.TRAIL_LENGTH+1):
				self.shoot_tick = 0
				self.SHOOT = False
		
		glLoadIdentity()
		
		glTranslatef(self.posx, self.posy, 0)
		glRotatef(self.angle, 0,0,1)
		glTranslatef(-(Util.HERO_SPRITE_WIDTH / 2),-(Util.HERO_SPRITE_HEIGHT / 2), 0)
		glCallList(self.getDisplayList())
		
		#print self.posx
		#print self.posy
		
	def getMouseAngle(self):
		pos = pygame.mouse.get_pos()
		
		ang = math.degrees(math.atan2((Util.WINDOW_HEIGHT - pos[1] - self.posy),(pos[0] - self.posx)))
		
		return ang
		
	def update(self):
		self.frame += 1
		
		self.set_angle(self.getMouseAngle())
		
		if self.MOVE:
			if self.RUN:
				spd = RUNSPEED
			else:
				spd = WALKSPEED
			
			if self.direction == LEFT:
				self.posx -= spd
			elif self.direction == UPLEFT:
				self.posx -= spd/SQRT_2
				self.posy += spd/SQRT_2
			elif self.direction == UP:
				self.posy += spd
			elif self.direction == UPRIGHT:
				self.posy += spd/SQRT_2	
				self.posx += spd/SQRT_2
			elif self.direction == RIGHT:
				self.posx += spd
			elif self.direction == DOWNRIGHT:
				self.posy -= spd/SQRT_2
				self.posx += spd/SQRT_2
			elif self.direction == DOWN:
				self.posy -= spd
			elif self.direction == DOWNLEFT:
				self.posy -= spd/SQRT_2
				self.posx -= spd/SQRT_2
			
			if self.frame >= len(Util.HERO_WALK_DISPLIST): self.frame = 0
		else:
			if self.frame >= len(Util.HERO_IDLE_DISPLIST): self.frame = 0
				
	
	def face(self, dirind):
		self.direction = dirind
	
	def move(self, dirind): 
		self.face(dirind)
		self.MOVE = True
	def stop(self): self.MOVE = False

	def run(self): self.RUN = True
	def unrun(self): self.RUN = False
	
	def set_angle(self, theta):
		ang = int(theta % 360)
		self.angle = ang

	def rotate(self, delta):
		self.set_angle(self.angle + delta)
		
	def shoot(self):
		if not self.SHOOT:
			pos = pygame.mouse.get_pos()
			ang = math.degrees(math.atan2((Util.WINDOW_HEIGHT - pos[1] - self.posy),(pos[0] - self.posx)))
			self.shoot_ang = ang
			self.TRAIL_LENGTH = math.dist((self.posx, self.posy),(pos[0], Util.WINDOW_HEIGHT - pos[1]))
		
			self.SHOOT = True
			
		
