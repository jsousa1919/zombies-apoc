import pygame, os, media

class Cursor(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		self.image = media.CURS_SPRITE_MAIN
		self.rect = media.CURS_SPRITE_MAIN.get_rect()

	def update(self):
		self.rect.center = pygame.mouse.get_pos()
