import pygame, sys, os, Zombie, Hero
from pygame.locals import *

pygame.init()

WINDOW_HEIGHT = Zombie.WINDOW_HEIGHT
WINDOW_WIDTH = Zombie.WINDOW_WIDTH
FPS = 24

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background = pygame.image.load(os.path.join("data","flagstone2.jpg"))
window.blit(background, (0,0))
pygame.display.flip()
pygame.display.set_caption('ZOMBIE')

zombies = pygame.sprite.RenderUpdates()
heroes = pygame.sprite.RenderUpdates()

for i in xrange(0,5):
   zombies.add(Zombie.Zombie())

heroes.add(Hero.Hero())

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
            hero.move_downleft()
    elif keyspressed[K_s] and keyspressed[K_d]:
        for hero in heroes:
            hero.move_downright()
    elif keyspressed[K_d] and keyspressed[K_w]:
        for hero in heroes:
            hero.move_upright()
    elif keyspressed[K_w] and keyspressed[K_a]:
        for hero in heroes:
            hero.move_upleft()
    elif keyspressed[K_a]:
        for hero in heroes:
            hero.move_left()
    elif keyspressed[K_s]:
        for hero in heroes:
            hero.move_down()
    elif keyspressed[K_d]:
        for hero in heroes:
            hero.move_right()
    elif keyspressed[K_w]:
        for hero in heroes:
            hero.move_up()
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            quit = True
        elif event.type == KEYUP and (event.key == K_LSHIFT or event.key == K_RSHIFT):
            hero.unrun()
        elif event.type == KEYDOWN and (event.key == K_LSHIFT or event.key == K_RSHIFT):
            hero.run()
        #else:
            #print event

pygame.quit()
sys.exit(0)
