import pygame, sys
import window, view, label
from pygame.locals import *
from label import *

class Game:
	def __init__(self, title = 'Untitled', size = (100, 100)):
		self.size = size
		self.title = title
		self.fps = 60
		self.time_elapsed = 0
		self.key_window = None

	# install the given window on the next run loop
	def install_window(self, window):
		self.key_window = window

	# manage the clock and fps
	def clock_tick(self):
		miliseconds = self.clock.tick(self.fps)
		self.time_previous = self.time_elapsed
		self.time_elapsed += miliseconds

	# top level event processing, cascades to windows as necessary
	def send_event(self, event):
		if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
			self.quit()
		elif (self.key_window != None):
			self.key_window.send_event(event)

	def quit(self):
		sys.exit(0)
		
	def init_pygame(self):
		pygame.init()
		pygame.display.set_mode(self.size)
		pygame.display.set_caption(self.title)
		self.clock = pygame.time.Clock()
		self.game_surface = pygame.display.get_surface()

	def run(self):
		if (self.key_window == None):
			raise Exception('Must call install_window to provide a key_window')
		self.init_pygame()
		while True:
			for event in pygame.event.get():
				self.send_event(event)
			self.key_window.blit(self.game_surface)
			pygame.display.flip()


def gen_label(text, origin, text_alignment):
	l = Label(pygame.Rect(origin, (250, 0)))
	l.text_alignment = text_alignment
	l.autofit_height()
	l.update_text(text)
	return l

if __name__ == '__main__':

	game = Game('Test Game', (250, 250))
	window = window.Window(pygame.Rect(0, 0, 250, 250))
	green = view.View(pygame.Rect(50, 50, 50, 50))
	green.background_color = pygame.Color(0, 255, 0, 0)
	window.add_subview(green)

	label = gen_label('Testing label left align', (0, 150), 'left')
	label.text_color = (255, 0, 0)
	window.add_subview(label)

	label = gen_label('Testing label center align', (0, 170), 'center')
	label.text_color = (0, 255, 0)
	window.add_subview(label)

	label = gen_label('Testing label right align', (0, 190), 'right')
	label.text_color = (0, 0, 255)
	window.add_subview(label)

	game.install_window(window)
	game.run()
