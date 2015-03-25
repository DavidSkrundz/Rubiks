from copy import deepcopy
import pygame
from pygame import Color
from random import randint

from pygame.mixer import Sound

class Cube:
	"""
	Represents a rubik's cube that is NxNxN
	"""

	# Some constants
	Top = "U"
	Bottom = "D"
	Left = "L"
	Right = "R"
	Front = "F"
	Back = "B"
	Center = "C"
	Middle = "M"
	Top_ = "U'"
	Bottom_ = "D'"
	Left_ = "L'"
	Right_ = "R'"
	Front_ = "F'"
	Back_ = "B'"
	Center_ = "C'"
	Middle_ = "M'"

	White = 0
	Yellow = 1
	Red = 2
	Orange = 3
	Green = 4
	Blue = 5

	def __init__(self, n):
		self.n = n
		# Initialize all faces solved
		# -----
		# These arrays of arrays represent the rows/columns NOT x/y
		# eg. self.__topFace[row][column]
		# Refer to CubeCoordsX.png for the orientation of each face (where [0][0] is)
		# -----
		self.__topFace 		= [[Cube.White] * self.n for _ in range(self.n)]
		self.__bottomFace 	= [[Cube.Yellow] * self.n for _ in range(self.n)]
		self.__frontFace 	= [[Cube.Red] * self.n for _ in range(self.n)]
		self.__backFace 	= [[Cube.Orange] * self.n for _ in range(self.n)]
		self.__leftFace 	= [[Cube.Green] * self.n for _ in range(self.n)]
		self.__rightFace 	= [[Cube.Blue] * self.n for _ in range(self.n)]
		# Default colors
		self.topColor 		= Color(255, 255, 255, 1) # White
		self.bottomColor 	= Color(255, 255, 000, 1) # Yellow
		self.frontColor 	= Color(255, 000, 000, 1) # Red
		self.backColor 		= Color(255, 128, 000, 1) # Orange
		self.leftColor 		= Color(000, 255, 000, 1) # Green
		self.rightColor 	= Color(000, 000, 255, 1) # Blue
		# For tracking performance
		self.moveHistory = []
		self.startTime = None
		self.endTime = None

	def randomize(self):
		"""
		Randomly applies a single move to the cube
		"""
		operation = randint(0,11)
		if operation == 0:
			self.F(False)
		elif operation == 1:
			self.F_(False)
		elif operation == 2:
			self.B(False)
		elif operation == 3:
			self.B_(False)
		elif operation == 4:
			self.U(False)
		elif operation == 5:
			self.U_(False)
		elif operation == 6:
			self.D(False)
		elif operation == 7:
			self.D_(False)
		elif operation == 8:
			self.L(False)
		elif operation == 9:
			self.L_(False)
		elif operation == 10:
			self.R(False)
		elif operation == 11:
			self.R_(False)

	def isSolved(self):
		"""
		Checks the cube to see if it has been solved
		"""
		for face in self.faces():
			thisFaceColor = face[0][0]
			for i in range(self.n):
				for j in range(self.n):
					if face[i][j] != thisFaceColor:
						return False
		if self.endTime == None:
			self.endTime = pygame.time.get_ticks()
		return True

	def faces(self):
		"""
		Returns a tuple of each face (top, front, right, back, left, bottom)
		pls don't change anything... pls
		"""
		return (self.__topFace, self.__frontFace, self.__rightFace, self.__backFace, self.__leftFace, self.__bottomFace)

	def colorForValue(self, value):
		"""
		Returns the proper color given the value stored in that square
		"""
		if value == 0:
			return self.topColor
		elif value == 1:
			return self.bottomColor
		elif value == 2:
			return self.frontColor
		elif value == 3:
			return self.backColor
		elif value == 4:
			return self.leftColor
		elif value == 5:
			return self.rightColor
		else:
			raise Exception("Bad value; No color exists!")

	def rotateFaceArray(self, faceArray):
		"""
		Rotates only the given self.__xFace which is a 2D array

		Rotate CW
		"""
		# Make a copy
		tempArray = deepcopy(faceArray)
		# Rotate the numbers 90 degrees CW
		for i in range(self.n):
			for j in range(self.n):
				faceArray[i][j] = tempArray[self.n-1 - j][i]

	def rotateFaceArray_(self, faceArray):
		"""
		Rotates only the given self.__xFace which is a 2D array

		Rotate CCW
		"""
		# Make a copy
		tempArray = deepcopy(faceArray)
		# Rotate the numbers 90 degrees CW
		for i in range(self.n):
			for j in range(self.n):
				faceArray[i][j] = tempArray[j][self.n-1 - i]

	# Add the move to the history
	def performMove(self, move):
		"""
		Move is a constant from Cube
		"""
		if self.endTime:
			if not self.isSolved():
				self.moveHistory = []
				self.startTime = None
				self.endTime = None

		# If its the first move start the timer
		if len(self.moveHistory) == 0:
			self.startTime = pygame.time.get_ticks()
			self.endTime = None

			pygame.mixer.music.load("../assets/audio/BGM.wav")
			pygame.mixer.music.play(loops=-1)

		self.moveHistory.append(move)

		if self.isSolved():
			self.endTime = pygame.time.get_ticks()
			# Play the VICTORY SOUND!!!
			winSound = Sound(file = "../assets/audio/WIN.wav")
			winSound.play()
			pygame.mixer.music.fadeout(1)

	# Turn (Rotate) Entire Cube ->
	def T(self, timed = True):
		self.U_(timed)
		self.M(timed)
		self.D(timed)

	def T_(self, timed = True):#	<-
		self.U(timed)
		self.M_(timed)
		self.D_(timed)

	# Spin (Rotate) Entire Cube ^ ^ ^
	def S(self, timed = True):#        		| | |
		self.R(timed)
		self.C(timed)
		self.L_(timed)

	#				| | |
	def S_(self, timed = True):#	v v v
		self.R_(timed)
		self.C_(timed)
		self.L(timed)

	# Front Face	^ v
	def F(self, timed = True):
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.F(False)
		>>> cube.faces()
		([[0, 1, 2], [3, 4, 5], [44, 41, 38]], [[15, 12, 9], [16, 13, 10], [17, 14, 11]], [[6, 19, 20], [7, 22, 23], [8, 25, 26]], [[27, 28, 29], [30, 31, 32], [33, 34, 35]], [[36, 37, 45], [39, 40, 46], [42, 43, 47]], [[24, 21, 18], [48, 49, 50], [51, 52, 53]])
		"""
		self.rotateFaceArray(self.__frontFace)

		# Save top
		tempArray = deepcopy(self.__topFace[self.n-1])
		# Move left to top
		for i in range(self.n):
			self.__topFace[self.n-1][i] = self.__leftFace[self.n-1 - i][self.n-1]
		# Move bottom to left
		for i in range(self.n):
			self.__leftFace[i][self.n-1] = self.__bottomFace[0][i]
		# Move right to bottom
		for i in range(self.n):
			self.__bottomFace[0][i] = self.__rightFace[self.n-1 - i][0]
		# Restore top to right
		for i in range(self.n):
			self.__rightFace[i][0] = tempArray[i]
		if timed:
			self.performMove(Cube.Front)

	def F_(self, timed = True):#	v ^
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.F_(False)
		>>> cube.faces()
		([[0, 1, 2], [3, 4, 5], [18, 21, 24]], [[11, 14, 17], [10, 13, 16], [9, 12, 15]], [[47, 19, 20], [46, 22, 23], [45, 25, 26]], [[27, 28, 29], [30, 31, 32], [33, 34, 35]], [[36, 37, 8], [39, 40, 7], [42, 43, 6]], [[38, 41, 44], [48, 49, 50], [51, 52, 53]])
		"""
		self.rotateFaceArray_(self.__frontFace)

		# Save top
		tempArray = deepcopy(self.__topFace[self.n-1])
		# Move right to top
		for i in range(self.n):
			self.__topFace[self.n-1][i] = self.__rightFace[i][0]
		# Move bottom to right
		for i in range(self.n):
			self.__rightFace[i][0] = self.__bottomFace[0][self.n-1 - i]
		# Move left to bottom
		for i in range(self.n):
			self.__bottomFace[0][i] = self.__leftFace[i][self.n-1]
		# Restore top to left
		for i in range(self.n):
			self.__leftFace[i][self.n-1] = tempArray[self.n-1 - i]

		if timed:
			self.performMove(Cube.Front_)

	# Back Face		v ^
	def B(self, timed = True):
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.B(False)
		>>> cube.faces()
		([[20, 23, 26], [3, 4, 5], [6, 7, 8]], [[9, 10, 11], [12, 13, 14], [15, 16, 17]], [[18, 19, 53], [21, 22, 52], [24, 25, 51]], [[33, 30, 27], [34, 31, 28], [35, 32, 29]], [[2, 37, 38], [1, 40, 41], [0, 43, 44]], [[45, 46, 47], [48, 49, 50], [36, 39, 42]])
		"""
		self.rotateFaceArray(self.__backFace)

		# Save top
		tempArray = deepcopy(self.__topFace[0])
		# Move right to top
		for i in range(self.n):
			self.__topFace[0][i] = self.__rightFace[i][self.n-1]
		# Move bottom to right
		for i in range(self.n):
			self.__rightFace[i][self.n-1] = self.__bottomFace[self.n-1][self.n-1 - i]
		# Move left to bottom
		for i in range(self.n):
			self.__bottomFace[self.n-1][self.n-1 - i] = self.__leftFace[self.n-1 - i][0]
		# Restore top to left
		for i in range(self.n):
			self.__leftFace[self.n-1 - i][0] = tempArray[i]

		if timed:
			self.performMove(Cube.Back)

	def B_(self, timed = True):#	^ v
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.B_(False)
		>>> cube.faces()
		([[42, 39, 36], [3, 4, 5], [6, 7, 8]], [[9, 10, 11], [12, 13, 14], [15, 16, 17]], [[18, 19, 0], [21, 22, 1], [24, 25, 2]], [[29, 32, 35], [28, 31, 34], [27, 30, 33]], [[51, 37, 38], [52, 40, 41], [53, 43, 44]], [[45, 46, 47], [48, 49, 50], [26, 23, 20]])
		"""
		self.rotateFaceArray_(self.__backFace)

		# Save top
		tempArray = deepcopy(self.__topFace[0])
		# Move left to top
		for i in range(self.n):
			self.__topFace[0][i] = self.__leftFace[self.n-1 - i][0]
		# Move bottom to left
		for i in range(self.n):
			self.__leftFace[self.n-1 - i][0] = self.__bottomFace[self.n-1][self.n-1 - i]
		# Move right to bottom
		for i in range(self.n):
			self.__bottomFace[self.n-1][self.n-1 - i] = self.__rightFace[i][self.n-1]
		# Restore top to right
		for i in range(self.n):
			self.__rightFace[i][self.n-1] = tempArray[i]

		if timed:
			self.performMove(Cube.Back_)

	# Left Face		|
	def L(self, timed = True):#	v
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.L(False)
		>>> cube.faces()
		([[35, 1, 2], [32, 4, 5], [29, 7, 8]], [[0, 10, 11], [3, 13, 14], [6, 16, 17]], [[18, 19, 20], [21, 22, 23], [24, 25, 26]], [[27, 28, 51], [30, 31, 48], [33, 34, 45]], [[42, 39, 36], [43, 40, 37], [44, 41, 38]], [[9, 46, 47], [12, 49, 50], [15, 52, 53]])
		"""
		self.rotateFaceArray(self.__leftFace)

		# Save top
		tempArray = []
		for i in range(self.n):
			tempArray.append(self.__topFace[i][0])
		# Move back to top
		for i in range(self.n):
			self.__topFace[i][0] = self.__backFace[self.n-1 - i][self.n-1]
		# Move bottom to back
		for i in range(self.n):
			self.__backFace[self.n-1 - i][self.n-1] = self.__bottomFace[i][0]
		# Move front to bottom
		for i in range(self.n):
			self.__bottomFace[i][0] = self.__frontFace[i][0]
		# Restore top to front
		for i in range(self.n):
			self.__frontFace[i][0] = tempArray[i]

		if timed:
			self.performMove(Cube.Left)

	#				^
	def L_(self, timed = True):#	|
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.L_(False)
		>>> cube.faces()
		([[9, 1, 2], [12, 4, 5], [15, 7, 8]], [[45, 10, 11], [48, 13, 14], [51, 16, 17]], [[18, 19, 20], [21, 22, 23], [24, 25, 26]], [[27, 28, 6], [30, 31, 3], [33, 34, 0]], [[38, 41, 44], [37, 40, 43], [36, 39, 42]], [[35, 46, 47], [32, 49, 50], [29, 52, 53]])
		"""
		self.rotateFaceArray_(self.__leftFace)

		# Save top
		tempArray = []
		for i in range(self.n):
			tempArray.append(self.__topFace[i][0])
		# Move front to top
		for i in range(self.n):
			self.__topFace[i][0] = self.__frontFace[i][0]
		# Move bottom to front
		for i in range(self.n):
			self.__frontFace[i][0] = self.__bottomFace[i][0]
		# Move back to bottom
		for i in range(self.n):
			self.__bottomFace[i][0] = self.__backFace[self.n-1 - i][self.n-1]
		# Restore top to back
		for i in range(self.n):
			self.__backFace[self.n-1 - i][self.n-1] = tempArray[i]

		if timed:
			self.performMove(Cube.Left_)

	# Right Face	^
	def R(self, timed = True):#	|
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.R(False)
		>>> cube.faces()
		([[0, 1, 11], [3, 4, 14], [6, 7, 17]], [[9, 10, 47], [12, 13, 50], [15, 16, 53]], [[24, 21, 18], [25, 22, 19], [26, 23, 20]], [[8, 28, 29], [5, 31, 32], [2, 34, 35]], [[36, 37, 38], [39, 40, 41], [42, 43, 44]], [[45, 46, 33], [48, 49, 30], [51, 52, 27]])
		"""
		self.rotateFaceArray(self.__rightFace)

		# Save top
		tempArray = []
		for i in range(self.n):
			tempArray.append(self.__topFace[i][self.n-1])
		# Move front to top
		for i in range(self.n):
			self.__topFace[i][self.n-1] = self.__frontFace[i][self.n-1]
		# Move bottom to front
		for i in range(self.n):
			self.__frontFace[i][self.n-1] = self.__bottomFace[i][self.n-1]
		# Move back to bottom
		for i in range(self.n):
			self.__bottomFace[i][self.n-1] = self.__backFace[self.n-1 - i][0]
		# Restore top to back
		for i in range(self.n):
			self.__backFace[i][0] = tempArray[self.n-1 - i]

		if timed:
			self.performMove(Cube.Right)

	#				|
	def R_(self, timed = True):#	v
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.R_(False)
		>>> cube.faces()
		([[0, 1, 33], [3, 4, 30], [6, 7, 27]], [[9, 10, 2], [12, 13, 5], [15, 16, 8]], [[20, 23, 26], [19, 22, 25], [18, 21, 24]], [[53, 28, 29], [50, 31, 32], [47, 34, 35]], [[36, 37, 38], [39, 40, 41], [42, 43, 44]], [[45, 46, 11], [48, 49, 14], [51, 52, 17]])
		"""
		self.rotateFaceArray_(self.__rightFace)

		# Save top
		tempArray = []
		for i in range(self.n):
			tempArray.append(self.__topFace[i][self.n-1])
		# Move back to top
		for i in range(self.n):
			self.__topFace[i][self.n-1] = self.__backFace[self.n-1 - i][0]
		# Move bottom to back
		for i in range(self.n):
			self.__backFace[i][0] = self.__bottomFace[self.n-1 - i][self.n-1]
		# Move front to bottom
		for i in range(self.n):
			self.__bottomFace[i][self.n-1] = self.__frontFace[i][self.n-1]
		# Restore top to front
		for i in range(self.n):
			self.__frontFace[i][self.n-1] = tempArray[i]

		if timed:
			self.performMove(Cube.Right_)

	# Up (Top) Face	<-
	def U(self, timed = True):
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.U(False)
		>>> cube.faces()
		([[6, 3, 0], [7, 4, 1], [8, 5, 2]], [[18, 19, 20], [12, 13, 14], [15, 16, 17]], [[27, 28, 29], [21, 22, 23], [24, 25, 26]], [[36, 37, 38], [30, 31, 32], [33, 34, 35]], [[9, 10, 11], [39, 40, 41], [42, 43, 44]], [[45, 46, 47], [48, 49, 50], [51, 52, 53]])
		"""
		self.rotateFaceArray(self.__topFace)

		# Save front
		tempArray = deepcopy(self.__frontFace[0])
		# Move right to front
		for i in range(self.n):
			self.__frontFace[0][i] = self.__rightFace[0][i]
		# Move back to right
		for i in range(self.n):
			self.__rightFace[0][i] = self.__backFace[0][i]
		# Move left to back
		for i in range(self.n):
			self.__backFace[0][i] = self.__leftFace[0][i]
		# Restore front to left
		for i in range(self.n):
			self.__leftFace[0][i] = tempArray[i]

		if timed:
			self.performMove(Cube.Top)

	def U_(self, timed = True):#	->
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.U_(False)
		>>> cube.faces()
		([[2, 5, 8], [1, 4, 7], [0, 3, 6]], [[36, 37, 38], [12, 13, 14], [15, 16, 17]], [[9, 10, 11], [21, 22, 23], [24, 25, 26]], [[18, 19, 20], [30, 31, 32], [33, 34, 35]], [[27, 28, 29], [39, 40, 41], [42, 43, 44]], [[45, 46, 47], [48, 49, 50], [51, 52, 53]])
		"""
		self.rotateFaceArray_(self.__topFace)

		# Save front
		tempArray = deepcopy(self.__frontFace[0])
		# Move left to front
		for i in range(self.n):
			self.__frontFace[0][i] = self.__leftFace[0][i]
		# Move back to left
		for i in range(self.n):
			self.__leftFace[0][i] = self.__backFace[0][i]
		# Move right to back
		for i in range(self.n):
			self.__backFace[0][i] = self.__rightFace[0][i]
		# Restore front to right
		for i in range(self.n):
			self.__rightFace[0][i] = tempArray[i]

		if timed:
			self.performMove(Cube.Top_)

	# Down (Bottom) Face	->
	def D(self, timed = True):
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.D(False)
		>>> cube.faces()
		([[0, 1, 2], [3, 4, 5], [6, 7, 8]], [[9, 10, 11], [12, 13, 14], [42, 43, 44]], [[18, 19, 20], [21, 22, 23], [15, 16, 17]], [[27, 28, 29], [30, 31, 32], [24, 25, 26]], [[36, 37, 38], [39, 40, 41], [33, 34, 35]], [[51, 48, 45], [52, 49, 46], [53, 50, 47]])
		"""
		self.rotateFaceArray(self.__bottomFace)

		# Save front
		tempArray = deepcopy(self.__frontFace[self.n-1])
		# Move left to front
		for i in range(self.n):
			self.__frontFace[self.n-1][i] = self.__leftFace[self.n-1][i]
		# Move back to left
		for i in range(self.n):
			self.__leftFace[self.n-1][i] = self.__backFace[self.n-1][i]
		# Move right to back
		for i in range(self.n):
			self.__backFace[self.n-1][i] = self.__rightFace[self.n-1][i]
		# Restore front to right
		for i in range(self.n):
			self.__rightFace[self.n-1][i] = tempArray[i]

		if timed:
			self.performMove(Cube.Bottom)

	def D_(self, timed = True):#	<-
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.D_(False)
		>>> cube.faces()
		([[0, 1, 2], [3, 4, 5], [6, 7, 8]], [[9, 10, 11], [12, 13, 14], [24, 25, 26]], [[18, 19, 20], [21, 22, 23], [33, 34, 35]], [[27, 28, 29], [30, 31, 32], [42, 43, 44]], [[36, 37, 38], [39, 40, 41], [15, 16, 17]], [[47, 50, 53], [46, 49, 52], [45, 48, 51]])
		"""
		self.rotateFaceArray_(self.__bottomFace)

		# Save front
		tempArray = deepcopy(self.__frontFace[self.n-1])
		# Move right to front
		for i in range(self.n):
			self.__frontFace[self.n-1][i] = self.__rightFace[self.n-1][i]
		# Move back to right
		for i in range(self.n):
			self.__rightFace[self.n-1][i] = self.__backFace[self.n-1][i]
		# Move left to back
		for i in range(self.n):
			self.__backFace[self.n-1][i] = self.__leftFace[self.n-1][i]
		# Restore front to left
		for i in range(self.n):
			self.__leftFace[self.n-1][i] = tempArray[i]

		if timed:
			self.performMove(Cube.Bottom_)

	# Middle Row (Horizontal) ->
	def M(self, timed = True):
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.M(False)
		>>> cube.faces()
		([[0, 1, 2], [3, 4, 5], [6, 7, 8]], [[9, 10, 11], [39, 40, 41], [15, 16, 17]], [[18, 19, 20], [12, 13, 14], [24, 25, 26]], [[27, 28, 29], [21, 22, 23], [33, 34, 35]], [[36, 37, 38], [30, 31, 32], [42, 43, 44]], [[45, 46, 47], [48, 49, 50], [51, 52, 53]])
		"""
		# Save front
		tempArray = deepcopy(self.__frontFace[int(self.n / 2)])
		# Move left to front
		for i in range(self.n):
			self.__frontFace[int(self.n / 2)][i] = self.__leftFace[int(self.n / 2)][i]
		# Move back to left
		for i in range(self.n):
			self.__leftFace[int(self.n / 2)][i] = self.__backFace[int(self.n / 2)][i]
		# Move right to back
		for i in range(self.n):
			self.__backFace[int(self.n / 2)][i] = self.__rightFace[int(self.n / 2)][i]
		# Restore front to right
		for i in range(self.n):
			self.__rightFace[int(self.n / 2)][i] = tempArray[i]

		if timed:
			self.performMove(Cube.Middle)

	def M_(self, timed = True):#	<-
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.M_(False)
		>>> cube.faces()
		([[0, 1, 2], [3, 4, 5], [6, 7, 8]], [[9, 10, 11], [21, 22, 23], [15, 16, 17]], [[18, 19, 20], [30, 31, 32], [24, 25, 26]], [[27, 28, 29], [39, 40, 41], [33, 34, 35]], [[36, 37, 38], [12, 13, 14], [42, 43, 44]], [[45, 46, 47], [48, 49, 50], [51, 52, 53]])
		"""
		# Save front
		tempArray = deepcopy(self.__frontFace[int(self.n / 2)])
		# Move right to front
		for i in range(self.n):
			self.__frontFace[int(self.n / 2)][i] = self.__rightFace[int(self.n / 2)][i]
		# Move back to right
		for i in range(self.n):
			self.__rightFace[int(self.n / 2)][i] = self.__backFace[int(self.n / 2)][i]
		# Move left to back
		for i in range(self.n):
			self.__backFace[int(self.n / 2)][i] = self.__leftFace[int(self.n / 2)][i]
		# Restore front to left
		for i in range(self.n):
			self.__leftFace[int(self.n / 2)][i] = tempArray[i]

		if timed:
			self.performMove(Cube.Middle_)

	# Center Row (Vertical) 		^
	def C(self, timed = True):#		|
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.C(False)
		>>> cube.faces()
		([[0, 10, 2], [3, 13, 5], [6, 16, 8]], [[9, 46, 11], [12, 49, 14], [15, 52, 17]], [[18, 19, 20], [21, 22, 23], [24, 25, 26]], [[27, 7, 29], [30, 4, 32], [33, 1, 35]], [[36, 37, 38], [39, 40, 41], [42, 43, 44]], [[45, 34, 47], [48, 31, 50], [51, 28, 53]])
		"""
		# Save top
		tempArray = []
		for i in range(self.n):
			tempArray.append(self.__topFace[i][int(self.n / 2)])
		# Move front to top
		for i in range(self.n):
			self.__topFace[i][int(self.n / 2)] = self.__frontFace[i][int(self.n / 2)]
		# Move bottom to front
		for i in range(self.n):
			self.__frontFace[i][int(self.n / 2)] = self.__bottomFace[i][int(self.n / 2)]
		# Move back to bottom
		for i in range(self.n):
			self.__bottomFace[i][int(self.n / 2)] = self.__backFace[self.n-1 - i][int(self.n / 2)]
		# Restore top to back
		for i in range(self.n):
			self.__backFace[self.n-1 - i][int(self.n / 2)] = tempArray[i]

		if timed:
			self.performMove(Cube.Center)

	#								|
	def C_(self, timed = True):#	v
		"""
		>>> cube = Cube(3)
		>>> faces = cube.faces()
		>>> top = faces[0]
		>>> front = faces[1]
		>>> right = faces[2]
		>>> back = faces[3]
		>>> left = faces[4]
		>>> bottom = faces[5]
		>>> top[0] = [0, 1, 2]
		>>> top[1] = [3, 4, 5]
		>>> top[2] = [6, 7, 8]
		>>> front[0] = [9, 10, 11]
		>>> front[1] = [12, 13, 14]
		>>> front[2] = [15, 16, 17]
		>>> right[0] = [18, 19, 20]
		>>> right[1] = [21, 22, 23]
		>>> right[2] = [24, 25, 26]
		>>> back[0] = [27, 28, 29]
		>>> back[1] = [30, 31, 32]
		>>> back[2] = [33, 34, 35]
		>>> left[0] = [36, 37, 38]
		>>> left[1] = [39, 40, 41]
		>>> left[2] = [42, 43, 44]
		>>> bottom[0] = [45, 46, 47]
		>>> bottom[1] = [48, 49, 50]
		>>> bottom[2] = [51, 52, 53]
		>>> cube.C_(False)
		>>> cube.faces()
		([[0, 34, 2], [3, 31, 5], [6, 28, 8]], [[9, 1, 11], [12, 4, 14], [15, 7, 17]], [[18, 19, 20], [21, 22, 23], [24, 25, 26]], [[27, 52, 29], [30, 49, 32], [33, 46, 35]], [[36, 37, 38], [39, 40, 41], [42, 43, 44]], [[45, 10, 47], [48, 13, 50], [51, 16, 53]])
		"""
		# Save top
		tempArray = []
		for i in range(self.n):
			tempArray.append(self.__topFace[i][int(self.n / 2)])
		# Move back to top
		for i in range(self.n):
			self.__topFace[i][int(self.n / 2)] = self.__backFace[self.n-1 - i][int(self.n / 2)]
		# Move bottom to back
		for i in range(self.n):
			self.__backFace[self.n-1 - i][int(self.n / 2)] = self.__bottomFace[i][int(self.n / 2)]
		# Move front to bottom
		for i in range(self.n):
			self.__bottomFace[i][int(self.n / 2)] = self.__frontFace[i][int(self.n / 2)]
		# Restore top to front
		for i in range(self.n):
			self.__frontFace[i][int(self.n / 2)] = tempArray[i]

		if timed:
			self.performMove(Cube.Center_)
