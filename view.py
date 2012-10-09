import pygame

class View:
	def __init__(self, frame):
		self.superview = None
		self.subviews = []
		self.update_frame(frame)
		self.background_color = pygame.Color(0, 0, 0, 0)
		self.set_needs_display()

	def update_frame(self, frame):
		self.frame = frame
		self.set_needs_display()

	def set_needs_display(self, rect = None):
		if (rect == None):
			self.invalid_rect = self.bounds()
		else:
			self.invalid_rect = rect

		for subview in self.subviews:
			subview.set_needs_display(self.bounds().clip(subview.frame))

	def bounds(self):
		return pygame.Rect((0, 0), self.frame.size)

	def add_subview(self, subview):
		self.subviews.append(subview)
		subview.superview = self

	def draw(self, rect):
		self.surface = pygame.Surface(self.frame.size)
		self.invalid_rect = None
		self.surface.fill(self.background_color)



