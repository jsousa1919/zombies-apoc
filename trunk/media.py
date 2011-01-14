import pygame, os

print "loading media"

#MAIN
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000

DATA_DIR = "data"
SPRITE_DIR = os.path.join(DATA_DIR, "sprites")
SOUND_DIR = os.path.join(DATA_DIR, "sounds")
TEXTURE_DIR = os.path.join(DATA_DIR, "textures")

#TERRAIN
BACKGROUND = None

#ZOMBIE
ZOM_SPRITE_WIDTH = 128
ZOM_SPRITE_HEIGHT = 128
ZOM_SPRITE_MAIN = None
ZOM_SPRITE_IDLE = None
ZOM_SPRITE_WALK = None
ZOM_FOV = [[], []]
ZOM_FOV_DEV = 4
ZOM_FOV_MIN = 200

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


def request_fov(x):
	if len(ZOM_FOV) > x > 0 and ZOM_FOV[x] != []:
		return
	while len(ZOM_FOV) <= x:
		ZOM_FOV.append([])
	
	for i in range(0, 360 / ZOM_FOV_DEV):
		ZOM_FOV[x].append(pygame.transform.scale(ZOM_FOV[1][i], (2 * ZOM_FOV_MIN * x, 2 * ZOM_FOV_MIN * x)))

def prepare():
	#TERRAIN
	global BACKGROUND
	BACKGROUND = pygame.image.load(os.path.join(TEXTURE_DIR,"flagstone2.jpg")).convert()
	bg = BACKGROUND
	bgw, bgh = BACKGROUND.get_rect().right, BACKGROUND.get_rect().bottom
	for i in xrange(1,int(WINDOW_WIDTH/bgw)):
		for j in xrange(1, int(WINDOW_WIDTH/bgh)):
			BACKGROUND.blit(bg, BACKGROUND.get_rect().topleft + (i*256, j*256))

	#ZOMBIE
	global ZOM_SPRITE_MAIN
	global ZOM_SPRITE_IDLE
	global ZOM_SPRITE_WALK
	global ZOM_FOV

	#ZOMBIE SPRITES
	ZOM_SPRITE_MAIN = pygame.image.load(os.path.join(SPRITE_DIR,"zombie_1.png")).convert_alpha()
	ZOM_SPRITE_IDLE = load_sprite_matrix(ZOM_SPRITE_MAIN, 0, 4, 0, 8, ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT)
	ZOM_SPRITE_WALK = load_sprite_matrix(ZOM_SPRITE_MAIN, 4, 12, 0, 8, ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT)

	#ZOMBIE FOV
	#TODO: when no longer necessary for debugging, don't store the images, only store the (preferably trimmed) masks and their dimensions
	ZOM_FOV[1].append(pygame.Surface((400,400)))
	pygame.draw.polygon(ZOM_FOV[1][0], pygame.Color('0xFF000040'), [(ZOM_FOV_MIN, ZOM_FOV_MIN), (2*ZOM_FOV_MIN, 0), (2*ZOM_FOV_MIN, 2*ZOM_FOV_MIN)])
	for i in range(1, 360 / ZOM_FOV_DEV):
		ZOM_FOV[1].append(pygame.transform.rotate(ZOM_FOV[1][0], ZOM_FOV_DEV*i))


	#HERO
	global HERO_SPRITE_MAIN
	global HERO_SPRITE_IDLE
	global HERO_SPRITE_WALK
	global HERO_SPRITE_RUN
	global HERO_MASK

	#HERO SPRITES
	HERO_SPRITE_MAIN = pygame.image.load(os.path.join(SPRITE_DIR,"male_unarmored.png")).convert_alpha()
	HERO_SPRITE_IDLE = load_sprite_matrix(HERO_SPRITE_MAIN, 0, 1, 0, 8, HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT)
	HERO_SPRITE_WALK = load_sprite_matrix(HERO_SPRITE_MAIN, 0, 4, 0, 8, HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT)
	HERO_SPRITE_RUN = load_sprite_matrix(HERO_SPRITE_MAIN, 4, 6, 0, 8, HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT)

	HERO_MASK = pygame.mask.from_surface(HERO_SPRITE_IDLE[0][0])

