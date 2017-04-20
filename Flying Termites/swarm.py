from random import randint,random
import numpy as np
import math

class Swarm:
	light = [250,250]
	max_velocity = 10
	def __init__(self):
		self.x = randint(0,499)
		self.y = randint(0,499)
		self.velocityX = randint(1,10)/10.0
		self.velocityY = randint(1,10)/10.0
		self.distract = [randint(0,499),randint(0,499)]
		self.close = False
		self.c1 = 0.001
		self.c2 = 0.005

#		if(Swarm.global_best > self.personal_best_value):
#			Swarm.global_best = self.personal_best_value

	def move(self):
		x = Swarm.light[0]
		y = Swarm.light[1]
		
		if abs(self.velocityX) > Swarm.max_velocity or abs(self.velocityY) > Swarm.max_velocity:
			scaleFactor = Swarm.max_velocity / max(abs(self.velocityX), abs(self.velocityY))
			self.velocityX *= scaleFactor
			self.velocityY *= scaleFactor

		if (self.x >= x-125 and self.x <= x+125 and self.y >= y-125 and self.y <= y+125 and self.close == False):
			self.c1 = 0.001
			self.c2 = 0.005
			self.velocityX *= 0.75
			self.velocityY *= 0.75
			self.close = True
		else:
			self.close = False
			self.c1 = 0
			self.c2 = 0.00001

		self.distract = [randint(x-125,x+125),randint(y-125,y+125)]
		self.velocityX += 0.5 * self.c1 * random() * (Swarm.light[0] - self.x) + self.c2 * random() * (self.distract[0] - self.x)
		self.velocityY += 0.5 * self.c1 * random() * (Swarm.light[1] - self.x) + self.c2 * random() * (self.distract[1] - self.y)
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

		self.velocityX -= (avgX / 100)
		self.velocityY -= (avgY / 100) 

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

		self.velocityX += (avgX / 40)
		self.velocityY += (avgY / 40)

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

		self.velocityX -= distanceX / 5
		self.velocityY -= distanceY / 5