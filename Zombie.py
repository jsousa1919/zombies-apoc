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
MAXHEALTH = 10

ST_DEAD = -1
ST_IDLE = 0
ST_SEARCHING = 1
ST_SWARMING = 2
ST_CHASING = 3
ST_ATTACKING = 4

class Zombie():
#init
	def __init__(self, player, swarm):
		self.swarm = swarm
		self.hero = player

		self.focus = 4
		self.endurance = 4
		self.sight = 2
		self.hp = 10

		Util.request_fov(self.sight)

		self.last_search = 0
		self.last_seen = 0
		self.last_swarm = 0
		self.start_swarm_tick = 0
		self.end_slow = 0

		self.hero_focus = None
		self.state = ST_IDLE
		self.speaking = False
		self.is_slow = False
		self.moving = False
		self.frame = 0
		self.tick = 0
		self.angle = random.randrange(0,360)
		self.angle_target = random.randrange(0,360)
		
		self.speed_mod = random.randrange(0, MINSPEED)
		self.speed = MINSPEED
		self.speed_target = MINSPEED

		random.seed()
		self.posx = random.random() * Util.WINDOW_WIDTH
		self.posy = random.random() * Util.WINDOW_HEIGHT
		self.rect = pygame.Rect((0,0), (Util.ZOM_SPRITE_WIDTH, Util.ZOM_SPRITE_HEIGHT)) 
		self.rect.center = (self.posx, self.posy)

		self.lkl = self.rect.center
		self.dist = 0

		self.update()
		
	def getDisplayList(self):
		if self.state == ST_DEAD:
			return Util.ZOM_DEAD_DISPLIST[self.frame % len(Util.ZOM_SPRITE_DEAD)]
		elif self.moving:
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
		if self.state == ST_DEAD and self.frame == len(UTIL.ZOM_DEAD_DISPLIST)-1:
			return
		self.tick += 1
		#if self.state != 0: print self.state

		#for hero in self.heroes:
		self.test_fov(self.hero)

		#state specific actions	
	
		if self.state == ST_IDLE:
			self.set_speed(MINSPEED)
			if (self.tick - self.last_search) > random.randrange(10 * self.focus * self.endurance, 15 * MAXFOCUS * MAXENDUR):
				self.investigate()				
			
		if self.state == ST_SEARCHING:
			if (self.tick - self.last_search) > random.randrange(10 * self.focus * self.endurance, 15 * MAXFOCUS * MAXENDUR):
				self.investigate()	
			if (self.tick - self.last_seen) > random.randrange(20 * self.endurance, 20 * MAXENDUR):
				self.state = ST_IDLE

		if self.state == ST_SWARMING:
			if (self.tick - self.start_swarm_tick) > random.randrange(25 * self.endurance, 25 * MAXENDUR):
				self.slow(4)

		if self.state == ST_CHASING:
			self.set_speed(MIDSPEED)
			if (self.last_seen - self.tick) > 5:
				self.state = ST_SEARCHING
			self.swarm.add(self.rect.center, self.lkl)
			if self.dist < 10:
				self.state = ST_ATTACKING

		if self.state == ST_ATTACKING:
			if self.dist > 10:
				self.state = ST_CHASING

		#check ailments
		if self.is_slow and self.tick > self.end_slow:
			self.is_slow == False

		self.goto_lkl()
		self.move()
	
	def test_fov(self, hero):
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
			self.last_seen = self.tick
			self.state = ST_CHASING
			self.set_speed(MIDSPEED)

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
	def go(self):
		self.moving = True

	def stop(self):
		self.end_swarm()
		self.state = ST_IDLE
		self.lkl = self.rect.center
		self.moving = False

	def set_center(self, x, y = None):
		if y != None:
			self.rect.center = (self.posx, self.posy) = (x, y)
		else:
			self.rect.center = (self.posx, self.posy) = x	

	def add_center(self, x, y = None):
		if y != None:
			self.rect.center = (self.posx, self.posy) = (self.posx + x, self.posy + y)
		else:
			self.rect.center = (self.posx, self.posy) = (self.posx + x[0], self.posy + x[1])

	def set_speed(self, speed):
		speed += self.speed_mod
		if self.is_slow:
			speed = speed / 2
		self.speed_target = speed

	def set_angle(self, theta):
		ang = int(theta) % 360
		self.angle_target = ang

	def move(self):	
		if self.tick % int(MAXSPEED + self.speed_mod / self.speed) == 0: 
			self.frame += 1
		if self.moving:
			if self.frame >= len(Util.ZOM_SPRITE_WALK): self.frame = 0

			if self.speed < self.speed_target: self.speed += 1
			elif self.speed > self.speed_target: self.speed -= 1

			ldiff = (self.angle_target - self.angle) % 360
			rdiff = (self.angle - self.angle_target) % 360
			if (ldiff < rdiff):
				dt = (self.angle + (ldiff / 5)) % 360
			else:
				dt = (self.angle - (rdiff / 5)) % 360
			self.angle = dt

			
			
			#print self.speed
			dx = self.speed*math.cos(math.radians(self.angle))
			dy = self.speed*math.sin(math.radians(self.angle))
			#print self.rect.center, " to ", self.lkl, " at ", self.angle
			self.add_center(dx, dy)

		else:
			self.end_swarm()
			if self.frame >= len(Util.ZOM_SPRITE_IDLE): self.frame = 0
		

