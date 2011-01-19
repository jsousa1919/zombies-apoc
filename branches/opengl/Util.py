import pygame, os, Bullets
from OpenGL.GL import *
from OpenGL.GLU import *

#MAIN
WINDOW_HEIGHT = 256 * 4
WINDOW_WIDTH = 256 * 6
SCREEN = None

DATA_DIR = "data"
SPRITE_DIR = os.path.join(DATA_DIR, "sprites")
SOUND_DIR = os.path.join(DATA_DIR, "sounds")
TEXTURE_DIR = os.path.join(DATA_DIR, "textures")

FPS = 30

#TERRAIN
BACKGROUND = None
BG_DISPLIST = None

#ZOMBIE
ZOM_SPRITE_WIDTH = 128
ZOM_SPRITE_HEIGHT = 128
ZOM_SPRITE_MAIN = None
ZOM_SPRITE_IDLE = None
ZOM_SPRITE_WALK = None
ZOM_SPRITE_DAMG = None
ZOM_SPRITE_DEAD = None
ZOM_SPRITE_ATTK = None
ZOM_IDLE_DISPLIST = None
ZOM_WALK_DISPLIST = None
ZOM_DAMG_DISPLIST = None
ZOM_DEAD_DISPLIST = None
ZOM_ATTK_DISPLIST = None

ZOM_FOV = [[], []]
ZOM_FOV_MASK = [[], []]
ZOM_FOV_DEV = 4
ZOM_FOV_MIN = 200

#HERO
HERO_SPRITE_WIDTH = 256
HERO_SPRITE_HEIGHT = 256
HERO_SPRITE_MAIN = None
HERO_SPRITE_IDLE = None
HERO_SPRITE_WALK = None
HERO_IDLE_DISPLIST = None
HERO_WALK_DISPLIST = None
HERO_MASK = None

#CURSOR
CURS_SPRITE_WIDTH = 64
CURS_SPRITE_HEIGHT = 64
CURS_SPRITE_MAIN = None
CURS_DISPLIST = None

#TESTING STUFF / VARIABLES TO EVENTUALLY MOVE
SUPERSWARM = True

#BULLETS
BULLET_DISPLIST = None
BULLET_SIZE = 15
BULLET_MASK = Bullets.BulletMask()

def load_sprite_matrix(main, xmin, xmax, ymin, ymax, w, h):
	sprites = []
	for i in xrange(ymin, ymax):
		for j in xrange(xmin, xmax):
			sprites.append(toTexture(main.subsurface(j*w, i*h, w, h), w, h))
	return sprites

def request_fov(x):
	global ZOM_FOV
	global ZOM_FOV_MASK
	if len(ZOM_FOV) > x > 0 and ZOM_FOV[x] != []:
		return
	while len(ZOM_FOV) <= x:
		ZOM_FOV.append([])
		ZOM_FOV_MASK.append([])
	
	for i in range(0, 360 / ZOM_FOV_DEV):
		scaled = pygame.transform.scale(ZOM_FOV[1][i], (2 * ZOM_FOV_MIN * x, 2 * ZOM_FOV_MIN * x))
		scaled.set_colorkey(pygame.Color('black'))
		ZOM_FOV[x].append(scaled)
		ZOM_FOV_MASK[x].append(pygame.mask.from_surface(scaled))

def createTexDList(texture, w, h):
	dlist = glGenLists(1)
	glNewList(dlist, GL_COMPILE)
	
	glBindTexture(GL_TEXTURE_2D, texture)
	
	glBegin(GL_QUADS)
	glTexCoord2f(0,0)
	glVertex2f(0,0)
	glTexCoord2f(0,1)
	glVertex2f(0,h)
	glTexCoord2f(1,1)
	glVertex2f(w,h)
	glTexCoord2f(1,0)
	glVertex2f(w,0)
	glEnd()
	
	glEndList()
	
	return dlist
	
def delDList(dlist):
	for j in xrange(0, len(dlist)):
		glDeleteLists(dlist[j],1)

def toTexture(surface, w, h):
	#w, h MUST BE powers of 2 to work with OpenGL (e.g. 16x16, 256x512)
	
	surfData = pygame.image.tostring(surface, "RGBA", True)
	
	texture = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, texture)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, surfData)
	
	return texture
	
def delTexture(texture):
	glDeleteTextures(texture)
	
