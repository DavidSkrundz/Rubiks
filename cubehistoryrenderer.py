from cube import Cube
import math
import pygame
from cubemoverenderer import CubeMoveRenderer

class CubeHistoryRenderer:
	"""
	Renders the history of a cube
	"""
	# Create a dictionary of sprites for rotations

	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.surfaceY = 0

		self.h = self.height

		self.surfaceWidth = 0
		self.surfaceHeight = 0
		self.__createNewSurface()

	def __createNewSurface(self):
		self.surfaceWidth = self.width
		self.surfaceHeight = self.h*24
		self.surface = pygame.surface.Surface((self.surfaceWidth, self.surfaceHeight))

	def render(self, screen, cube):
		# Draw move history
		self.__renderSurface(cube)
		# Draw the surface onto the screen
		screen.blit(self.surface, (self.x, self.y), area=(0, self.surfaceY, self.surfaceWidth, self.height))

	def __renderSurface(self, cube):
		s = CubeMoveRenderer.size(cube.N)
		w = math.floor(self.width / s)
		h = math.floor(self.height / s)
		# If we don't have enough space
		if len(cube.moveHistory) > w * h:
			self.h = math.ceil(len(cube.moveHistory) / w) + 5
			self.__createNewSurface()
		# Draw the move history
		self.surface.fill((50,50,50))
		i = 0
		j = 0
		for item in cube.moveHistory:
			x = s * i
			y = s * j
			CubeMoveRenderer.render(self.surface, x, y, cube.N, item[0], item[1])
			i = (i + 1) % w
			if i == 0:
				j += 1
