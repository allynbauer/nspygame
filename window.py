import pygame, view
from view import *
from pygame import *

class Window(View):
	def __init__(self, frame):
		View.__init__(self, frame)

	def send_event(self, event):
		if (event.type == MOUSEBUTTONDOWN):
			self.set_needs_display(pygame.Rect(event.pos, (1, 1)))

	def blit(self, surface):
		if (self.invalid_rect != None):
			self.draw(self.invalid_rect)
			for subview in self.subviews:
				if (subview.invalid_rect != None):
					subview.draw(subview.invalid_rect)
					self.surface.blit(subview.surface, subview.frame)
			surface.blit(self.surface, self.frame)