def cleanUp():
	delTexture(BACKGROUND)
	delTexture(ZOM_SPRITE_IDLE)
	delTexture(ZOM_SPRITE_WALK)
	delTexture(HERO_SPRITE_IDLE)
	delTexture(HERO_SPRITE_WALK)
	delTexture(ZOM_SPRITE_DAMG)
	delTexture(ZOM_SPRITE_DEAD)
	delTexture(ZOM_SPRITE_ATTK)
	
	delDList(HERO_IDLE_DISPLIST)
	delDList(HERO_WALK_DISPLIST)
	delDList(ZOM_IDLE_DISPLIST)
	delDList(ZOM_WALK_DISPLIST)
	delDList(ZOM_DAMG_DISPLIST)
	delDList(ZOM_DEAD_DISPLIST)
	delDList(ZOM_ATTK_DISPLIST)
	
	delDList(CURS_DISPLIST)
	
	delDList(BULLET_DISPLIST)
	
def initDispLists():
	global ZOM_IDLE_DISPLIST
	global ZOM_WALK_DISPLIST
	global ZOM_DAMG_DISPLIST
	global ZOM_DEAD_DISPLIST
	global ZOM_ATTK_DISPLIST
	global HERO_IDLE_DISPLIST
	global HERO_WALK_DISPLIST
	global CURS_DISPLIST
	global BULLET_DISPLIST
	
	ZOM_IDLE_DISPLIST = []
	for i in xrange(0, len(ZOM_SPRITE_IDLE)):
		ZOM_IDLE_DISPLIST.append(createTexDList(ZOM_SPRITE_IDLE[i], ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT))
	
	ZOM_WALK_DISPLIST = []
	for i in xrange(0, len(ZOM_SPRITE_WALK)):
		ZOM_WALK_DISPLIST.append(createTexDList(ZOM_SPRITE_WALK[i], ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT))
	
	ZOM_DAMG_DISPLIST = []
	for i in xrange(0, len(ZOM_SPRITE_DAMG)):
		ZOM_DAMG_DISPLIST.append(createTexDList(ZOM_SPRITE_DAMG[i], ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT))
	
	ZOM_DEAD_DISPLIST = []
	for i in xrange(0, len(ZOM_SPRITE_DEAD)):
		ZOM_DEAD_DISPLIST.append(createTexDList(ZOM_SPRITE_DEAD[i], ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT))
	
	ZOM_ATTK_DISPLIST = []
	for i in xrange(0, len(ZOM_SPRITE_ATTK)):
		ZOM_ATTK_DISPLIST.append(createTexDList(ZOM_SPRITE_ATTK[i], ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT))
			
	HERO_IDLE_DISPLIST = []
	for i in xrange(0, len(HERO_SPRITE_IDLE)):
		HERO_IDLE_DISPLIST.append(createTexDList(HERO_SPRITE_IDLE[i], HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT))
			
	HERO_WALK_DISPLIST = []
	for i in xrange(0, len(HERO_SPRITE_WALK)):
		HERO_WALK_DISPLIST.append(createTexDList(HERO_SPRITE_WALK[i], HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT))
			
	CURS_DISPLIST = []
	CURS_DISPLIST.append(createTexDList(CURS_SPRITE_MAIN, CURS_SPRITE_WIDTH, CURS_SPRITE_HEIGHT))
	
	BULLET_DISPLIST = []
	
	dlist = glGenLists(1)
	glNewList(dlist, GL_COMPILE)
	
	glBegin(GL_POINTS)
	glColor3f(0.0,1.0,1.0)
	glVertex2f(0.0,0.0)
	glColor3f(1.0,1.0,1.0)
	glEnd()
	
	glEndList()
	
	BULLET_DISPLIST.append(dlist)
	
