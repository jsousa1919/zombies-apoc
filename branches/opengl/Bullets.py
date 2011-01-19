import pygame, Util, math
from OpenGL.GL import *

#Shooting & Bullet Trails
BULLET_VELOCITY = 50
INCREMENTS = 60

#Damage Type
DMG_NORMAL = 1 < 0
DMG_FIRE = 1 < 1

class BulletMask:
	def __init__(self):
		self.mask = pygame.Mask((Util.WINDOW_WIDTH, Util.WINDOW_HEIGHT))
		self.bullets = {}

	def add(self, bullet):
		if 0 < bullet.posx < Util.WINDOW_WIDTH and 0 <= bullet.posy < Util.WINDOW_HEIGHT:
			self.bullets[(bullet.posx, bullet.posy)] = bullet
			self.mask.set_at((int(bullet.posx), int(bullet.posy)), True)

	def clear(self):
		self.mask.clear()
		self.bullets.clear()
		
	def update(self):
		self.mask.clear()
		for key,bullet in self.bullets.items():
			bullet.update()
			if 0 < bullet.posx < Util.WINDOW_WIDTH and 0 <= bullet.posy < Util.WINDOW_HEIGHT:
				self.mask.set_at((int(bullet.posx), int(bullet.posy)), True)
			else:
				self.bullets.pop(key)
		
class Bullet:
	def __init__(self, player, dtype):
		self.owner = player
		self.posx, self.posy = player.posx, player.posy
		self.angle = 360 - player.getMouseAngle()
		self.dmgtype = dtype
		self.rect = pygame.Rect(self.posx - Util.BULLET_SIZE/2, Util.WINDOW_HEIGHT - self.posy + Util.BULLET_SIZE/2, Util.BULLET_SIZE, Util.BULLET_SIZE)
		
	def update(self):
		delta = (BULLET_VELOCITY*math.cos(math.radians(self.angle)), BULLET_VELOCITY*math.sin(math.radians(self.angle)))
		
		self.posx += delta[0]
		self.posy += delta[1]
		self.rect.centerx += delta[0]
		self.rect.centery -= delta[1]
