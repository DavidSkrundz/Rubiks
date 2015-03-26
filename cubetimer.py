from printer import Printer
import pygame
from pygame import Color

class CubeTimer:
	def __init__(self):
		self.textPrinter = Printer()

		self.startTime = None
		self.endTime = None

	def start(self):
		self.startTime = pygame.time.get_ticks()

	def stop(self):
		self.endTime = pygame.time.get_ticks()

	def reset(self):
		self.startTime = None
		self.endTime = None

	def render(self, screen, x, y):
		if self.startTime:
			self.textPrinter.moveTo(x, y)
			if self.endTime:
				self.textPrinter.printText(screen, str(round((self.endTime - self.startTime) / 10) / 100), Color(255, 255, 255))
			else:
				self.textPrinter.printText(screen, str(round((pygame.time.get_ticks() - self.startTime) / 10) / 100), Color(255, 255, 255))