#
	def investigate(self, rmin = 50, rmax = 500):
		x = random.randrange(rmin, rmax, 1)
		if x % 2 == 0: x = -x
		y = random.randrange(rmin, rmax, 1)
		if y % 2 == 0: y = -y

		self.lkl = self.lkl[0] + x, self.lkl[1] + y
		self.last_search = self.tick
		#print self.rect.center, " investigate ", self.lkl

		if random.randrange(0, 100) < self.speed:
			self.last_seen = self.tick
			self.try_swarm()

	def goto_lkl(self, nogo = 60):
		x, y = self.lkl
		self.dist = math.hypot(y - self.posy, x - self.posx)
		ang = math.degrees(math.atan2(y - self.posy, x - self.posx))
		self.set_angle(ang)
		
		#if self.moving: 
		#	print self.dist
		if self.dist <= nogo:
			self.stop()
		else:
			self.go()

	def try_swarm(self):
		if self.state == ST_ATTACKING or (self.tick - self.last_swarm) < (10 * self.focus) or (self.state == ST_SWARMING and (self.tick % 5) > 0):
			return
		num, to = self.swarm.swarm_movement(self)
		if num != 0 and random.randrange(0, 5 * self.focus) < num:
			self.start_swarm(to)

	def start_swarm(self, to):
		#print "swarm to", loc
		self.lkl = to
		self.last_seen = self.tick
		if self.state != ST_SWARMING:
			self.state = ST_SWARMING
			self.start_swarm_tick = self.tick
			

	def end_swarm(self):
		if self.state == ST_SWARMING:
			self.investigate(50, 100)
			self.state = ST_SEARCHING
			self.last_swarm = self.tick

	def prop_swarm(self):
		if Util.SUPERSWARM and self.state == ST_SWARMING:
			self.swarm.add(self.rect.center, self.rect.center)

	def slow(self, mod):
		if self.is_slow:
			self.end_slow += (mod * (MAXENDUR - self.endurance) * 4)
		else:
			self.end_slow = self.tick + (mod * (MAXENDUR - self.endurance) * 4)

#collision
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
		if self.state < ST_SWARMING and abs(180 - abs(ang - self.angle)) > 150 and random.randrange(0, MAXENDUR) > self.endurance:
			self.stop()
		x = mag*math.cos(math.radians(ang))
		y = mag*math.sin(math.radians(ang))
		self.add_center(x, y)

	def damage(self):
		self.health -= 5
		if self.health <= 0:
			self.state = ST_DEAD
			
