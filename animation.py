import pygame
from animation_queue import *
from pygame import *
import utilities
import colorsys

class Animation(object):	
	def __init__(self, duration, view, block, finished):
		self.duration = float(duration)
		self.view = view
		self.queue = None
		self.finished_block = finished
		self.animation_finished = False
		self.begain = None
		self.start_value = None
		self.end_value = None
		self.perform_animation = None
		block(self)

	def __getattr__(self, name):
		def _missing(*args, **kwargs):
			self.type = name
			if name == 'frame':
				assert len(args) == 4
				self.start_value = self.view.frame
				self.end_value = pygame.Rect(args)
				self.perform_animation = self.tick_frame
			elif name == 'bounds':
				pass
			elif name == 'background_color':
				self.start_value = colorsys.rgb_to_hsv(self.view.background_color.r, self.view.background_color.g, self.view.background_color.b)
				self.end_value = colorsys.rgb_to_hsv(*args)
				self.perform_animation = self.tick_background_color


			#print "A missing method was called."
			#print "The object was %r, the method was %r. " % (self, name)
			#print "It was called with %r and %r as arguments" % (args, kwargs)
		return _missing

	def mapped_value(self, value, min_range, max_range):
		return utilities.map_value(value, self.began, self.began + self.duration * 1000, min_range, max_range)

	def tick_frame(self, clock):
		now = pygame.time.get_ticks()
		# TODO: only do the right thing for whatever animation we're doing, don't assume frame
		x = self.mapped_value(now, self.start_value.x, self.end_value.x)
		y = self.mapped_value(now, self.start_value.y, self.end_value.y)
		w = self.mapped_value(now, self.start_value.width, self.end_value.width)
		h = self.mapped_value(now, self.start_value.height, self.end_value.height)

		self.view.update_frame(pygame.Rect(x, y, w, h))
		if now - self.began >= self.duration * 1000:
			self.animation_finished = True
			self.view.update_frame(self.end_value)


	def tick_background_color(self, clock):
		now = pygame.time.get_ticks()
		h = self.mapped_value(now, self.start_value[0], self.end_value[0])
		s = self.mapped_value(now, self.start_value[1], self.end_value[1])
		v = self.mapped_value(now, self.start_value[2], self.end_value[2])

		rgb = list(colorsys.hsv_to_rgb(h, s, v))
		rgba = [int(rgb[0]), int(rgb[1]), int(rgb[2]), 1]
		self.view.background_color = pygame.Color(*rgba)

	def tick(self, clock):
		if self.begain is None:
			self.begain = pygame.time.get_ticks()
			# TODO: use clock
		self.perform_animation(clock)
		
	# removes the animation from the queue, at once. the view is left where it is. you deal with it.
	def cancel(self):
		self.queue.remove(self)
