import pygame, sys, os, random, timer, math, time, operator, Util
from pygame.locals import *
from OpenGL.GL import *

#Stats
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

#Sprite Direction Indices
LEFT = 1
UPLEFT = 2
UP = 3
UPRIGHT = 4
RIGHT = 5
DOWNRIGHT = 6
DOWN = 7
DOWNLEFT = 0

class Zombie():
#init
	def __init__(self, player):
		self.hero = player

		self.focus = 4
		self.endurance = 4
		self.sight = 3

		Util.request_fov(self.sight)

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

		random.seed()
		self.posx = random.random() * Util.WINDOW_WIDTH
		self.posy = random.random() * Util.WINDOW_HEIGHT

		self.lkl = self.posx, self.posy

		self.update()
		
	def getDisplayList(self):
		if self.MOVE:
			return Util.ZOM_WALK_DISPLIST[self.direction][self.frame]
		else:
			return Util.ZOM_IDLE_DISPLIST[self.direction][self.frame]
			
	def draw(self):
		glLoadIdentity()
		glTranslatef(self.posx - Util.ZOM_SPRITE_WIDTH/2, self.posy - Util.ZOM_SPRITE_WIDTH/2, 0)
		glCallList(self.getDisplayList())

#update
	def update(self):
		self.tick += 1

		#scale frame switching to zombie speed
		if self.tick % int(MAXSPEED / self.speed) == 0: 
			self.frame += 1

		#create field of view mask
		fov_image = Util.ZOM_FOV[self.sight][int(self.angle / Util.ZOM_FOV_DEV)]
		fov_image.set_colorkey(pygame.Color('black'))
		fov_rect = fov_image.get_rect(center=(self.posx, self.posy))
		fov_mask = pygame.mask.from_surface(fov_image)

		#interact with heroes
		hero_center = (self.hero.posx, self.hero.posy)
		world_diff = map(operator.sub, hero_center, fov_image.get_rect().center) # actual position difference
		local_diff = map(operator.sub, fov_image.get_rect().center, hero_center) # difference to account for sprite size
		diff = map(operator.add, world_diff, local_diff)

		if fov_mask.overlap(Util.HERO_MASK, diff):
			#start hero sighted
			#self.speak() 
			#print "attack!"
			self.hero_focus = self.hero
			self.lkl = hero_center
			self.lt = self.tick
			self.state = ST_ATTACKING
			self.speed = MIDSPEED

		#state specific actions
		if self.state == ST_ATTACKING and self.lt != self.tick:
			self.state = ST_SEARCHING
	
		if self.state > ST_IDLE and (self.tick - self.lt) > (self.endurance * 100):
			self.stop()
			self.speed = MINSPEED
			self.state = ST_IDLE

		if self.state < ST_ATTACKING:
			if (self.tick - self.lt) % (self.focus * 25) == 0:
				self.rand_lkl(50)

		self.goto_lkl()
		
		if self.MOVE:
			if self.frame >= len(Util.ZOM_SPRITE_WALK[self.direction]): self.frame = 0

			x = self.speed*math.cos(math.radians(self.angle))
			y = self.speed*math.sin(math.radians(self.angle))
			self.posx += x
			self.posy += y

		else:
			if self.frame >= len(Util.ZOM_SPRITE_IDLE[self.direction]): self.frame = 0																		# for invisible FOV
	
#actions
	def speak(self):
		if self.speaking:
			return
		id = random.randrange(1,24,1)
		file_path = os.path.join(Util.SOUND_DIR, 'zombie-%d.ogg' % id)
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

	def rotate(self, delta):
		self.set_angle(self.angle + delta)

	def rand_lkl(self, rmin = 0, rmax = 200):
		x = random.randrange(rmin, rmax, 1)
		if x % 2 == 0: x = -x
		y = random.randrange(rmin, rmax, 1)
		if y % 2 == 0: y = -y
		self.lkl = self.lkl[0] + x, self.lkl[1] + y

	def goto_lkl(self, nogo = 65):
		x, y = self.lkl
		dist = math.hypot(y - self.posy, x - self.posx)
		ang = math.degrees(math.atan2((self.posy - y),(x - self.posx)))
		self.set_angle(ang)
		
		if dist <= nogo:
			self.stop()
		else:
			self.move()
