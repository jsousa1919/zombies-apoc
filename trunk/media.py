import pygame, os

print "loading media"

#MAIN
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000

DATA_DIR = "data"
SPRITE_DIR = os.path.join(DATA_DIR, "sprites")
SOUND_DIR = os.path.join(DATA_DIR, "sounds")

#TERRAIN
BACKGROUND = None

#ZOMBIE
ZOM_SPRITE_WIDTH = 128
ZOM_SPRITE_HEIGHT = 128
ZOM_SPRITE_MAIN = None
ZOM_SPRITE_IDLE = None
ZOM_SPRITE_WALK = None
ZOM_FOV = None

#HERO
HERO_SPRITE_WIDTH = 256
HERO_SPRITE_HEIGHT = 256
HERO_SPRITE_MAIN = None
HERO_SPRITE_IDLE = None
HERO_SPRITE_WALK = None
HERO_SPRITE_RUN = None
HERO_MASK = None

def load_sprite_matrix(main, xmin, xmax, ymin, ymax, w, h):
	sprites = []
	for i in xrange(ymin, ymax):
		sprites.append([])
		for j in xrange(xmin, xmax):
			sprites[i].append(main.subsurface((j*w, i*h, w, h)))
	return sprites


def prepare():
	#TERRAIN
	global BACKGROUND
	BACKGROUND = pygame.image.load(os.path.join(SPRITE_DIR,"flagstone2.jpg")).convert()

	#ZOMBIE
	global ZOM_SPRITE_MAIN
	global ZOM_SPRITE_IDLE
	global ZOM_SPRITE_WALK
	global ZOM_FOV
	ZOM_SPRITE_MAIN = pygame.image.load(os.path.join(SPRITE_DIR,"zombie_1.png")).convert_alpha()
	ZOM_SPRITE_WIDTH = 128
	ZOM_SPRITE_HEIGHT = 128

	ZOM_SPRITE_IDLE = load_sprite_matrix(ZOM_SPRITE_MAIN, 0, 4, 0, 8, ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT)
	ZOM_SPRITE_WALK = load_sprite_matrix(ZOM_SPRITE_MAIN, 4, 12, 0, 8, ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT)

	ZOM_FOV = pygame.Surface((400,400))
	pygame.draw.polygon(ZOM_FOV, pygame.Color('0xFF000040'), [(200, 200), (400, 100), (400, 300)])


	#HERO
	global HERO_SPRITE_MAIN
	global HERO_SPRITE_IDLE
	global HERO_SPRITE_WALK
	global HERO_SPRITE_RUN
	global HERO_MASK

	HERO_SPRITE_MAIN = pygame.image.load(os.path.join(SPRITE_DIR,"male_unarmored.png")).convert_alpha()
	HERO_SPRITE_WIDTH = 256
	HERO_SPRITE_HEIGHT = 256
	HERO_SPRITE_IDLE = load_sprite_matrix(HERO_SPRITE_MAIN, 0, 1, 0, 8, HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT)
	HERO_SPRITE_WALK = load_sprite_matrix(HERO_SPRITE_MAIN, 0, 4, 0, 8, HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT)
	HERO_SPRITE_RUN = load_sprite_matrix(HERO_SPRITE_MAIN, 4, 6, 0, 8, HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT)

	HERO_MASK = pygame.mask.from_surface(HERO_SPRITE_IDLE[0][0])

