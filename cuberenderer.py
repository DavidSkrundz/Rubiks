from printer import Printer
import pygame
from pygame import Color
from copy import deepcopy
from operator import itemgetter
from cubie import Cubie

class CubeRenderer:
	"""
	Knows how to render a Rubik's Cube onto the screen
	"""
	def __init__(self, x, y):
		self.textPrinter = Printer()

		self.rotateX = -90 - 30
		self.rotateY = 0
		self.rotateZ = 45 + 90 + 90

		self.deltaRotateX = 45
		self.deltaRotateZ = 40

		self.x = x
		self.y = y

		self.win_width = 100
		self.win_height = 100
		self.fov = 600
		self.viewer_distance = 10

		self.newX = self.x - self.win_width
		self.newY = self.y - self.win_height + 15
		self.newW = self.win_width * 3
		self.newH = self.win_height * 3

		self.mouseStartX = None
		self.mouseStartY = None

	def click(self, x, y, button, press):
		if not press:
			self.mouseStartX = None
			self.mouseStartY = None
		if x > self.newX and x < self.newX + self.newW:
			if y > self.newY and y < self.newY + self.newH:
				if button == 1:
					if press:
						self.mouseStartX = x
						self.mouseStartY = y

	def mouseMove(self, x, y, dx, dy):
		if self.mouseStartX and self.mouseStartY:
			self.deltaRotateX -= dx
			self.deltaRotateZ -= dy
			self.rotateZ -= dx
			self.rotateX -= dy

	def mouseOver(self, x, y):
		if x > self.newX and x < self.newX + self.newW:
			if y > self.newY and y < self.newY + self.newH:
				return True
		if self.mouseStartX != None:
			return True
		return False

	def render(self, screen, cube, doneUpdates):
		if doneUpdates:
			if self.deltaRotateX > 90:
				self.deltaRotateX -= 90
				self.rotateZ -= 90
				cube.UUU_(False)
			if self.deltaRotateX < 0:
				self.deltaRotateX += 90
				self.rotateZ += 90
				cube.UUU(False)

			if self.deltaRotateZ > 90:
				if self.deltaRotateX < 10:
					self.deltaRotateZ -= 90
					self.rotateX -= 90
					cube.RRR(False)

			if self.deltaRotateZ < 0:
				if self.deltaRotateX < 10:
					self.deltaRotateZ += 90
					self.rotateX += 90
					cube.RRR_(False)

		pygame.draw.rect(screen, Color(40, 40, 40), (self.newX, self.newY, self.newW, self.newH), 0)

		t = [] # Transformed vertices
		f = [] # Converted faces
		c = [] # Colors

		# Save the data into the arrays
		for cubie in cube.cubies:
			faceVertexOffset = len(t)
			for point in cubie.points:
				v = point.rotateZ(self.rotateZ).rotateY(self.rotateY).rotateX(self.rotateX).project(self.win_width, self.win_height, self.fov, self.viewer_distance)
				t.append(v)
			for face in cubie.faces:
				newFace = deepcopy(face)
				for i in range(4):
					newFace[i] += faceVertexOffset
				f.append(newFace)
			for color in cubie.faceColors:
				c.append(color)

		# Calculate the average Z values of each face.
		averageZ = []
		i = 0
		for face in f:
			z = (t[f[i][0]].z + t[f[i][1]].z + t[f[i][2]].z + t[f[i][3]].z) / 4.0
			averageZ.append([i, z])
			i += 1

		# Now draw with Painter's algorithm
		for faceData in sorted(averageZ, key=itemgetter(1), reverse=True):
			faceIndex = faceData[0]
			face = f[faceIndex]
			points = [
						(self.x + t[f[faceIndex][0]].x, self.y + t[f[faceIndex][0]].y), (self.x + t[f[faceIndex][1]].x, self.y + t[f[faceIndex][1]].y),
						(self.x + t[f[faceIndex][1]].x, self.y + t[f[faceIndex][1]].y), (self.x + t[f[faceIndex][2]].x, self.y + t[f[faceIndex][2]].y),
						(self.x + t[f[faceIndex][2]].x, self.y + t[f[faceIndex][2]].y), (self.x + t[f[faceIndex][3]].x, self.y + t[f[faceIndex][3]].y),
						(self.x + t[f[faceIndex][3]].x, self.y + t[f[faceIndex][3]].y), (self.x + t[f[faceIndex][0]].x, self.y + t[f[faceIndex][0]].y)
					]
			if c[faceIndex] != Cubie.Clear:
				pygame.draw.polygon(screen, c[faceIndex], points)
				pygame.draw.lines(screen, Cubie.Black, True, points)
