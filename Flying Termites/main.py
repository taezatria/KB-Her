import pygame
from pygame.locals import *
from swarm import Swarm
from random import random

class Simulation:
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	YELLOW = (255, 255, 0)

	def __init__(self):
		self._running = True
		self._display_surf = None
		self.size = self.width, self.height = 500,500
		self.clock = pygame.time.Clock()

	def on_init(self):
		self.swarm = [Swarm() for i in range(20)]
		pygame.init()
		self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
		self._display_surf.fill(Simulation.WHITE)
		self._running = True

	def on_event(self,event):
		if event.type == pygame.QUIT:
			self._running = False
		elif event.type == KEYUP:
			if event.key == K_ESCAPE:
				self._running = False

		if event.type == pygame.MOUSEBUTTONUP:
			Swarm.global_best_position = pygame.mouse.get_pos()

	def on_loop(self):
		for swrm in self.swarm:
			closeSwrm = []
			for otherSwrm in self.swarm:
				if otherSwrm == swrm:
					continue
				distance = swrm.distance(otherSwrm)
				if distance < 150:
					closeSwrm.append(otherSwrm)

			swrm.moveCloser(closeSwrm)
			swrm.moveWith(closeSwrm)
			swrm.moveAway(closeSwrm, 15)

			border = 25
			if swrm.x < border and swrm.velocityX < 0:
				swrm.velocityX = -swrm.velocityX * random()
			if swrm.x > self.width - border and swrm.velocityX > 0:
				swrm.velocityX = -swrm.velocityX * random()
			if swrm.y < border and swrm.velocityY < 0:
				swrm.velocityY = -swrm.velocityY * random()
			if swrm.y > self.height - border and swrm.velocityY > 0:
				swrm.velocityY = -swrm.velocityY * random()

			swrm.move()

	def on_render(self):
		pygame.draw.circle(self._display_surf, Simulation.YELLOW,(int(Swarm.global_best_position[0]),int(Swarm.global_best_position[1])),20,0)
		for swrm in self.swarm:
			pygame.draw.circle(self._display_surf, Simulation.BLACK, (int(swrm.x),int(swrm.y)), 5, 0)
		pygame.display.update()

	def on_cleanup(self):
		pygame.quit()

	def on_execute(self):
		if self.on_init() == False:
			self._running = False

		while(self._running):
			for event in pygame.event.get():
				self.on_event(event)
			self.on_loop()
			self.on_render()
			self.clock.tick(50)
			self._display_surf.fill(Simulation.WHITE)
		self.on_cleanup()

if __name__ == '__main__':
	app = Simulation()
	app.on_execute()