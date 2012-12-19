from animation import *

class AnimationQueue(object):
	def __init__(self):
		self.animations = []

	def add_animation(self, animation):
		assert animation != None
		animation.queue = self
		animation.began = pygame.time.get_ticks() # TODO: replace with clock
		self.animations.append(animation)

	def tick(self, clock):
		for animation in self.animations:
			animation.tick(clock)
		finished_animations = filter(lambda animation: animation.animation_finished, self.animations)
		for animation in finished_animations:
			if callable(animation.finished_block):
				animation.finished_block()
			self.animations.remove(animation)

