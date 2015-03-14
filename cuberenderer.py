from printer import Printer
import pygame
from pygame import Color

class CubeRenderer:
	"""
	Knows how to render a Rubik's Cube onto the screen
	"""
	def __init__(self):
		self.textPrinter = Printer()

	def render(self, screen, cube, x, y):
		self.render2D(screen, cube, x, y)

	def render2D(self, screen, cube, x, y):
		faces = cube.faces()
		# Draw time
		if cube.startTime:
			self.textPrinter.moveTo(x, y)
			if cube.endTime:
				self.textPrinter.printText(screen, str(round((cube.endTime - cube.startTime) / 10) / 100), Color(255, 255, 255))
			else:
				self.textPrinter.printText(screen, str(round((pygame.time.get_ticks() - cube.startTime) / 10) / 100), Color(255, 255, 255))
			self.textPrinter.printText(screen, str(len(cube.moveHistory)), Color(255, 255, 255))
		squareSize = 19
		for i in range(cube.n):
			for j in range(cube.n):
				# Top
				pygame.draw.rect(screen, cube.colorForValue(faces[0][i][j]), [3*(squareSize+1) + j*(squareSize+1) + x, 0*(squareSize+1) + i*(squareSize+1) + y, squareSize, squareSize], 0)
				# Front
				pygame.draw.rect(screen, cube.colorForValue(faces[1][i][j]), [3*(squareSize+1) + j*(squareSize+1) + x, 3*(squareSize+1) + i*(squareSize+1) + y, squareSize, squareSize], 0)
				# Right
				pygame.draw.rect(screen, cube.colorForValue(faces[2][i][j]), [6*(squareSize+1) + j*(squareSize+1) + x, 3*(squareSize+1) + i*(squareSize+1) + y, squareSize, squareSize], 0)
				# Back
				pygame.draw.rect(screen, cube.colorForValue(faces[3][i][j]), [9*(squareSize+1) + j*(squareSize+1) + x, 3*(squareSize+1) + i*(squareSize+1) + y, squareSize, squareSize], 0)
				# Left
				pygame.draw.rect(screen, cube.colorForValue(faces[4][i][j]), [0*(squareSize+1) + j*(squareSize+1) + x, 3*(squareSize+1) + i*(squareSize+1) + y, squareSize, squareSize], 0)
				# Bottom
				pygame.draw.rect(screen, cube.colorForValue(faces[5][i][j]), [3*(squareSize+1) + j*(squareSize+1) + x, 6*(squareSize+1) + i*(squareSize+1) + y, squareSize, squareSize], 0)
