import pygame
from pygame import Color
from cubemoverenderer import CubeMoveRenderer

class Button:
	def __init__(self, rect, action):
		self.rect = rect
		self.action = action
		self.enabled = True

	def activate(self):
		if self.enabled:
			self.action()

	def render(self, screen):
		pygame.draw.rect(screen, Color(40, 40, 40), self.rect, 0)
		pygame.draw.rect(screen, Color(80, 80, 80), self.rect, 1)

class TextButton(Button):
	def __init__(self, rect, text, action):
		Button.__init__(self, rect, action)
		self.text = text
		self.font = pygame.font.Font(None, 20)

	def render(self, screen):
		Button.render(self, screen)
		textBitmap = self.font.render(self.text, True, Color(255,255,255))
		w, h = textBitmap.get_size()
		x = self.rect[0] + self.rect[2]/2 - w/2
		y = self.rect[1] + self.rect[3]/2 - h/2
		screen.blit(textBitmap, (x, y))

class ImageButton(Button):
	def __init__(self, rect, image, action):
		Button.__init__(self, rect, action)
		self.image = image

	def render(self, screen):
		Button.render(self, screen)
		w, h = self.image.get_size()
		x = self.rect[0] + self.rect[2]/2 - w/2
		y = self.rect[1] + self.rect[3]/2 - h/2
		screen.blit(self.image, (x, y))

class MoveButton(Button):
	def __init__(self, x, y, cube, move, offsets):
		Button.__init__(self, (x, y, CubeMoveRenderer.size(cube.N), CubeMoveRenderer.size(cube.N)), self.cubeAction)
		self.move = move
		self.offsets = offsets
		self.cube = cube

	def cubeAction(self):
		pass

	def render(self, screen):
		CubeMoveRenderer.render(screen, self.rect[0], self.rect[1], self.cube.N, self.move, self.offsets)
