import pygame, sys, os, Zombie, math, Util, Bullets
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
	def __init__(self, ):
		self.MOVE = False
		self.RUN = False
		self.SHOOT = False
		self.speed = WALKSPEED

		self.frame = 0
		self.direction = 4

		self.posx, self.posy = Util.WINDOW_WIDTH/2, Util.WINDOW_HEIGHT/2
		self.angle = 0
		self.shoot_angle = 0
		self.shoot_tick = 1

		self.update()
	
	def getDisplayList(self):
		if self.MOVE:
			return Util.HERO_WALK_DISPLIST[self.frame]
		else:
			return Util.HERO_IDLE_DISPLIST[self.frame]
			
	def draw(self):
		if self.SHOOT:
			glLoadIdentity()
			#glTranslatef(self.posx, self.posy, 0)
			
			delx = (Bullets.BULLET_VELOCITY/Bullets.INCREMENTS)*math.cos(math.radians(self.shoot_angle))
			dely = (Bullets.BULLET_VELOCITY/Bullets.INCREMENTS)*math.sin(math.radians(self.shoot_angle))
			
			#glTranslatef(self.shoot_tick*delx, self.shoot_tick*dely, 0)
			#glCallList(Util.BULLET_DISPLIST[0])
			
			glBegin(GL_LINES)
			glColor3f(1.0,0.0,0.0)
			glVertex2f(self.posx, self.posy)
			glVertex2f(self.posx + delx*Bullets.INCREMENTS, self.posy + dely*Bullets.INCREMENTS)
			glColor3f(1.0,1.0,1.0)
			glEnd()
			
			self.shoot_tick += 1
			if self.shoot_tick > Bullets.INCREMENTS:
				self.SHOOT = False
				self.shoot_tick = 0
		
		glLoadIdentity()
		glTranslatef(self.posx, self.posy, 0)
		glRotatef(self.angle, 0,0,1)
		glTranslatef(-(Util.HERO_SPRITE_WIDTH / 2),-(Util.HERO_SPRITE_HEIGHT / 2), 0)
		glCallList(self.getDisplayList())
		
	def getMouseAngle(self):
		pos = pygame.mouse.get_pos()
		
		ang = int(math.degrees(math.atan2((Util.WINDOW_HEIGHT - pos[1] - self.posy),(pos[0] - self.posx))))
		
		return ang
		
	def update(self):
		self.frame += 1
		
		self.set_angle(self.getMouseAngle())
		
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
			
			if self.frame >= len(Util.HERO_WALK_DISPLIST): self.frame = 0
		else:
			if self.frame >= len(Util.HERO_IDLE_DISPLIST): self.frame = 0
			
		if not self.SHOOT and pygame.mouse.get_pressed()[0]:
			self.shoot()
				
	
	def face(self, dirind):
		self.direction = dirind
	
	def move(self, dirind): 
		self.face(dirind)
		self.MOVE = True
	def stop(self): self.MOVE = False

	def run(self): self.RUN = True
	def unrun(self): self.RUN = False
	
	def set_angle(self, theta):
		ang = int(theta % 360)
		self.angle = ang

	def rotate(self, delta):
		self.set_angle(self.angle + delta)
		
	def shoot(self):
		Util.BULLET_MASK.add(Bullets.Bullet(self, Bullets.DMG_NORMAL))
		self.shoot_angle = self.angle
		self.SHOOT = True
