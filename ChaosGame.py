import colorsys
import math
import pygame
import random
import sys

class ChaosGame:

	def __init__(self, width, height, nSides, randSetting):
		self.width = width
		self.height = height
		self.nSides = nSides
		self.randSetting = randSetting
		self.curCorner = 0
		self.prevCorners = [0, 0]


	def getPolygon(self):
		delta = 360/self.nSides
		radius = self.width/2
		polygon = []

		for i in range(0, self.nSides):
			angle = (180 + i*delta)*math.pi/180
			color = colorsys.hsv_to_rgb((i*delta)/360, 0.8, 1)
			polygon.append(((self.width/2 + radius*math.sin(angle), self.height/2 + radius*math.cos(angle)),(int(color[0]*255), int(color[1]*255), int(color[2]*255))))
		return polygon

	def getRandomCorner(self, randSetting):

		# Next polygon corner is chosen at random with no restrictions
		if randSetting == 0:
			next = random.randint(0,self.nSides-1)
			return next

		# Next polygon corner is always different from the current polygon corner
		elif randSetting == 1:
			next = random.randint(0,self.nSides-1)
			while next == self.curCorner:
				next = random.randint(0,self.nSides-1)
			self.curCorner = next
			return next

		# The next corner will never be adjacent to curent corner
		elif randSetting == 2 and self.nSides > 4:
			next = random.randint(0,self.nSides-1)
			while (next == (self.curCorner+1)%self.nSides) or (next == (self.curCorner-1)%self.nSides):
				next = random.randint(0,self.nSides-1)
			self.curCorner = next
			return next

		# If the same polygon corner is chosen twice in a row the next polygon corner will not be adjacent to the current corner
		elif randSetting == 3 and self.nSides > 3:
			self.prevCorners[1] = self.prevCorners[0]
			self.prevCorners[0] = self.curCorner
			self.curCorner = random.randint(0, self.nSides - 1)
			if self.prevCorners[0] == self.prevCorners[1]:
				while ( (self.curCorner+1)%self.nSides == self.prevCorners[0] or (self.curCorner-1)%self.nSides == self.prevCorners[0] ):
					self.curCorner = random.randint(0, self.nSides - 1)
			return self.curCorner

		else:
			print ("Error: undefined randomness setting")
			sys.exit(1)


# Display functions

def markPixel(surface, position, pixelColor):
	color = surface.get_at(position)
	surface.set_at(position, (min(color[0] + pixelColor[0] / 10, 255),min(color[1] + pixelColor[1] / 10, 255), min(color[2] + pixelColor[2] / 10, 255)))


def displayFractal(width, height):

	mode = 3
	nSides = 5
	offset = 0.5

	# Pygame initial setup
	pygame.init()
	screen = pygame.display.set_mode((width, height))
	background = (0,0,0)
	screen.fill(background)
	pygame.display.set_caption("Fractal Generator")

	chaosGame = ChaosGame(width,height,nSides,0)
	toDisplay = chaosGame.getPolygon()

	# Display Loop
	while True:
		x,y = (0,0)
		for i in range(0,width*height):
			curCorner = chaosGame.getRandomCorner(mode)
			x += (toDisplay[curCorner][0][0] - x) * offset
			y += (toDisplay[curCorner][0][1] - y) * offset
			markPixel(screen, (int(x),int(y)), toDisplay[curCorner][1])

			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return

	pygame.quit()


def main():
	width = 1000
	height = 1000
	displayFractal(width,height)
if __name__ == "__main__":
	main()
