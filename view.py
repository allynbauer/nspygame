import pygame
from animation import *
from animation_queue import *

class View(object):

	def __init__(self, frame):
		if frame == None:
			frame = pygame.Rect(0, 0, 0, 0)
		if type(frame) != pygame.Rect:
			raise Exception('type must be a pygame.Rect')
		self.superview = None
		self.subviews = []
		self.event_responders = []
		self.frame = None
		self.update_frame(frame)
		self.background_color = pygame.Color(0, 0, 0, 0)
		self.set_needs_display()
		self.animation_queue = None

	def update_frame(self, frame):
		old_frame = self.frame
		self.frame = frame
		self.surface = None
		if self.superview == None:
			self.set_needs_display()
		elif old_frame == None:
			self.superview.set_needs_display(self.frame)
		else:
			draw_frame = pygame.Rect.union(old_frame, self.frame)
			print draw_frame
			self.superview.set_needs_display(draw_frame)

	def set_needs_display(self, rect = None):
		if (rect == None):
			self.invalid_rect = self.bounds()
		else:
			self.invalid_rect = rect
		for subview in self.subviews:
			if self.invalid_rect.colliderect(subview.frame):
				display_frame = self.invalid_rect.clip(subview.frame)
				subview.set_needs_display(display_frame)

	def bounds(self):
		return pygame.Rect((0, 0), self.frame.size)

	def add_subview(self, subview):
		self.subviews.append(subview)
		subview.superview = self
		self.set_needs_display(subview.frame)

	def bring_to_top(self):
		if not self.superview:
			return
		self.superview.subviews.append(self)
		self.superview.subviews.remove(self)

	def draw(self, rect):
		if self.invalid_rect == None:
			return
		elif self.surface == None:
			self.surface = pygame.Surface(self.frame.size)
		if rect == self.frame:
			self.surface.fill(self.background_color)
		elif rect != None:
			print "end"

		self.draw_subviews()
		self.invalid_rect = None


	def draw_subviews(self):
		for subview in filter(lambda subview: subview.invalid_rect != None, self.subviews):
			print subview.invalid_rect
			self.surface.fill(self.background_color, self.invalid_rect)
			subview.draw(subview.invalid_rect)
				
			self.surface.blit(subview.surface, subview.frame)

	def remove_from_superview(self):
		if self.superview:
			self.superview.subviews.remove(self)
			self.superview.set_needs_display(self.frame)

	def add_event_responder(self, responder):
		self.event_responders.append(responder)

	# duration is in seconds
	# animation is a lambda view: view.frame()
	# returns an instance of Animation
	# 
  	def add_animation(self, queue, duration, block, finished):
  		animation = Animation(duration, self, block, finished)
  		queue.add_animation(animation)



