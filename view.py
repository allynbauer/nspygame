import pygame
from animation import *
from animation_queue import *

class View(object):

    animation_queue = None
    def __init__(self, frame):
        if frame is None:
            frame = pygame.Rect(0, 0, 0, 0)
        if type(frame) != pygame.Rect:
            raise Exception('type must be a pygame.Rect')
        self.invalid_rects = []
        self.superview = None
        self.subviews = []
        self.surface = None
        self.event_responders = []
        self.frame = None
        self.update_frame(frame)
        self.background_color = pygame.Color(0, 0, 0, 0)
        self.set_needs_display()

    def update_frame(self, frame):
        old_frame = self.frame
        self.frame = frame
        if self.superview is None:
            self.set_needs_display()
        elif old_frame is None:
            self.superview.set_needs_display(self.frame)
        else:
            draw_frame = pygame.Rect.union(old_frame, self.frame)
            self.superview.set_needs_display(draw_frame)

    # set this view as needing to draw. it will be drawn in the next game loop.
    # rect is a rect relative to this view that needs redrawn. subviews will automatically get marked
    # as needing to draw
    def set_needs_display(self, rect = None):
        if rect is None:
            rect = self.bounds()
        if self.superview is None:
            self.invalid_rects.append(rect)
        else:
            self.superview.set_needs_display(rect)

            # if we have a superview, we gotta tell the superview, cause the superview is gonna tell us what to draw, eventually.
            #for subview in self.subviews:
            #    if self.invalid_rect.colliderect(subview.frame):
            #        display_frame = self.invalid_rect.clip(subview.frame)
            #       subview.set_needs_display() # TODO:should really convert the display frame relative to the subview

    def bounds(self):
        return pygame.Rect((0, 0), self.frame.size)

    def add_subview(self, subview):
        self.subviews.append(subview)
        subview.superview = self
        subview.superview.set_needs_display(subview.frame)

    def bring_to_top(self):
        if not self.superview:
            return
        self.superview.subviews.append(self)
        self.superview.subviews.remove(self)

    def draw(self, rect):
        if self.surface is None:
            self.surface = pygame.Surface(self.frame.size)

        #self.surface.fill(self.background_color, rect)

        self.draw_subviews()

    def draw_subviews(self):
        for invalid_rect in self.invalid_rects:
            for subview in filter(lambda subview: invalid_rect.colliderect(subview.frame), self.subviews):
                subview.draw(subview.bounds())
                assert self.surface is not None, 'must have surface'
                assert subview.surface is not None, 'must have surface'
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
        return animation

    def convert_rect_from_view(self, rect, view):
        pass

    def convert_rect_to_view(self, rect, view):
        pass

