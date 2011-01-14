import pygame, sys, os, Zombie, random, math
from pygame.locals import *

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000
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

		self.master_image = pygame.image.load(os.path.join("data","male_unarmored.png")).convert_alpha()

		self.idle_sprites = self.__load_idle_sprites__()
		self.walk_sprites = self.__load_walk_sprites__()
		self.run_sprites = self.__load_run_sprites__()
			  
		self.direction = 0
		self.MOVE = False
		self.RUN = False
		self.speed = WALKSPEED

		self.rect = self.idle_sprites[0][0].get_rect()
		self.frame = 0

		self.area = self.screen.get_rect()

		random.seed()
		x = random.random() * WINDOW_WIDTH
		y = random.random() * WINDOW_HEIGHT

		self.rect.topleft = x, y

		self.update()
    
	def __load_idle_sprites__(self, w = 256, h = 256):
		'''
		THE HERO SPRITE HAS A WIDTH, HEIGHT of 256
		'''
		images = []

		for i in xrange(0,8):
		    images.append([])
		    for j in xrange(0,1):
			images[i].append(self.master_image.subsurface((j*w, i*h, w, h)))

		return images

	def __load_walk_sprites__(self, w = 256, h = 256):
		'''
		THE HERO SPRITE HAS A WIDTH, HEIGHT of 256
		'''
		images = []

		for i in xrange(0,8):
		    images.append([])
		    for j in xrange(0,4):
			images[i].append(self.master_image.subsurface((j*w, i*h, w, h)))

		return images

	def __load_run_sprites__(self, w = 256, h = 256):
		'''
		THE HERO SPRITE HAS A WIDTH, HEIGHT of 256
		'''
		images = []

		for i in xrange(0,8):
		    images.append([])
		    for j in xrange(4,6):
			images[i].append(self.master_image.subsurface((j*w, i*h, w, h)))

		return images

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
		
				if self.frame >= len(self.run_sprites[self.direction]): self.frame = 0
				self.image = self.walk_sprites[self.direction][self.frame]
			else:
				if self.frame >= len(self.walk_sprites[self.direction]): self.frame = 0
				self.image = self.walk_sprites[self.direction][self.frame]

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
			if self.frame >= len(self.idle_sprites[self.direction]): self.frame = 0
			self.image = self.idle_sprites[self.direction][self.frame]

	def move(self, dirindex):
		self.direction = dirindex
		self.MOVE = True

	def run(self): self.RUN = True
	def unrun(self): self.RUN = False
