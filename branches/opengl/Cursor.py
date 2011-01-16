import pygame, Util
from OpenGL.GL import *

class Cursor:
	def __init__(self):
		self.posx, self.posy = 11,0
		self.frame = 0
		
		self.update()
		
	def getDisplayList(self):
		return Util.CURS_DISPLIST[self.frame]

	def draw(self):
		glLoadIdentity()
		glTranslatef(self.posx - (Util.CURS_SPRITE_WIDTH / 2), self.posy - (Util.CURS_SPRITE_HEIGHT / 2), 0)
		glCallList(self.getDisplayList())
	
	def update(self):
		mpos = pygame.mouse.get_pos()
		self.posx, self.posy = mpos[0], Util.WINDOW_HEIGHT - mpos[1]
