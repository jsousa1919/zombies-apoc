import pygame, os
from OpenGL.GL import *
from OpenGL.GLU import *

#MAIN
WINDOW_HEIGHT = 256 * 3
WINDOW_WIDTH = 256 * 4
SCREEN = None

DATA_DIR = "data"
SPRITE_DIR = os.path.join(DATA_DIR, "sprites")
SOUND_DIR = os.path.join(DATA_DIR, "sounds")
TEXTURE_DIR = os.path.join(DATA_DIR, "textures")

#TERRAIN
BACKGROUND = None
BG_DISPLIST = None

#ZOMBIE
ZOM_SPRITE_WIDTH = 128
ZOM_SPRITE_HEIGHT = 128
ZOM_SPRITE_MAIN = None
ZOM_SPRITE_IDLE = None
ZOM_SPRITE_WALK = None
ZOM_IDLE_DISPLIST = None
ZOM_WALK_DISPLIST = None

ZOM_FOV = [[], []]
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

def load_sprite_matrix(main, xmin, xmax, ymin, ymax, w, h):
	sprites = []
	for i in xrange(ymin, ymax+1):
		sprites.append([])
		for j in xrange(xmin, xmax+1):
			sprites[i].append(toTexture(main.subsurface(j*w, i*h, w, h), w, h))
	return sprites

def request_fov(x):
	if len(ZOM_FOV) > x > 0 and ZOM_FOV[x] != []:
		return
	while len(ZOM_FOV) <= x:
		ZOM_FOV.append([])
	
	for i in range(0, 360 / ZOM_FOV_DEV):
		ZOM_FOV[x].append(pygame.transform.scale(ZOM_FOV[1][i], (2 * ZOM_FOV_MIN * x, 2 * ZOM_FOV_MIN * x)))

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
	for i in xrange(0, len(dlist)):
		for j in xrange(0, len(dlist[0])):
			glDeleteLists(dlist[i][j],1)

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
	
	delDList(HERO_IDLE_DISPLIST)
	delDList(HERO_WALK_DISPLIST)
	delDList(ZOM_IDLE_DISPLIST)
	delDList(ZOM_WALK_DISPLIST)
	
def initDispLists():
	global ZOM_IDLE_DISPLIST
	global ZOM_WALK_DISPLIST
	global HERO_IDLE_DISPLIST
	global HERO_WALK_DISPLIST
	
	ZOM_IDLE_DISPLIST = []
	for i in xrange(0, len(ZOM_SPRITE_IDLE)):
		ZOM_IDLE_DISPLIST.append([])
		for j in xrange(0,len(ZOM_SPRITE_IDLE[0])):
			ZOM_IDLE_DISPLIST[i].append(createTexDList(ZOM_SPRITE_IDLE[i][j], ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT))
	
	ZOM_WALK_DISPLIST = []
	for i in xrange(0, len(ZOM_SPRITE_WALK)):
		ZOM_WALK_DISPLIST.append([])
		for j in xrange(0,len(ZOM_SPRITE_WALK[0])):
			ZOM_WALK_DISPLIST[i].append(createTexDList(ZOM_SPRITE_WALK[i][j], ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT))
			
	HERO_IDLE_DISPLIST = []
	for i in xrange(0, len(HERO_SPRITE_IDLE)):
		HERO_IDLE_DISPLIST.append([])
		for j in xrange(0,len(HERO_SPRITE_IDLE[0])):
			HERO_IDLE_DISPLIST[i].append(createTexDList(HERO_SPRITE_IDLE[i][j], HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT))
			
	HERO_WALK_DISPLIST = []
	for i in xrange(0, len(HERO_SPRITE_WALK)):
		HERO_WALK_DISPLIST.append([])
		for j in xrange(0,len(HERO_SPRITE_WALK[0])):
			HERO_WALK_DISPLIST[i].append(createTexDList(HERO_SPRITE_WALK[i][j], HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT))
	
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
	global ZOM_FOV

	#ZOMBIE SPRITES
	ZOM_SPRITE_MAIN = pygame.image.load(os.path.join(SPRITE_DIR,"zombie_1.png")).convert_alpha()
	ZOM_SPRITE_IDLE = load_sprite_matrix(ZOM_SPRITE_MAIN, 0, 3, 0, 7, ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT)
	ZOM_SPRITE_WALK = load_sprite_matrix(ZOM_SPRITE_MAIN, 4, 11, 0, 7, ZOM_SPRITE_WIDTH, ZOM_SPRITE_HEIGHT)

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
	global HERO_MASK

	#HERO SPRITES
	HERO_SPRITE_MAIN = pygame.image.load(os.path.join(SPRITE_DIR,"male_unarmored.png")).convert_alpha()
	HERO_SPRITE_IDLE = load_sprite_matrix(HERO_SPRITE_MAIN, 0, 0, 0, 7, HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT)
	HERO_SPRITE_WALK = load_sprite_matrix(HERO_SPRITE_MAIN, 0, 3, 0, 7, HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT)
	
	HERO_MASK = pygame.mask.from_surface(HERO_SPRITE_MAIN.subsurface(0, 0, HERO_SPRITE_WIDTH, HERO_SPRITE_HEIGHT))

	
	#MISC
	global CURS_SPRITE_MAIN

	pygame.mouse.set_visible(False)

	CURS_SPRITE_MAIN = pygame.image.load(os.path.join(SPRITE_DIR,"crosshairs/crosshair6.png")).convert_alpha()
	
	#Create OpenGL display lists for textures
	initDispLists()

def initDisplay():
	global WINDOW_HEIGHT
	global WINDOW_WIDTH
	global SCREEN
	
	flags = pygame.OPENGL | pygame.DOUBLEBUF
	SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), flags)
	
	glClearColor(0.0,0.0,0.0,1.0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(0,WINDOW_WIDTH,0,WINDOW_HEIGHT) #2D Orthographic: Origin (0,0) at bottomleft
	glMatrixMode(GL_MODELVIEW)
	
	#Enable & setup texturing
	glEnable(GL_TEXTURE_2D)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	
def init():
	pygame.init()
	
	#random.seed()
	
	initDisplay()
	loadTextures()
