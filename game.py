import pygame, sys
import window, view, label, button
from pygame.locals import *
from label import *
from event_responder import *
from animation_queue import *
from clock import *

class Game(object):
    def __init__(self, title = 'Untitled', size = (100, 100)):
        self.size = size
        self.title = title
        self.fps = 60
        self.time_elapsed = 0
        self.key_window = None
        self.main_queue = AnimationQueue()
        self.clock = Clock()

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
        elif self.key_window is not None:
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
        if self.key_window is None:
            raise Exception('Must call install_window to provide a key_window')
        self.init_pygame()
        while True:
            self.clock_tick()
            pygame.event.pump()
            for event in pygame.event.get():
                self.send_event(event)
            self.key_window.refresh()
            self.game_surface.blit(self.key_window.surface, self.key_window.frame)
            pygame.display.flip()
            self.main_queue.tick(self.clock)

def gen_label(text, origin, text_alignment):
    l = Label(pygame.Rect(origin, (250, 0)))
    l.text_alignment = text_alignment
    l.autofit_height()
    l.update_text(text)
    return l

left = False
can_change = True

def toggle():
    global left, can_change
    can_change = True
    left = not left

def animation():
    global left
    def animation_right():
        return lambda view: view.frame(250, 50, 75, 75)
    def animation_left():
        return lambda view: view.frame(50, 50, 50, 50)
    if left:
        return animation_left()
    else:
        return animation_right()

animate_colors = True
colors_side = True
def toggle_animate_colors_enabled():
    global animate_colors
    animate_colors = True

def color_animation():
    global colors_side
    def animation_right():
        return lambda view: view.background_color(100, 100, 100)
    def animation_left():
        return lambda view: view.background_color(0, 0, 0)
    if colors_side:
        return animation_left()
    else:
        return animation_right()

def animate_colors(event):
    global animate_colors, green
    if animate_colors:
        green.add_animation(game.main_queue, float(1.5), color_animation(), toggle_animate_colors_enabled)

def test(event):
    global game, can_change
    if can_change:
        green.add_animation(game.main_queue, float(1), animation(), toggle)
        can_change = not can_change


if __name__ == '__main__':

    game = Game('Test Game', (500, 500))
    window = window.Window(pygame.Rect(0, 0, 500, 500))
    window.add_event_responder(KeyDownResponder((K_a), None, 1, test))
    #window.add_event_responder(KeyDownResponder((K_c), None, 0, animate_colors))
    green = view.View(pygame.Rect(50, 50, 50, 50))
    green.background_color = pygame.Color(0, 255, 0, 0)
    window.add_subview(green)

    label = gen_label('Testing label left align', (0, 150), 'left')
    label.background_color = pygame.Color(0,255,255,0)
    label.text_color = pygame.Color(255, 0, 0, 1)
    window.add_subview(label)

    label = gen_label('Testing label center align', (0, 170), 'center')
    label.text_color = pygame.Color(0, 255, 0, 1)
    window.add_subview(label)

    label = gen_label('Testing label right align', (0, 190), 'right')
    label.text_color = pygame.Color(0, 0, 255, 1)
    window.add_subview(label)

    button = button.Button(pygame.Rect((0, 210), (100, 50)), {'text': 'Test Button'})
    button.background_color = pygame.Color(255,255,0,0)
    button.autosize()
    window.add_subview(button)

    game.install_window(window)
    game.run()
