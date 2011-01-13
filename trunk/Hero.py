import pygame, sys, os, Zombie, random
from pygame.locals import *

WINDOW_HEIGHT = Zombie.WINDOW_HEIGHT
WINDOW_WIDTH = Zombie.WINDOW_WIDTH
RUNSPEED = 24
WALKSPEED = 15

class Hero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        
        self.master_image = pygame.image.load(os.path.join("data","ogre.png"))
        
        self.idle_sprites = self.__load_idle_sprites__()
        self.walk_sprites = self.__load_walk_sprites__()
        self.run_sprites = self.__load_run_sprites__()
                                              
        self.direction = 0
        self.MOVE = False
        self.RUN = False
        
        self.rect = self.idle_sprites[0][0].get_rect()
        self.frame = 0

        self.area = self.screen.get_rect()
        self.speed = WALKSPEED

        random.seed()
        x = random.random() * WINDOW_WIDTH
        y = random.random() * WINDOW_HEIGHT
        
        self.position = 50,50
        self.rect.topleft = 50,50

        self.update()
    
    def __load_idle_sprites__(self, w = 256, h = 256):
        '''
        THE HERO SPRITE HAS A WIDTH, HEIGHT of 256
        '''
        images = []

        for i in xrange(0, 8):
            images.append([])
            for j in xrange(0, 1):
                images[i].append(self.master_image.subsurface((j*w, i*h, w, h)))

        return images

    def __load_walk_sprites__(self, w = 256, h = 256):
        '''
        THE HERO SPRITE HAS A WIDTH, HEIGHT of 256
        '''
        images = []

        for i in xrange(0,8):
            images.append([])
            for j in xrange(0,4):
                images[i].append(self.master_image.subsurface((j*w, i*h, w, h)))

        return images

    def __load_run_sprites__(self, w = 256, h = 256):
        '''
        THE HERO SPRITE HAS A WIDTH, HEIGHT of 256
        '''
        images = []

        for i in xrange(0,8):
            images.append([])
            for j in xrange(4,6):
                images[i].append(self.master_image.subsurface((j*w, i*h, w, h)))

        return images


    def update(self):  
        self.frame += 1
        if self.MOVE:
            if self.frame >= len(self.walk_sprites[self.direction]): self.frame = 0
            self.image = self.walk_sprites[self.direction][self.frame]

            spd = WALKSPEED
                
            if self.RUN:
                spd = RUNSPEED
                if self.frame == 0:
                    file = 'fall.ogg'
                    file = os.path.join('sounds',file)

                    try:
                        randsound = pygame.mixer.Sound(file)
                    except:
                        #print "fuck you"
                        randound = None
                    if randsound:
                        randsound.play()

            if self.direction == 0:
                self.rect.left -= spd
            elif self.direction == 1:
                self.rect.left -= spd/2
                self.rect.top -= spd/2
            elif self.direction == 2:
                self.rect.top -= spd
            elif self.direction == 3:
                self.rect.top -= spd/2
                self.rect.right += spd/2
            elif self.direction == 4:
                self.rect.right += spd
            elif self.direction == 5:
                self.rect.bottom += spd/2
                self.rect.right += spd/2
            elif self.direction == 6:
                self.rect.bottom += spd
            elif self.direction == 7:
                self.rect.bottom += spd/2
                self.rect.left -= spd/2
                 
            self.MOVE = False
        else:
            if self.frame >= len(self.idle_sprites[self.direction]): self.frame = 0
            self.image = self.idle_sprites[self.direction][self.frame]

    def move_left(self):
        self.direction = 0
        self.MOVE = True
    def move_upleft(self):
        self.direction = 1
        self.MOVE = True
    def move_up(self):
        self.direction = 2
        self.MOVE = True
    def move_upright(self):
        self.direction = 3
        self.MOVE = True
    def move_right(self):
        self.direction = 4
        self.MOVE = True
    def move_downright(self):
        self.direction = 5
        self.MOVE = True
    def move_down(self):
        self.direction = 6
        self.MOVE = True
    def move_downleft(self):
        self.direction = 7
        self.MOVE = True
    def run(self): self.RUN = True
    def unrun(self): self.RUN = False
