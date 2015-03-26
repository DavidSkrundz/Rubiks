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
	def __init__(self):
		self.textPrinter = Printer()

		self.rotateX = -45
		self.rotateY = 0
		self.rotateZ = 30

# 		self.rotateX = 90 + 30
# 		self.rotateY = -30
# 		self.rotateZ = 165

		self.win_width = 100
		self.win_height = 100
		self.fov = 600
		self.viewer_distance = 10

	def render(self, screen, cube, x, y):
		t = [] # Transformed vertices
		f = [] # Converted faces
		c = [] # Colors

		# Save the data into the arrays
		for cubie in cube.cubies:
			faceVertexOffset = len(t)
			for point in cubie.points:
				v = point.rotateX(self.rotateX).rotateY(self.rotateY).rotateZ(self.rotateZ).project(self.win_width, self.win_height, self.fov, self.viewer_distance)
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
						(x + t[f[faceIndex][0]].x, y + t[f[faceIndex][0]].y), (x + t[f[faceIndex][1]].x, y + t[f[faceIndex][1]].y),
						(x + t[f[faceIndex][1]].x, y + t[f[faceIndex][1]].y), (x + t[f[faceIndex][2]].x, y + t[f[faceIndex][2]].y),
						(x + t[f[faceIndex][2]].x, y + t[f[faceIndex][2]].y), (x + t[f[faceIndex][3]].x, y + t[f[faceIndex][3]].y),
						(x + t[f[faceIndex][3]].x, y + t[f[faceIndex][3]].y), (x + t[f[faceIndex][0]].x, y + t[f[faceIndex][0]].y)
					]
			if c[faceIndex] != Cubie.Clear:
				pygame.draw.polygon(screen, c[faceIndex], points)
				pygame.draw.lines(screen, Cubie.Black, True, points)
