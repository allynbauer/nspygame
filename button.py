import pygame, view, label, event_responder, static_view
from view import *
from static_view import *
from event_responder import *
from pygame import *

class Button(View):
	def __init__(self, frame, args = { 'text': "Untitled", 'normal_surface': None, 'active_surface': None }):
		View.__init__(self, frame)
		self.text = None
		self.active = False

		self.active_view = StaticView(args.get('active_surface'))
		self.normal_view = StaticView(args.get('normal_surface'))
		self.label_view = None
		
		self.text_color = (255, 0, 0)
		self.active_text_color = (255, 255, 0)
		self.button_is_rounded_rect = self.normal_view.surface != None
		self.update_text(args.get('text'))
		
		self.add_event_responder(MouseButtonDownResponder('toggle'))
		self.add_event_responder(MouseButtonUpResponder('toggle'))

	def create_surfaces(self):
		if True and self.normal_view.surface == None:
			self.normal_view.surface = self.rounded_rect_surface()
			self.normal_view.background_color = pygame.Color(0,255,0,0)
			print "creating normal surface"


		if True and self.active_view.surface == None:
			self.active_view.surface = self.rounded_rect_surface((25,25,25))
			print "creating active surface"

	def toggle(self, event):
		self.active = not self.active
		self.create_surfaces()

		if self.active:
   			self.normal_view.remove_from_superview()
   			self.add_subview(self.active_view)
			if not self.button_is_rounded_rect:
				self.label_view.text_color = self.active_text_color
			print "active view added"
   		else:
   			self.active_view.remove_from_superview()
   			self.add_subview(self.normal_view)
			if not self.button_is_rounded_rect:
				self.label_view.text_color = self.text_color
			print "normal view added"

		self.set_needs_display()

   	def autosize(self):
		f = self.frame
		f.size = self.label_view.get_text_size()
		self.update_frame(f)

	def generate_label(self):
		l = label.Label(pygame.Rect((0, 0), (self.frame.width, 0)))
		l.size = 24
		l.text_alignment = 'center'
		l.autofit_height()
		l.update_text(self.text)
		l.text_color = self.text_color
		l.background_color = self.background_color
		self.add_subview(l)
		return l

	def update_text(self, text):
		self.text = text
		self.set_needs_display()
		l = self.generate_label()
		self.label_view = l

	def AAfilledRoundedRect(self, surface,rect,color,radius=0.4):

	    """
	    AAfilledRoundedRect(surface,rect,color,radius=0.4)

	    surface : destination
	    rect    : rectangle
	    color   : rgb or rgba
	    radius  : 0 <= radius <= 1
	    """

	    color = Color(*color)
	    alpha = color.a
	    color.a = 0
	    pos = rect.topleft
	    rect.topleft = 0,0
	    rectangle = Surface(rect.size, SRCALPHA)

	    circle = Surface([min(rect.size)*3]*2, SRCALPHA)
	    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
	    circle = transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

	    radius = rectangle.blit(circle,(0,0))
	    radius.bottomright = rect.bottomright
	    rectangle.blit(circle,radius)
	    radius.topright = rect.topright
	    rectangle.blit(circle,radius)
	    radius.bottomleft = rect.bottomleft
	    rectangle.blit(circle,radius)

	    rectangle.fill((0,0,0), rect.inflate(-radius.w,0))
	    rectangle.fill((0,0,0), rect.inflate(0,-radius.h))

	    rectangle.fill(color, special_flags=BLEND_RGBA_MAX)
	    rectangle.fill((255,255,255,alpha), special_flags=BLEND_RGBA_MIN)

	    return surface.blit(rectangle,pos)

	def rounded_rect_surface(self, color = (77,77,77)):
		s = Surface(self.frame.size)
		self.AAfilledRoundedRect(s, self.bounds(), color)
		return s

   	def draw(self, rect):		
		self.label_view.bring_to_top()
		print "{} {}".format(self.subviews, rect)
		View.draw(self, rect)


