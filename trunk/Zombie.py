import pygame, sys, os, random, timer, math, time
from pygame.locals import *

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000
MAXSPEED = 12

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        pygame.mixer.init(11025)
        self.screen = pygame.display.get_surface()

        self.master_image = pygame.image.load(os.path.join("data","zombie_0.png"))

        self.idle_sprites = self.__load_idle_sprites__()
        self.walk_sprites = self.__load_walk_sprites__()
        self.tick = 0
        self.direction = 0
        self.prevDirection = 0

        self.speaking = False
        self.MOVE = False
        
        self.rect = self.idle_sprites[0][0].get_rect()
        self.frame = 0

        self.area = self.screen.get_rect()
        self.speed = 4

        random.seed()
        x = random.random() * WINDOW_WIDTH
        y = random.random() * WINDOW_HEIGHT
        
        self.position = x, y
        self.rect.topleft = x, y

        self.update()

        
    def __load_idle_sprites__(self, w = 128, h = 128):
        '''
        ZOMBIE SPRITES HAVE A WIDTH, HEIGHT of 128
        '''
        images = []

        for i in xrange(0, 8):
            images.append([])
            for j in xrange(0, 4):
                images[i].append(self.master_image.subsurface((j*w, i*h, w, h)))

        return images

    def __load_walk_sprites__(self, w = 128, h = 128):
        '''
        ZOMBIE SPRITES HAVE A WIDTH, HEIGHT of 128
        '''
        images = []

        for i in xrange(0,8):
            images.append([])
            for j in xrange(4,12):
                images[i].append(self.master_image.subsurface((j*w, i*h, w, h)))

        return images

    def speak(self):
        if self.speaking:
            return
        id = random.randrange(1,24,1)
        file_path = os.path.join('sounds', 'zombie-%d.ogg' % id)
        sound = pygame.mixer.Sound(file_path)

        print ('Playing Sound...')
        self.speaking = True
        channel = sound.play()
        t = timer.ttimer(0.5, 1, self.endspeak, channel)
        t.Start()

    def endspeak(self, channel):
        if not channel.get_busy():
            self.speaking = False
            print ('...Finished')
        else:
            t = timer.ttimer(0.5, 1, self.endspeak, channel)
            t.Start()
    
    def update(self):
        self.tick += 1
        if self.tick % ((((MAXSPEED - self.speed)) / 4) + 1) == 0: 
            self.frame += 1
        if self.MOVE:
            if self.frame >= len(self.walk_sprites[self.direction]): self.frame = 0
            self.image = self.walk_sprites[self.direction][self.frame]
            sqrt_2 = math.sqrt(2)
            if self.direction == 0:
                self.rect.centerx -= self.speed
            elif self.direction == 1:
                self.rect.centerx -= self.speed/sqrt_2
                self.rect.centery -= self.speed/sqrt_2
            elif self.direction == 2:
                self.rect.centery -= self.speed
            elif self.direction == 3:
                self.rect.centery -= self.speed/sqrt_2
                self.rect.centerx += self.speed/sqrt_2
            elif self.direction == 4:
                self.rect.centerx += self.speed
            elif self.direction == 5:
                self.rect.centerx += self.speed/sqrt_2
                self.rect.centery += self.speed/sqrt_2
            elif self.direction == 6:
                self.rect.centery += self.speed
            elif self.direction == 7:
                self.rect.centery += self.speed/sqrt_2
                self.rect.centerx -= self.speed/sqrt_2
            if self.direction != self.prevDirection:
                if random.randrange(0,100,1) == 0: self.speak()
                self.prevDirection = self.direction
                
            self.MOVE = False
        else:
            self.image = self.idle_sprites[self.direction][self.frame % len(self.idle_sprites[self.direction])]


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

