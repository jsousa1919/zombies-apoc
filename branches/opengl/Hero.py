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

#Constants
SQRT_2 = math.sqrt(2)

class Hero:
	def __init__(self):
		self.MOVE = False
		self.RUN = False
		self.speed = WALKSPEED

		self.direction = 0
		self.frame = 0

		self.posx, self.posy = 50, 50
		self.angle = 0

		self.update()
	
	def getDisplayList(self):
		if self.MOVE:
			return Util.HERO_WALK_DISPLIST[self.direction][self.frame]
		else:
			return Util.HERO_IDLE_DISPLIST[self.direction][self.frame]
			
	def draw(self):
		glLoadIdentity()
		glTranslatef(self.posx, self.posy, 0)
		glCallList(self.getDisplayList())
		
	def update(self):
		self.frame += 1
		
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
			
			if self.frame >= len(Util.HERO_WALK_DISPLIST[self.direction]): self.frame = 0
		else:
			if self.frame >= len(Util.HERO_IDLE_DISPLIST[self.direction]): self.frame = 0

	def face(self, dirindex):
		if self.direction != dirindex:
			self.direction = dirindex
	
	def move(self, dirindex):
		self.face(dirindex)
		self.MOVE = True
	def stop(self):
		self.MOVE = False

	def run(self): self.RUN = True
	def unrun(self): self.RUN = False
	
	def set_angle(self, theta):
		ang = int(theta % 360)
		self.angle = ang

		if ang >= 338 or ang < 23:
			self.face(RIGHT)
		elif 23 <= ang < 68:
			self.face(UPRIGHT)
		elif 68 <= ang < 113:
			self.face(UP)
		elif 113 <= ang < 158:
			self.face(UPLEFT)
		elif 158 <= ang < 203:
			self.face(LEFT)
		elif 203 <= ang < 248:
			self.face(DOWNLEFT)
		elif 248 <= ang < 293:
			self.face(DOWN)
		else:
			self.face(DOWNRIGHT)

	def rotate(self, delta):
		self.set_angle(self.angle + delta)
