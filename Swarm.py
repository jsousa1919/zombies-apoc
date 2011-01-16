import pygame, Util

class Swarm:
	def __init__(self, size):
		self.size = size
		self.mask = pygame.Mask(size)
		self.sightings = {}
		

	def add(self, loc, target):
		loc = (int(loc[0]), int(loc[1]))
		target = (int(target[0]), int(target[1]))
		#print "swarm add: ", loc, " to ", target
		if 0 <= loc[0] < self.size[0] and 0 <= loc[1] < self.size[1]: # for now, the mask is only as big as the window
			self.mask.set_at(loc, True)
			self.sightings[loc] = target

	def clear(self):
		self.mask.clear()
		self.sightings.clear()

	def swarm_movement(self, zom):
		loc = (zom.posx, zom.posy)
		theta = zom.angle
		sight = zom.sight

		fov = Util.ZOM_FOV[sight][theta / Util.ZOM_FOV_DEV]
		fov_rect = fov.get_rect(center=loc)
		fov_mask = pygame.mask.from_surface(fov)
		hit_mask = self.mask.overlap_mask(fov_mask, fov_rect.topleft)
		hit_num = hit_mask.count()
		hit_list = hit_mask.get_bounding_rects()
		x, y = (0, 0)
		for hit in hit_list:
			if hit.center in self.sightings:
				p = self.sightings[hit.center]
				x += p[0] / hit_num
				y += p[1] / hit_num
		return hit_num, (x,y)
