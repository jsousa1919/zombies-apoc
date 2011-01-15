import pygame, sys, os, random, timer, math, time, operator, media
from pygame.locals import *

MAXSPEED = 12
MIDSPEED = 8
MINSPEED = 4
MINFOCUS = 1
MAXFOCUS = 10
MINENDUR = 1
MAXENDUR = 10
MINSIGHT = 1
MAXSIGHT = 10

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
#init
	def __init__(self, herogroup):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		self.screen = pygame.display.get_surface()
		self.area = self.screen.get_rect()

		self.heroes = herogroup

		self.focus = 4
		self.endurance = 4
		self.sight = 2

		media.request_fov(self.sight)

		self.hero_focus = None
		self.state = ST_IDLE
		self.lt = 0
		self.speaking = False
		self.MOVE = False
		self.frame = 0
		self.angle = 0
		self.tick = 0
		self.direction = 0
		self.speed = MINSPEED
		self.speed_mod = random.randrange(0, MINSPEED)

		random.seed()
		x = random.random() * media.WINDOW_WIDTH
		y = random.random() * media.WINDOW_HEIGHT

		self.image = media.ZOM_SPRITE_IDLE[0][0]
		self.rect = media.ZOM_SPRITE_IDLE[0][0].get_rect(center=(x,y))

		self.lkl = x, y

		self.update()

#update
	def update(self):
		
		self.tick += 1

		#scale frame switching to zombie speed
		if self.tick % int((MAXSPEED + self.speed_mod )/ self.speed) == 0: 
			self.frame += 1			

		#create field of view mask
		fov_image = media.ZOM_FOV[self.sight][int(self.angle / media.ZOM_FOV_DEV)]
		fov_rect = fov_image.get_rect(center=self.rect.center)

		# for viewing FOV
		#self.image = fov_image = media.ZOM_FOV[self.sight][int(self.angle / media.ZOM_FOV_DEV)]
		#self.rect = self.image.get_rect(center=self.rect.center)

		fov_mask = pygame.mask.from_surface(fov_image)

		#interact with heroes
		if self.tick % 5 == 0:
			for hero in self.heroes:
				hero_center = hero.rect.center
				world_diff = map(operator.sub, hero_center, self.rect.center) # actual position difference
				local_diff = map(operator.sub, fov_image.get_rect().center, hero.image.get_rect().center) # difference to account for sprite size
				diff = map(operator.add, world_diff, local_diff)

				if fov_mask.overlap(media.HERO_MASK, diff):
					#start hero sighted
					#self.speak() 
					#print "attack!"
					self.hero_focus = hero
					self.lkl = hero_center
					self.lt = self.tick
					self.state = ST_ATTACKING
					self.set_speed(MIDSPEED)

		#state specific actions
		if self.state == ST_ATTACKING and self.tick - self.lt > 5:
			self.state = ST_SEARCHING
	
		if self.state > ST_IDLE and (self.tick - self.lt) > (self.endurance * 100):
			self.stop()
			self.set_speed(MINSPEED)
			self.state = ST_IDLE

		if self.state < ST_ATTACKING:
			if (self.tick - self.lt) % (self.focus * 25) == 0:
				#print "change"
				self.rand_lkl(50)
			#if self.MOVE == False:
			#	self.add_to_angle(self.focus * (random.random() - 0.5) * 20)

		self.goto_lkl()

		#draw zombie
		if self.MOVE:
			if self.frame >= len(media.ZOM_SPRITE_WALK[self.direction]): self.frame = 0
			im = media.ZOM_SPRITE_WALK[self.direction][self.frame]

			x = self.speed*math.cos(math.radians(self.angle))
			y = self.speed*math.sin(math.radians(self.angle))
			self.rect.centerx += x
			self.rect.centery -= y

		else:
			if self.frame >= len(media.ZOM_SPRITE_IDLE[self.direction]): self.frame = 0
			im = media.ZOM_SPRITE_IDLE[self.direction][self.frame]
		
		#self.image.blit(im, map(operator.sub, self.image.get_rect().center, im.get_rect().center))	# for viewing FOV
		self.image = im																				# for invisible FOV

#actions
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
		

	def face(self, dirindex):
		if self.direction != dirindex: 
			#self.speak()
			self.direction = dirindex
		
#movement
	def move(self):
		self.MOVE = True
	def stop(self):
		self.MOVE = False


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

	def set_speed(self, speed):
		self.speed = speed + self.speed_mod

	def rand_lkl(self, rmin = 0, rmax = 200):
		x = random.randrange(rmin, rmax, 1)
		if x % 2 == 0: x = -x
		y = random.randrange(rmin, rmax, 1)
		if y % 2 == 0: y = -y
		self.lkl = self.lkl[0] + x, self.lkl[1] + y

	def goto_lkl(self, nogo = 65):
		x, y = self.lkl
		dist = math.hypot(y - self.rect.centery, x - self.rect.centerx)
		ang = math.degrees(math.atan2((self.rect.centery - y),(x - self.rect.centerx)))
		ldiff = (ang - self.angle) % 360
		rdiff = (self.angle - ang) % 360
		if (ldiff < rdiff):
			self.add_to_angle(ldiff / 5)
		else:
			self.add_to_angle(-rdiff / 5)
#		self.set_angle(ang)
		
		if dist <= nogo:
			self.stop()
		else:
			self.move()
