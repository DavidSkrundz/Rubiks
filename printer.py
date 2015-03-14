import pygame

class Printer:
	"""
	Helps with printing text to the screen
	"""
	def __init__(self):
		self.font = pygame.font.Font(None, 20)
		self.x = 0
		self.y = 0
		self.line_height = 15

	def moveTo(self, x, y):
		self.x = x
		self.y = y

	def shift(self, x, y):
		self.x += x
		self.y += y

	def printText(self, screen, text, color):
		textBitmap = self.font.render(text, True, color)
		screen.blit(textBitmap, [self.x, self.y])
		self.y += self.line_height
