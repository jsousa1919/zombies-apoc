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
		fov_mask = Util.ZOM_FOV_MASK[sight][theta / Util.ZOM_FOV_DEV]
		hit_mask = self.mask.overlap_mask(fov_mask, fov_rect.topleft)

		#hit_list = hit_mask.get_bounding_rects()
		hit_count = 0
		x, y = (0, 0)
		for hit in self.sightings.keys():
			if hit_mask.get_at(hit):
				p = self.sightings[hit]
				x += p[0]
				y += p[1]
				hit_count += 1
			if hit_count == 5:
				break
		if hit_count:
			x /= hit_count
			y /= hit_count
		return hit_count, (x,y)
