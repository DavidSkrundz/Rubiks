"""
A Cubie class
"""
from pygame import Color
from helpers import Point
from operator import itemgetter

class Cubie:
	"""
	A Cubie class
	"""

	White  = Color(255, 255, 255,   1)
	Yellow = Color(255, 255, 000,   1)
	Red    = Color(255, 000, 000,   1)
	Orange = Color(255, 128, 000,   1)
	Green  = Color(000, 255, 000,   1)
	Blue   = Color(000, 000, 255,   1)
	Clear  = Color(000, 000, 000, 000)
	Black  = Color(000, 000, 000,   1)

	def __init__(self, faceColors, position):
		"""
		faceColors is an array of 6 colors: (Top, Front, Right, Back, Left, Bottom)
		Use Clear for not drawing it

		Position is the (x,y, z) 'number' of the block (0,0,0) is the middle of the center block
		(+1, +1, +1) is the right back top corner of a 3x3x3 cube
		"""
		self.targetX = 0
		self.targetY = 0
		self.targetZ = 0
		self.delta = 30

		self.faceColors = faceColors
		self.position = position

		self.points = [
						Point(self.position.x - 0.5, self.position.y + 0.5, self.position.z + 0.5), # Left , Back , Top
						Point(self.position.x - 0.5, self.position.y - 0.5, self.position.z + 0.5), # Left , Front, Top
						Point(self.position.x + 0.5, self.position.y - 0.5, self.position.z + 0.5), # Right, Front, Top
						Point(self.position.x + 0.5, self.position.y + 0.5, self.position.z + 0.5), # Right, Back , Top
						Point(self.position.x + 0.5, self.position.y + 0.5, self.position.z - 0.5), # Right, Back , Bottom
						Point(self.position.x + 0.5, self.position.y - 0.5, self.position.z - 0.5), # Right, Front, Bottom
						Point(self.position.x - 0.5, self.position.y - 0.5, self.position.z - 0.5), # Left , Front, Bottom
						Point(self.position.x - 0.5, self.position.y + 0.5, self.position.z - 0.5), # Left , Back , Bottom
					]

		self.faces = [
						[0, 1, 2, 3], # Top
						[1, 2, 5, 6], # Front
						[2, 3, 4, 5], # Right
						[0, 3, 4, 7], # Back
						[0, 1, 6, 7], # Left
						[4, 5, 6, 7], # Bottom
					]

	def frontColor(self):
		unsortedPoints = []
		for i in range(len(self.points)):
			unsortedPoints.append((i, self.points[i].y))
		sortedPoints = sorted(unsortedPoints, key=itemgetter(1), reverse=False)
		targetFace = set([sortedPoints[0][0], sortedPoints[1][0], sortedPoints[2][0], sortedPoints[3][0]])
		for i in range(len(self.faces)):
			if set(self.faces[i]) == targetFace:
				return self.faceColors[i]

	def backColor(self):
		unsortedPoints = []
		for i in range(len(self.points)):
			unsortedPoints.append((i, self.points[i].y))
		sortedPoints = sorted(unsortedPoints, key=itemgetter(1), reverse=True)
		targetFace = set([sortedPoints[0][0], sortedPoints[1][0], sortedPoints[2][0], sortedPoints[3][0]])
		for i in range(len(self.faces)):
			if set(self.faces[i]) == targetFace:
				return self.faceColors[i]

	def leftColor(self):
		unsortedPoints = []
		for i in range(len(self.points)):
			unsortedPoints.append((i, self.points[i].x))
		sortedPoints = sorted(unsortedPoints, key=itemgetter(1), reverse=True)
		targetFace = set([sortedPoints[0][0], sortedPoints[1][0], sortedPoints[2][0], sortedPoints[3][0]])
		for i in range(len(self.faces)):
			if set(self.faces[i]) == targetFace:
				return self.faceColors[i]

	def rightColor(self):
		unsortedPoints = []
		for i in range(len(self.points)):
			unsortedPoints.append((i, self.points[i].x))
		sortedPoints = sorted(unsortedPoints, key=itemgetter(1), reverse=False)
		targetFace = set([sortedPoints[0][0], sortedPoints[1][0], sortedPoints[2][0], sortedPoints[3][0]])
		for i in range(len(self.faces)):
			if set(self.faces[i]) == targetFace:
				return self.faceColors[i]

	def topColor(self):
		unsortedPoints = []
		for i in range(len(self.points)):
			unsortedPoints.append((i, self.points[i].z))
		sortedPoints = sorted(unsortedPoints, key=itemgetter(1), reverse=True)
		targetFace = set([sortedPoints[0][0], sortedPoints[1][0], sortedPoints[2][0], sortedPoints[3][0]])
		for i in range(len(self.faces)):
			if set(self.faces[i]) == targetFace:
				return self.faceColors[i]

	def bottomColor(self):
		unsortedPoints = []
		for i in range(len(self.points)):
			unsortedPoints.append((i, self.points[i].z))
		sortedPoints = sorted(unsortedPoints, key=itemgetter(1), reverse=False)
		targetFace = set([sortedPoints[0][0], sortedPoints[1][0], sortedPoints[2][0], sortedPoints[3][0]])
		for i in range(len(self.faces)):
			if set(self.faces[i]) == targetFace:
				return self.faceColors[i]

	def ready(self):
		return self.targetX == 0 and self.targetY == 0 and self.targetZ == 0

	def update(self):
		if self.targetX > 0:
			self.targetX -= self.delta
			for i in range(len(self.points)):
				self.points[i] = self.points[i].rotateX(self.delta)
			return False
		elif self.targetY > 0:
			self.targetY -= self.delta
			for i in range(len(self.points)):
				self.points[i] = self.points[i].rotateY(self.delta)
			return False
		elif self.targetZ > 0:
			self.targetZ -= self.delta
			for i in range(len(self.points)):
				self.points[i] = self.points[i].rotateZ(self.delta)
			return False
		elif self.targetX < 0:
			self.targetX += self.delta
			for i in range(len(self.points)):
				self.points[i] = self.points[i].rotateX(-self.delta)
			return False
		elif self.targetY < 0:
			self.targetY += self.delta
			for i in range(len(self.points)):
				self.points[i] = self.points[i].rotateY(-self.delta)
			return False
		elif self.targetZ < 0:
			self.targetZ += self.delta
			for i in range(len(self.points)):
				self.points[i] = self.points[i].rotateZ(-self.delta)
			return False
		else:
			return True

	def rotateX(self, angle, animate=True):
		if animate:
			self.targetX += angle
		else:
			for i in range(len(self.points)):
				self.points[i] = self.points[i].rotateX(angle)

	def rotateY(self, angle, animate=True):
		if animate:
			self.targetY += angle
		else:
			for i in range(len(self.points)):
				self.points[i] = self.points[i].rotateY(angle)

	def rotateZ(self, angle, animate=True):
		if animate:
			self.targetZ += angle
		else:
			for i in range(len(self.points)):
				self.points[i] = self.points[i].rotateZ(angle)
