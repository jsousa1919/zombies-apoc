import pygame, sys, os, Zombie, random, math, media
from pygame.locals import *

RUNSPEED = 24
WALKSPEED = 15
LEFT = 0
UPLEFT = 1
UP = 2
UPRIGHT = 3
RIGHT = 4
DOWNRIGHT = 5
DOWN = 6
DOWNLEFT = 7


class Hero(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.screen = pygame.display.get_surface()
			  
		self.direction = 0
		self.MOVE = False
		self.RUN = False
		self.speed = WALKSPEED

		self.frame = 0

		self.area = self.screen.get_rect()

		random.seed()
		x = random.random() * media.WINDOW_WIDTH
		y = random.random() * media.WINDOW_HEIGHT

		self.rect = media.HERO_SPRITE_IDLE[0][0].get_rect(center=(x, y))
		self.image = media.HERO_SPRITE_IDLE[0][0]

		self.update()


	def update(self):
		self.frame += 1
		if self.MOVE:
			spd = WALKSPEED
	 
			if self.RUN:
				spd = RUNSPEED
				file = 'fall.ogg'
				file = os.path.join('sounds',file)
				 
				try:
				    randsound = pygame.mixer.Sound(file)
				except:
				    #print "fuck you"
				    randound = None
				if randsound:
				    randsound.play()
		
				if self.frame >= len(media.HERO_SPRITE_RUN[self.direction]): self.frame = 0
				self.image = media.HERO_SPRITE_RUN[self.direction][self.frame]
			else:
				if self.frame >= len(media.HERO_SPRITE_WALK[self.direction]): self.frame = 0
				self.image = media.HERO_SPRITE_WALK[self.direction][self.frame]

			sqrt_2 = math.sqrt(2)
			if self.direction == 0:
				self.rect.centerx -= spd
			elif self.direction == 1:
				self.rect.centerx -= spd/sqrt_2
				self.rect.centery -= spd/sqrt_2
			elif self.direction == 2:
				self.rect.centery -= spd
			elif self.direction == 3:
				self.rect.centery -= spd/sqrt_2	
				self.rect.centerx += spd/sqrt_2
			elif self.direction == 4:
				self.rect.centerx += spd
			elif self.direction == 5:
				self.rect.centery += spd/sqrt_2
				self.rect.centerx += spd/sqrt_2
			elif self.direction == 6:
				self.rect.centery += spd
			elif self.direction == 7:
				self.rect.centery += spd/sqrt_2
				self.rect.centerx -= spd/sqrt_2
			    
			self.MOVE = False
		else:
			if self.frame >= len(media.HERO_SPRITE_IDLE[self.direction]): self.frame = 0
			self.image = media.HERO_SPRITE_IDLE[self.direction][self.frame]

	def move(self, dirindex):
		self.direction = dirindex
		self.MOVE = True

	def run(self): self.RUN = True
	def unrun(self): self.RUN = False
