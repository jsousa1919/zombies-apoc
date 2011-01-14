import pygame, sys, os, random, timer, math, time
from pygame.locals import *

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000
MAXSPEED = 12
MIDSPEED = 8
MINSPEED = 4
LEFT = 0
UPLEFT = 1
UP = 2
UPRIGHT = 3
RIGHT = 4
DOWNRIGHT = 5
DOWN = 6
DOWNLEFT = 7

class Zombie(pygame.sprite.Sprite):
	def __init__(self, herogroup):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		pygame.mixer.init(11025)
		self.screen = pygame.display.get_surface()

		self.master_image = pygame.image.load(os.path.join("data","zombie_0.png"))

		self.idle_sprites = self.__load_idle_sprites__()
		self.walk_sprites = self.__load_walk_sprites__()

		self.heroes = herogroup

		self.angle = 0

		self.tick = 0
		self.direction = 0

		self.speaking = False
		self.MOVE = False

		self.rect = self.idle_sprites[0][0].get_rect()
		self.frame = 0

		self.area = self.screen.get_rect()
		self.speed = MINSPEED

		random.seed()
		x = random.random() * WINDOW_WIDTH
		y = random.random() * WINDOW_HEIGHT

		self.rect.topleft = x, y

		self.update()


	def __load_idle_sprites__(self, w = 128, h = 128):
		'''
		ZOMBIE SPRITES HAVE A WIDTH, HEIGHT of 128
		'''
		images = []

		for i in xrange(0, 8):
			images.append([])
			for j in xrange(0, 4):
				images[i].append(self.master_image.subsurface((j*w, i*h, w, h)))

		return images

	def __load_walk_sprites__(self, w = 128, h = 128):
		'''
		ZOMBIE SPRITES HAVE A WIDTH, HEIGHT of 128
		'''
		images = []

		for i in xrange(0,8):
			images.append([])
			for j in xrange(4,12):
				images[i].append(self.master_image.subsurface((j*w, i*h, w, h)))

		return images

	def speak(self):
		if self.speaking:
			return
		id = random.randrange(1,24,1)
		file_path = os.path.join('sounds', 'zombie-%d.ogg' % id)
		sound = pygame.mixer.Sound(file_path)

		#print ('Playing Sound...')
		self.speaking = True
		channel = sound.play()
		t = timer.ttimer(0.5, 1, self.endspeak, channel)
		t.Start()

	def endspeak(self, channel):
		if not channel.get_busy():
			self.speaking = False
			#print ('...Finished')
		else:
			t = timer.ttimer(0.5, 1, self.endspeak, channel)
			t.Start()
    
	def update(self):
		self.tick += 1
		if self.tick % int(MAXSPEED / self.speed) == 0: 
			self.frame += 1

		if self.MOVE:
			if self.frame >= len(self.walk_sprites[self.direction]): self.frame = 0
			self.image = self.walk_sprites[self.direction][self.frame]

			x = self.speed*math.cos(math.radians(self.angle))
			y = self.speed*math.sin(math.radians(self.angle))
			self.rect.centerx += x
			self.rect.centery -= y
		else:
			if self.frame >= len(self.idle_sprites[self.direction]): self.frame = 0
			self.image = self.idle_sprites[self.direction][self.frame]
		
		self.look_for_food()

	def face(self, dirindex):
		if self.direction != dirindex: 
			self.speak()
			self.direction = dirindex
        
	def set_angle(self, theta):
		ang = theta % 360
	    
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
		    
		self.angle = ang

	def add_to_angle(self, delta):
		self.set_angle(self.angle + delta)

	def move(self):
		self.MOVE = True
	def stop(self):
		self.MOVE = False

	def look_for_food(self):
		for hero in self.heroes:
			x = hero.rect.centerx
			y = hero.rect.centery

			dist = math.sqrt(math.pow(y - self.rect.centery, 2) + math.pow(x - self.rect.centerx, 2))

			ang = math.degrees(math.atan2((self.rect.centery - y),(x - self.rect.centerx)))

			self.set_angle(ang)
			
			if dist <= 65:
				self.stop()
			else:
				self.move()