def loadTextures():
	#TERRAIN
	global BACKGROUND
	global BG_DISPLIST
	temp = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
	img = pygame.image.load(os.path.join(TEXTURE_DIR,"roads/roadPLAZA.tga")).convert()
	
	bgw, bgh = img.get_width(), img.get_height()

	for i in xrange(0,int(WINDOW_WIDTH/bgw)):
		for j in xrange(0, int(WINDOW_WIDTH/bgh)):
			temp.blit(img,(i*bgw, j*bgh))
			
	BACKGROUND = toTexture(temp, WINDOW_WIDTH, WINDOW_HEIGHT)
	BG_DISPLIST = createTexDList(BACKGROUND, WINDOW_WIDTH, WINDOW_HEIGHT)

	#ZOMBIE
	global ZOM_SPRITE_MAIN
	global ZOM_SPRITE_IDLE
	global ZOM_SPRITE_WALK
	global ZOM_SPRITE_DAMG
	global ZOM_SPRITE_ATTK
	global ZOM_SPRITE_DEAD
	global ZOM_FOV

	#ZOMBIE SPRITES
	ZOM_SPRITE_MAIN = pygame.image.load(os.path.join(SPRITE_DIR,"zombie_1.png")).convert_alpha()
	ZOM_SPRITE_IDLE = load_sprite_matrix(ZOM_SPRITE_MAIN, 0, 4, 5, 6, ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT)
	ZOM_SPRITE_WALK = load_sprite_matrix(ZOM_SPRITE_MAIN, 4, 12, 5, 6, ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT)
	ZOM_SPRITE_DAMG = load_sprite_matrix(ZOM_SPRITE_MAIN, 16, 20, 5, 6, ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT)
	ZOM_SPRITE_DEAD = load_sprite_matrix(ZOM_SPRITE_MAIN, 28, 36, 5, 6, ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT)
	ZOM_SPRITE_ATTK = load_sprite_matrix(ZOM_SPRITE_MAIN, 12, 16, 5, 6, ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT)

	#ZOMBIE FOV
	#TODO: when no longer necessary for debugging, don't store the images, only store the (preferably trimmed) masks and their dimensions
	ZOM_FOV[1].append(pygame.Surface((400,400)))
	pygame.draw.polygon(ZOM_FOV[1][0], pygame.Color('0xFF000040'), [(int(ZOM_FOV_MIN * 7/8), ZOM_FOV_MIN), (2*ZOM_FOV_MIN, 0), (2*ZOM_FOV_MIN, 2*ZOM_FOV_MIN)])
	ZOM_FOV_MASK[1].append(pygame.mask.from_surface(ZOM_FOV[1][0]))
	for i in range(1, 360 / ZOM_FOV_DEV):
		rotated = pygame.transform.rotate(ZOM_FOV[1][0], ZOM_FOV_DEV*(-i))
		rotated.set_colorkey(pygame.Color('black'))
		ZOM_FOV[1].append(rotated)
		ZOM_FOV_MASK[1].append(pygame.mask.from_surface(rotated))


	#HERO
	global HERO_SPRITE_MAIN
	global HERO_SPRITE_IDLE
	global HERO_SPRITE_WALK
	global HERO_MASK

	#HERO SPRITES
	HERO_SPRITE_MAIN = pygame.transform.rotate(pygame.image.load(os.path.join(SPRITE_DIR,"A_big_13.png")).convert_alpha(), 90)
	HERO_SPRITE_IDLE = load_sprite_matrix(HERO_SPRITE_MAIN, 0, 1, 0, 1, HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT) #0,0,0,7
	HERO_SPRITE_WALK = load_sprite_matrix(HERO_SPRITE_MAIN, 0, 1, 0, 1, HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT) #0,3,0,7
	
	HERO_MASK = pygame.mask.from_surface(HERO_SPRITE_MAIN.subsurface(0, 0, HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT))
	
	#MISC
	global CURS_SPRITE_MAIN
	CURS_SPRITE_MAIN = toTexture(pygame.image.load(os.path.join(SPRITE_DIR,"crosshairs/crosshair6.png")).convert_alpha(), CURS_SPRITE_WIDTH, CURS_SPRITE_HEIGHT)
	
	#Create OpenGL display lists for textures
	initDispLists()

def initDisplay():
	global WINDOW_HEIGHT
	global WINDOW_WIDTH
	global SCREEN
	
	flags = pygame.OPENGL | pygame.DOUBLEBUF
	SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), flags)
	
	glDisable(GL_DEPTH_TEST)
	
	glClearColor(0.0,0.0,0.0,1.0)
	glClear(GL_COLOR_BUFFER_BIT)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1) #2D Orthographic: Origin (0,0) at bottomleft
	glMatrixMode(GL_MODELVIEW)
	
	#Enable & setup texturing
	glEnable(GL_TEXTURE_2D)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	
	glPointSize(BULLET_SIZE)
	glLineWidth(BULLET_SIZE)
	
def init():
	pygame.init()
	pygame.mouse.set_visible(False)
	
	initDisplay()
	loadTextures()
