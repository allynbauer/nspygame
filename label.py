import pygame, view
from view import *
from pygame import *

class Label(View):
    def __init__(self, frame):
        View.__init__(self, frame)
        pygame.font.init()
        self.font_name = 'Helvetica'
        self.font = None
        self.size = 12
        self.update_text('Empty')
        self.text_color = (255, 255, 255)
        self.text_alignment = 'left' # or center or right

    def load_font(self):
        font = None
        path = pygame.font.match_font(self.font_name, False, False)
        if path is not None:
            font = pygame.font.Font(path, self.size)
        else:
            path = os.path.join('fonts', self.font_name)
            font = pygame.font.Font(path, self.size)
        
        return font

    def update_height(self, height):
        f = self.frame
        f.height = height
        self.update_frame(f)

    def get_text_size(self):
    	return self.get_font().size(self.text)

    def autofit_height(self):
        self.update_height(self.get_text_size()[1])
        self.set_needs_display()

    def update_text(self, text):
        self.text = text
        self.set_needs_display()

   	def set_needs_display(self, rect = None):
   		View.set_needs_display(self, rect)
   		self.font = None

    def get_font(self):
        if self.font is None:
            self.font = self.load_font()
        return self.font

    def draw(self, rect):
        View.draw(self, rect)
        self.text_surface = self.get_font().render(self.text, False, self.text_color, self.background_color)
        if self.text_alignment == 'left':
            text_origin = (0, 0)
        elif self.text_alignment == 'center':
            text_origin = ((self.frame.width - self.text_surface.get_width()) / 2.0, 0)
        elif self.text_alignment == 'right':
            text_origin = (self.frame.width - self.text_surface.get_width(), 0)
        else:
            raise Exception('text_alignment value \'{}\' invalid'.format(self.text_alignment))
        self.surface.blit(self.text_surface, text_origin)

