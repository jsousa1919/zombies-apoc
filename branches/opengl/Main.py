import pygame, os, Util, Hero, Zombie, Swarm, math, Cursor
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

hero = None
zombies = []
swarm = None
curs = None
FPS = 30
ZOMBS = 10

def draw():
	glLoadIdentity()
	
	glCallList(Util.BG_DISPLIST)
	hero.draw()
	for zombie in zombies:
		zombie.draw()
		
	curs.draw()
	
	pygame.display.flip()

	
def handleKeys():
	keyspressed = pygame.key.get_pressed()
	
	if keyspressed[K_ESCAPE]:
		return 0	
	
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
		
	if keyspressed[K_LSHIFT]: hero.run()
	else: hero.unrun()
	
	if keyspressed[K_SPACE]: 
		global zombies
		zombies.append(Zombie.Zombie(hero, swarm))
	
	return 1
	
def initPlayers():
	global hero
	hero = Hero.Hero()

def initZombies(x):
	global zombies
	global swarm
	swarm = Swarm.Swarm((Util.WINDOW_WIDTH, Util.WINDOW_HEIGHT))
	for i in range(0, x):
		zombies.append(Zombie.Zombie(hero, swarm))
	
def update():
	global swarm
	curs.update()
	hero.update()
	for zombie in zombies:
		zombie.update()
	for zombie in zombies:
		zombie.try_swarm()
	swarm.clear()
	for zombie in zombies:
		zombie.prop_swarm()
	
def initEnvironment():
	global curs
	
	initPlayers()
	initZombies(ZOMBS)
	curs = Cursor.Cursor()

def main():
	Util.init()
	initEnvironment()

	frames = 0
	pygame.event.set_allowed([QUIT])
	clock = pygame.time.Clock()
	
	quit = False
	while not quit:
		clock.tick(FPS)
		
		update()
		draw()
		
		event = pygame.event.poll()
			
		if not handleKeys():
			quit = True
	
		if event.type == QUIT: 
			quit = True
		
		elif event.type == KEYDOWN and event.key == K_LSHIFT:
			hero.run()
		elif event.type == KEYUP and event.key == K_LSHIFT:
			hero.unrun()

	Util.cleanUp()
	
if __name__ == '__main__': main()
