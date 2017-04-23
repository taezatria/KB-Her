from random import randint,random
import numpy as np
import math

class Swarm:
	max_velocity = 10
	def __init__(self):
		self.x = randint(0,599)
		self.y = randint(0,599)
		self.velocityX = randint(1,10)/10.0
		self.velocityY = randint(1,10)/10.0
		self.distract = [randint(0,599),randint(0,599)]
		self.close = False
		self.c1 = 0.001
		self.c2 = 0.005
		self.m1 = 0.01
		self.m2 = 0.025

#		if(Swarm.global_best > self.personal_best_value):
#			Swarm.global_best = self.personal_best_value
	def set_pos(self,x,y):
		self.x = x
		self.y = y

	def move(self,light):
		d = self.distance(light)
		
		if abs(self.velocityX) > Swarm.max_velocity or abs(self.velocityY) > Swarm.max_velocity:
			scaleFactor = Swarm.max_velocity / max(abs(self.velocityX), abs(self.velocityY))
			self.velocityX *= scaleFactor
			self.velocityY *= scaleFactor

		if (d < 250 and self.close == False):
			self.c1 = 0.001
			self.c2 = 0.005
			self.m1 = 0.01
			self.m2 = 0.025
			self.m3 = 0.2
			self.velocityX *= 0.75
			self.velocityY *= 0.75
			self.close = True
		else:
			self.close = False
			self.c1 = 0
			self.c2 = 0.000001
			self.m1 = 0.002
			self.m2 = 0.005
			self.m3 = 0.04

		self.distract = [randint(light.x-125,light.x+125),randint(light.y-125,light.y+125)]
		self.velocityX += 0.5 * (self.c1 * random() * (light.x - self.x) + self.c2 * random() * (self.distract[0] - self.x))
		self.velocityY += 0.5 * (self.c1 * random() * (light.y - self.x) + self.c2 * random() * (self.distract[1] - self.y))
		self.x += self.velocityX
		self.y += self.velocityY

	def distance(self, swrm):
		distX = self.x - swrm.x
		distY = self.y - swrm.y
		return math.sqrt(distX * distX + distY * distY)

	def moveCloser(self, swarms):
		if len(swarms) < 1: 
			return

		avgX = 0
		avgY = 0
		for swrm in swarms:
			if swrm.x == self.x and swrm.y == self.y:
				continue
			avgX += (self.x - swrm.x)
			avgY += (self.y - swrm.y)
		
		avgX /= len(swarms)
		avgY /= len(swarms)

		distance = math.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0

		self.velocityX -= (avgX * self.m1)
		self.velocityY -= (avgY * self.m1)

	def moveWith(self, swarms):
		if len(swarms) < 1: 
			return

		avgX = 0
		avgY = 0
		
		for swrm in swarms:
			avgX += swrm.velocityX
			avgY += swrm.velocityY

		avgX /= len(swarms)
		avgY /= len(swarms)

		self.velocityX += (avgX * self.m2)
		self.velocityY += (avgY * self.m2)

	def moveAway(self, swarms, minDistance):
		if len(swarms) < 1: 
			return

		distanceX = 0
		distanceY = 0
		numClose = 0

		for swrm in swarms:
			distance = self.distance(swrm)
			if  distance < minDistance:
				numClose += 1
				xdiff = (self.x - swrm.x) 
				ydiff = (self.y - swrm.y) 

				if xdiff >= 0: 
					xdiff = math.sqrt(minDistance) - xdiff
				elif xdiff < 0: 
					xdiff = -math.sqrt(minDistance) - xdiff
	
				if ydiff >= 0: 
					ydiff = math.sqrt(minDistance) - ydiff
				elif ydiff < 0: 
					ydiff = -math.sqrt(minDistance) - ydiff

				distanceX += xdiff 
				distanceY += ydiff 
		
		if numClose == 0:
			return

		self.velocityX -= distanceX * self.m3
		self.velocityY -= distanceY * self.m3