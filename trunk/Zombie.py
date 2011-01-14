import pygame, sys, os, random, timer, math, time, operator
from pygame.locals import *

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000

MAXSPEED = 12
MIDSPEED = 8
MINSPEED = 4
MINFOCUS = 1
MAXFOCUS = 10
MINENDUR = 1
MAXENDUR = 10
MINSIGHT = 200
MAXSIGHT = 2000

ST_IDLE = 0
ST_SEARCHING = 1
ST_ATTACKING = 2

LEFT = 1
UPLEFT = 2
UP = 3
UPRIGHT = 4
RIGHT = 5
DOWNRIGHT = 6
DOWN = 7
DOWNLEFT = 0

class Zombie(pygame.sprite.Sprite):
	def __init__(self, herogroup):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		pygame.mixer.init(11025)
		self.screen = pygame.display.get_surface()
		self.fov_image = pygame.Surface((400,400))
		pygame.draw.polygon(self.fov_image, pygame.Color('0xFF000040'), [(200, 200), (400, 100), (400, 300)])

		self.master_image = pygame.image.load(os.path.join("data","zombie_1.png")).convert_alpha()

		self.idle_sprites = self.__load_idle_sprites__()
		self.walk_sprites = self.__load_walk_sprites__()

		self.heroes = herogroup
		self.hero_focus = None
		self.state = ST_IDLE
		self.lt = 0

		self.angle = 0

		self.tick = 0
		self.direction = 0

		self.focus = 4
		self.endurance = 4
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
		self.lkl = x, y

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

		#self.goto_lkl()
		self.image = pygame.transform.rotate(self.fov_image, self.angle)
		self.rect = self.image.get_rect(center=self.rect.center)
		self.image.set_colorkey(pygame.Color('black'))

		fov = pygame.mask.from_surface(self.image)
		for hero in self.heroes:
			hero_center = hero.rect.center
			hero_mask = pygame.mask.from_surface(hero.image)
			world_diff = map(operator.sub, hero.rect.center, self.rect.center)
			local_diff = map(operator.sub, self.image.get_rect().center, hero.image.get_rect().center)
			diff = map(operator.add, world_diff, local_diff)
			if fov.overlap(hero_mask, diff):
				#start hero sighted
				#self.speak() 
				self.hero_focus = hero
				self.lkl = hero_center
				self.lt = self.tick
				self.state = ST_ATTACKING
				self.speed = MIDSPEED

		if self.state > ST_IDLE and self.tick - self.lt > self.endurance * 100:
			self.stop()
			self.speed = MINSPEED
			self.state = ST_IDLE

		if self.state == ST_IDLE:
			if self.tick % (self.focus * 1000) == 0:
				print "change"
				self.lkl = self.lkl[0] + ((random.random() - 0.5) * 3000), self.lkl[1] + ((random.random() - 0.5) * 3000)
			self.goto_lkl(MAXSPEED,50)
			if self.MOVE == False:
				self.add_to_angle(self.focus * (random.random() - 0.5) * 20)

		if self.state > ST_IDLE:
			self.goto_lkl()

		if self.MOVE:
			if self.frame >= len(self.walk_sprites[self.direction]): self.frame = 0
			im = self.walk_sprites[self.direction][self.frame]
			#self.image.blit(im, map(operator.sub, self.image.get_rect().center, im.get_rect().center))
			self.image = im
			self.rect = im.get_rect(center=self.rect.center)

			x = self.speed*math.cos(math.radians(self.angle))
			y = self.speed*math.sin(math.radians(self.angle))
			self.rect.centerx += x
			self.rect.centery -= y

		else:
			if self.frame >= len(self.idle_sprites[self.direction]): self.frame = 0
			im = self.idle_sprites[self.direction][self.frame]
			#self.image.blit(im, map(operator.sub, self.image.get_rect().center, im.get_rect().center))
			self.image = im
			self.rect = im.get_rect(center=self.rect.center)
		
	def face(self, dirindex):
		if self.direction != dirindex: 
			#self.speak()
			self.direction = dirindex
		
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
			
		self.angle = ang

	def add_to_angle(self, delta):
		self.set_angle(self.angle + delta)

	def move(self):
		self.MOVE = True
	def stop(self):
		self.MOVE = False

	def goto_lkl(self, nogo = 65, rr = 20):
		x, y = self.lkl
		x += ((random.random() - 0.5) * rr)
		y += ((random.random() - 0.5) * rr)
		dist = math.hypot(y - self.rect.centery, x - self.rect.centerx)
		self.lkl = x, y

		if dist <= nogo:
			self.stop()
		else:
			self.move()
			ang = math.degrees(math.atan2((self.rect.centery - y),(x - self.rect.centerx)))
			self.set_angle(ang)
		
		
