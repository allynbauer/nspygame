import view
from view import *

class StaticView(View):
	def __init__(self, rect):
		View.__init__(self, rect)

	def set_needs_display(self, rect = None):
		View.set_needs_display(self, rect)
		if self.surface:
			self.update_frame(pygame.Rect(self.surface.get_rect()))