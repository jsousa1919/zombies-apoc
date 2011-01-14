import pygame, sys, os, Zombie, Hero
from pygame.locals import *

pygame.init()

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000
FPS = 24

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background = pygame.image.load(os.path.join("data","flagstone2.jpg"))
window.blit(background, (0,0))
pygame.display.flip()
pygame.display.set_caption('ZOMBIE')

zombies = pygame.sprite.RenderUpdates()
hero = Hero.Hero()
heroes = pygame.sprite.RenderUpdates()

for i in xrange(0,1):
	heroes.add(hero)

for i in xrange(0,5):
	zombies.add(Zombie.Zombie(heroes))

def update():
	zombies.update()
	heroes.update()
	rectlist = zombies.draw(window) + heroes.draw(window)
	pygame.display.update(rectlist)
	zombies.clear(window, background)
	heroes.clear(window, background)

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
	for event in pygame.event.get(): 
		if event.type == QUIT: 
			quit = True
		elif event.type == KEYDOWN and event.key == K_LSHIFT:
			for hero in heroes:
				hero.run()
		elif event.type == KEYUP and event.key == K_LSHIFT:
			for hero in heroes:
				hero.unrun()

pygame.quit()
sys.exit(0)
