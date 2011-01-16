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
#ST_SWARMING
#ST_CHASING
ST_ATTACKING = 2

class Zombie():
#init
	def __init__(self, player, swarm):
		self.swarm = swarm
		self.hero = player

		self.focus = 4
		self.endurance = 4
		self.sight = 3

		Util.request_fov(self.sight)

		self.hero_focus = None
		self.state = ST_IDLE
		self.lt = 0
		self.swarming = False
		self.speaking = False
		self.MOVE = False
		self.frame = 0
		self.angle = random.randrange(0,360)
		self.tick = 0
		
		self.speed_mod = random.randrange(0, MINSPEED)
		self.set_speed(MINSPEED)

		random.seed()
		self.posx = random.random() * Util.WINDOW_WIDTH
		self.posy = random.random() * Util.WINDOW_HEIGHT
		self.rect = pygame.Rect((0,0), (Util.ZOM_SPRITE_WIDTH, Util.ZOM_SPRITE_HEIGHT)) 
		self.rect.center = (self.posx, self.posy)

		self.lkl = self.rect.center

		self.update()
		
	def getDisplayList(self):
		if self.MOVE:
			return Util.ZOM_WALK_DISPLIST[self.frame % len(Util.ZOM_SPRITE_WALK)]
		else:
			return Util.ZOM_IDLE_DISPLIST[self.frame % len(Util.ZOM_SPRITE_IDLE)]
			
	def draw(self):
		glLoadIdentity()
		
		glTranslatef(self.posx, self.posy, 0)
		glRotatef(self.angle, 0,0,1)
		glTranslatef(-(Util.ZOM_SPRITE_WIDTH / 2), -(Util.ZOM_SPRITE_HEIGHT / 2), 0)
		glCallList(self.getDisplayList())
		
		#print self.posx
		#print self.posy

#update
	def update(self):
		self.tick += 1

		#scale frame switching to zombie speed
		if self.tick % int(MAXSPEED + self.speed_mod / self.speed) == 0: 
			self.frame += 1

		#create field of view mask
		ang = int(self.angle / Util.ZOM_FOV_DEV)
		fov_image = Util.ZOM_FOV[self.sight][ang]
		fov_mask = Util.ZOM_FOV_MASK[self.sight][ang]

		#interact with hero
		#if self.tick % 5 == 0:
		hero_center = (self.hero.posx, self.hero.posy)
		world_diff = map(operator.sub, hero_center, self.rect.center) # actual position difference
		local_diff = map(operator.sub, fov_image.get_rect().center, (Util.HERO_SPRITE_WIDTH / 2, Util.HERO_SPRITE_HEIGHT / 2)) # difference to account for sprite size
		diff = map(int, map(operator.add, world_diff, local_diff))

		if fov_mask.overlap(Util.HERO_MASK, diff):
			#start hero sighted
			#self.speak() 
			#print "attack! ", hero_center
			self.hero_focus = self.hero
			self.lkl = hero_center
			self.lt = self.tick
			self.state = ST_ATTACKING
			self.end_swarm()
			self.set_speed(MIDSPEED)

		#state specific actions	
	
		if self.state == ST_ATTACKING:
			self.swarm.add(self.rect.center, self.lkl)

		if self.state == ST_ATTACKING and self.tick - self.lt > 10:
			self.state = ST_SEARCHING
	
		if self.state > ST_IDLE and (self.tick - self.lt) > (self.endurance * 25):
			self.stop()
			self.set_speed(MINSPEED)
			self.state = ST_IDLE

		if self.state < ST_ATTACKING:
			if (self.tick - self.lt) == random.randrange(75, (self.focus * self.speed * 25)):
				self.rand_lkl(100)

		self.goto_lkl()
		
		if self.MOVE:
			if self.frame >= len(Util.ZOM_SPRITE_WALK): self.frame = 0

			x = self.speed*math.cos(math.radians(self.angle))
			y = self.speed*math.sin(math.radians(self.angle))
			self.center(self.posx + x, self.posy + y)

		else:
			self.end_swarm()
			if self.frame >= len(Util.ZOM_SPRITE_IDLE): self.frame = 0
	
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
		
#movement
	def move(self):
		self.MOVE = True
	def stop(self):
		self.swarming = False
		self.MOVE = False

	def center(self, x, y = None):
		if y != None:
			(self.posx, self.posy) = self.rect.center = (x, y)
		else:
			(self.posx, self.posy) = self.rect.center = x	

	def set_speed(self, speed):
		self.speed = speed + self.speed_mod

	def set_angle(self, theta):
		ang = int(theta % 360)
		self.angle = ang

	def rotate(self, delta):
		self.set_angle(self.angle + delta)

	def rand_lkl(self, rmin = 0, rmax = 200):
		x = random.randrange(rmin, rmax, 1)
		if x % 2 == 0: x = -x
		y = random.randrange(rmin, rmax, 1)
		if y % 2 == 0: y = -y
		self.lkl = self.lkl[0] + x, self.lkl[1] + y
		if random.randrange(0, 100) < self.speed:
			self.swarming = True

	def goto_lkl(self, nogo = 20):
		x, y = self.lkl
		dist = math.hypot(y - self.posy, x - self.posx)
		ang = math.degrees(math.atan2((y - self.posy),(x - self.posx)))
		ldiff = (ang - self.angle) % 360
		rdiff = (self.angle - ang) % 360
		if (ldiff < rdiff):
			self.rotate(ldiff / 5)
		else:
			self.rotate(-rdiff / 5)
		
		if dist <= nogo:
			self.stop()
		else:
			self.move()
			x += random.randrange(0, self.focus * 4) - (self.focus * 2)
			y += random.randrange(0, self.focus * 4) - (self.focus * 2)
			self.lkl = (x, y)

	def try_swarm(self):
		if self.state != ST_ATTACKING and not (self.swarming and self.tick % 5 > 0):
			num, to = self.swarm.swarm_movement(self)
			if num != 0 and random.randrange(0, 5 * self.focus) < num:
				#print "swarm to", loc
				self.lkl = to
				self.lt = self.tick
				self.state = ST_SEARCHING
				self.swarming = True

	def prop_swarm(self):
		if Util.SUPERSWARM and self.swarming:
			self.swarm.add(self.rect.center, self.rect.center)
	
	def end_swarm(self):
		self.swarming == False

	def collide(self, other):
		x, y = other.rect.center
		dist = math.hypot(y - self.posy, x - self.posx)
		overlap = (Util.ZOM_SPRITE_WIDTH / 4) - dist
		if dist != 0 and overlap > 0:
			ang = math.degrees(math.atan2((y - self.posy),(x - self.posx)))
			other.push(overlap / 4, ang)
			self.push(overlap / 4, ang + 180)

	def push(self, mag, ang):
		ang %= 360
		if abs((180 - (ang - self.angle)) > 150):
			self.stop()
		else:
			self.move()
		x = mag*math.cos(math.radians(ang))
		y = mag*math.sin(math.radians(ang))
		self.center(self.posx + x, self.posy + y)
			
