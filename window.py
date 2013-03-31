import pygame, view
from view import *
from pygame import *

class Window(View):
    def __init__(self, frame):
        View.__init__(self, frame)


    def should_process_responders(self, event, view):
        if hasattr(event, 'pos'):
            return view.frame.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN:
            return True
        elif event.type == pygame.KEYUP:
            return True
        return False

    def process_responders(self, event, view):
        if self.should_process_responders(event, view):
            responders = filter(lambda responder: responder.responds_to_event(event), view.event_responders)
            for responder in responders:
                if callable(responder.callback):
                    callback = responder.callback
                else:
                    callback = getattr(view, responder.callback)
                callback(event)

    def send_event(self, event):
        self.process_responders(event, self)
        for subview in self.subviews:
            self.process_responders(event, subview)


    def refresh(self):
        self.draw(self.bounds())
