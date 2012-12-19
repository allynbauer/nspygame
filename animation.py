import pygame
from animation_queue import *
from pygame import *
from utilities import *

class Animation(object):	
	def __init__(self, duration, view, block, finished):
		self.duration = float(duration)
		self.view = view
		self.queue = None
		self.finished_block = finished
		self.animation_finished = False
		self.begain = None
		self.start_frame = None
		self.end_frame = None
		block(self)

	def __getattr__(self, name):
		def _missing(*args, **kwargs):
			if name == 'frame':
				assert len(args) == 4
				self.start_frame = self.view.frame
				self.end_frame = pygame.Rect(args)
			elif name == 'bounds':
				None


			#print "A missing method was called."
			#print "The object was %r, the method was %r. " % (self, name)
			#print "It was called with %r and %r as arguments" % (args, kwargs)
		return _missing

	def tick(self, clock):
		if self.begain == None:
			self.begain = pygame.time.get_ticks()
			# TODO: use clock
		now = pygame.time.get_ticks()
		# TODO: only do the right thing for whatever animation we're doing, don't assume frame
		x = map_value(now, self.began, self.began + self.duration * 1000, self.start_frame.x, self.end_frame.x)
		y = map_value(now, self.began, self.began + self.duration * 1000, self.start_frame.y, self.end_frame.y)
		w = map_value(now, self.began, self.began + self.duration * 1000, self.start_frame.width, self.end_frame.width)
		h = map_value(now, self.began, self.began + self.duration * 1000, self.start_frame.height, self.end_frame.height)
		
		self.view.update_frame(pygame.Rect(x, y, w, h))
		if now - self.began >= self.duration * 1000:
			self.animation_finished = True
			self.view.update_frame(self.end_frame)


	# removes the animation from the queue, at once. the view is left where it is. you deal with it.
	def cancel(self):
		self.queue.remove(self)
