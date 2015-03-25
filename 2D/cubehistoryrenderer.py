from cube import Cube
import math
import pygame

class CubeHistoryRenderer:
	"""
	Renders the history of a cube
	"""
	# Create a dictionary of sprites for rotations
	RotationStepSprites = {}

	def __init__(self, x, y, blocksWide, height):
		# If CubeRenderer.RotationStepSprites is empty add the sprites
		if not CubeHistoryRenderer.RotationStepSprites: # all 24x24 images
			CubeHistoryRenderer.RotationStepSprites[Cube.Center] = pygame.image.load("../assets/3x3/C.png").convert()
			CubeHistoryRenderer.RotationStepSprites[Cube.Center_] = pygame.image.load("../assets/3x3/C_.png").convert()
			CubeHistoryRenderer.RotationStepSprites[Cube.Bottom] = pygame.image.load("../assets/3x3/D.png").convert()
			CubeHistoryRenderer.RotationStepSprites[Cube.Bottom_] = pygame.image.load("../assets/3x3/D_.png").convert()
			CubeHistoryRenderer.RotationStepSprites[Cube.Front] = pygame.image.load("../assets/3x3/F.png").convert()
			CubeHistoryRenderer.RotationStepSprites[Cube.Front_] = pygame.image.load("../assets/3x3/F_.png").convert()
			CubeHistoryRenderer.RotationStepSprites[Cube.Left] = pygame.image.load("../assets/3x3/L.png").convert()
			CubeHistoryRenderer.RotationStepSprites[Cube.Left_] = pygame.image.load("../assets/3x3/L_.png").convert()
			CubeHistoryRenderer.RotationStepSprites[Cube.Middle] = pygame.image.load("../assets/3x3/M.png").convert()
			CubeHistoryRenderer.RotationStepSprites[Cube.Middle_] = pygame.image.load("../assets/3x3/M_.png").convert()
			CubeHistoryRenderer.RotationStepSprites[Cube.Right] = pygame.image.load("../assets/3x3/R.png").convert()
			CubeHistoryRenderer.RotationStepSprites[Cube.Right_] = pygame.image.load("../assets/3x3/R_.png").convert()
			CubeHistoryRenderer.RotationStepSprites[Cube.Top] = pygame.image.load("../assets/3x3/U.png").convert()
			CubeHistoryRenderer.RotationStepSprites[Cube.Top_] = pygame.image.load("../assets/3x3/U_.png").convert()

		self.x = x
		self.y = y
		self.surfaceY = 0
		self.width = blocksWide * (24 + 1) + 1
		self.height = height

		self.w = blocksWide
		self.h = math.floor((height - 1) / 25) # For preallocation

		self.surfaceWidth = 0
		self.surfaceHeight = 0
		self.__createNewSurface()

	def __createNewSurface(self):
		self.surfaceWidth = self.w * (24 + 1)
		self.surfaceHeight = max(self.h * (24 + 1), self.height)
		self.surface = pygame.surface.Surface((self.surfaceWidth, self.surfaceHeight))

	def render(self, screen, cube):
		# Draw move history
		self.__renderSurface(cube)
		# Draw the surface onto the screen
		screen.blit(self.surface, (self.x, self.y), area=(0, self.surfaceY, self.surfaceWidth, self.height))

	def __renderSurface(self, cube):
		# If we don't have enough space
		if len(cube.moveHistory) > self.w * self.h:
			self.h = math.ceil(len(cube.moveHistory) / self.w)
			self.__createNewSurface()
		# Draw the move history
		self.surface.fill((50,50,50))
		i = 0
		j = 0
		for item in cube.moveHistory:
			x = 25 * i
			y = 25 * j
			self.surface.blit(CubeHistoryRenderer.RotationStepSprites[item], (x, y))
			i = (i + 1) % self.w
			if i == 0:
				j += 1
