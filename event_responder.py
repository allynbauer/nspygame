import pygame

class EventResponder(object):
	def __init__(self, callback):
		self.callback = callback
		assert callable(callback) "callback must be callable"
		self.type = None

	def responds_to_event(self, event):
		return event.type == self.type

# calls callback with the event when the mouse moves
class MouseMotionResponder(EventResponder):
	def __init__(self, callback):
		EventResponder.__init__(self, callback)
		self.type = pygame.MOUSEMOTION

# calls callback with the event when button is clicked
class MouseButtonDownResponder(EventResponder):
	def __init__(self, callback):
		EventResponder.__init__(self, callback)
		self.type = pygame.MOUSEBUTTONDOWN
		self.button = 1

	def responds_to_event(self, event):
		return EventResponder.responds_to_event(self, event) and self.button == event.button

# calls callback with the event when button is released
class MouseButtonUpResponder(EventResponder):
	def __init__(self, callback):
		EventResponder.__init__(self, callback)
		self.type = pygame.MOUSEBUTTONUP
		self.button = 1

	def responds_to_event(self, event):
		return EventResponder.responds_to_event(self, event) and self.button == event.button

class KeyEventResponder(EventResponder):
	def __init__(self, keys, mods, repeats_every, callback):
		EventResponder.__init__(self, callback)
		self.keys = keys
		self.mods = mods
		self.repeats_every = max(float(0), float(repeats_every))
		self.callback = callback

	def responds_to_event(self, event):
		return EventResponder.responds_to_event(self, event) and self.keys == event.key

# actives when all keys are active on view. currently that view must be the window, because its hard
# repeats_every is when the event repeats. positive value in seconds, zero means doesn't repeat until key up.
# keys is a list of keys. but for now it will only support one
# mods is a list of mods #http://www.pygame.org/docs/ref/key.html
class KeyDownResponder(KeyEventResponder):
	def __init__(self, keys, mods, repeats_every, callback):
		KeyEventResponder.__init__(self, keys, mods, repeats_every, callback)
		self.type = pygame.KEYDOWN

	def responds_to_event(self, event):
		return KeyEventResponder.responds_to_event(self, event) and self.keys == event.key


class KeyUpResponder(KeyEventResponder):
	def __init__(self, keys, mods, repeats_every, callback):
		KeyEventResponder.__init__(self, keys, mods, repeats_every, callback)
		self.type = pygame.KEYUP

	def responds_to_event(self, event):
		return KeyEventResponder.responds_to_event(self, event) and self.keys == event.key