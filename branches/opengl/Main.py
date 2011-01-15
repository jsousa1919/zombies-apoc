import pygame, os, Util, Hero, Zombie
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

hero = None
zombie = None
FPS = 30

def draw():
	glLoadIdentity()
	glCallList(Util.BG_DISPLIST)
	
	hero.draw()
	zombie.draw()
	
	pygame.display.flip()
	
def handleKeys():
	keyspressed = pygame.key.get_pressed()
	
	if keyspressed[K_ESCAPE]:
		return QUIT	
	
	if keyspressed[K_a] and keyspressed[K_s]:
		hero.move(Hero.DOWNLEFT)
	elif keyspressed[K_s] and keyspressed[K_d]:
		hero.move(Hero.DOWNRIGHT)
	elif keyspressed[K_d] and keyspressed[K_w]:
		hero.move(Hero.UPRIGHT)
	elif keyspressed[K_w] and keyspressed[K_a]:
		hero.move(Hero.UPLEFT)
	elif keyspressed[K_a]:
		hero.move(Hero.LEFT)
	elif keyspressed[K_s]:
		hero.move(Hero.DOWN)
	elif keyspressed[K_d]:
		hero.move(Hero.RIGHT)
	elif keyspressed[K_w]:
		hero.move(Hero.UP)
	else:
		hero.stop()
	
	return 0
	
def initPlayer():
	global hero
	global zombie
	hero = Hero.Hero()
	zombie = Zombie.Zombie(hero)
	
def update():
	hero.update()
	
def main():
	Util.init()
	initPlayer()

	frames = 0
	pygame.event.set_allowed([KEYDOWN, KEYUP, QUIT])
	clock = pygame.time.Clock()
	
	quit = False
	while not quit:
		clock.tick(FPS)
		
		update()
		draw()
		
		events = pygame.event.get()
		if events == [] and pygame.event.poll().type != NOEVENT:
			pygame.event.pump()
			
		if handleKeys() == QUIT:
			quit = True
		
		for event in events: 
			if event.type == QUIT: 
				quit = True
			elif event.type == KEYDOWN and event.key == K_LSHIFT:
				hero.run()
			elif event.type == KEYUP and event.key == K_LSHIFT:
				hero.unrun()
	
	Util.cleanUp()
	
if __name__ == '__main__': main()
