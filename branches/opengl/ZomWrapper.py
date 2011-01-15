import pygame, sys, os, media, Zombie, Hero, Cursor
from pygame.locals import *

FPS = 24

pygame.init()
window = pygame.display.set_mode((media.WINDOW_WIDTH, media.WINDOW_HEIGHT), pygame.DOUBLEBUF)
pygame.mixer.init(11025)
media.prepare()

window.blit(media.BACKGROUND, (0,0))
pygame.display.flip()
pygame.display.set_caption('ZOMBIE')

cursor = Cursor.Cursor()
cgroup = pygame.sprite.RenderUpdates()
cgroup.add(cursor)

zombies = pygame.sprite.RenderUpdates()
heroes = pygame.sprite.RenderUpdates()


for i in xrange(0,1):
  heroes.add(Hero.Hero())

for i in xrange(0,6):
	zombies.add(Zombie.Zombie(heroes))

def update():
	cgroup.clear(window, media.BACKGROUND)
	zombies.clear(window, media.BACKGROUND)
	heroes.clear(window, media.BACKGROUND)
	
	cgroup.update()
	zombies.update()
	heroes.update()

	rectlist = zombies.draw(window) + heroes.draw(window) + cgroup.draw(window)
	pygame.display.update(rectlist)
	pygame.display.flip()

pygame.event.set_allowed([KEYDOWN, KEYUP, QUIT])
clock = pygame.time.Clock()
quit = False
while not quit:
	clock.tick(FPS)
	update()
	keyspressed = pygame.key.get_pressed()
            
	if keyspressed[K_a] and keyspressed[K_s]:
		for hero in heroes:
			hero.move(Hero.DOWNLEFT)
	elif keyspressed[K_s] and keyspressed[K_d]:
		for hero in heroes:
			hero.move(Hero.DOWNRIGHT)
	elif keyspressed[K_d] and keyspressed[K_w]:
		for hero in heroes:
			hero.move(Hero.UPRIGHT)
	elif keyspressed[K_w] and keyspressed[K_a]:
		for hero in heroes:
			hero.move(Hero.UPLEFT)
	elif keyspressed[K_a]:
		for hero in heroes:
			hero.move(Hero.LEFT)
	elif keyspressed[K_s]:
		for hero in heroes:
			hero.move(Hero.DOWN)
	elif keyspressed[K_d]:
		for hero in heroes:
			hero.move(Hero.RIGHT)
	elif keyspressed[K_w]:
		for hero in heroes:
			hero.move(Hero.UP)
	
	if keyspressed[K_ESCAPE]:
		quit = True
	
	events = pygame.event.get()
	pygame.event.pump()
	for event in events: 
		if event.type == QUIT: 
			quit = True
		elif event.type == KEYDOWN and event.key == K_LSHIFT:
			for hero in heroes:
				hero.run()
		elif event.type == KEYUP and event.key == K_LSHIFT:
			for hero in heroes:
				hero.unrun()
		elif event.type == KEYDOWN and event.key == K_SPACE:
			zombies.add(Zombie.Zombie(heroes))

pygame.quit()
sys.exit(0)
