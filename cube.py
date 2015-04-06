"""
New New Cube
"""
from cubie import Cubie
from random import randint
from helpers import Point
import cubemoverenderer
import button
from copy import deepcopy
from cubetimer import CubeTimer
import pygame
from pygame.mixer import Sound

W = Cubie.White
R = Cubie.Red
O = Cubie.Orange
G = Cubie.Green
B = Cubie.Blue
Y = Cubie.Yellow
C = Cubie.Clear

class Cube:
	"""
	A NxNxN Cube class
	"""
	Top = 1
	Bottom = -2
	Left = -3
	Right = 4
	Front = 5
	Middle = -6
	Center = 7
	Back = 8

	Top_ = -1
	Bottom_ = 2
	Left_ = 3
	Right_ = -4
	Front_ = -5
	Middle_ = 6
	Center_ = -7
	Back_ = -8

	TurnRRR = 11
	TurnRRR_=-11
	TurnUUU = 12
	TurnUUU_=-12

	Moves = None

	def __init__(self, N):
		# Populate if it doesn't already exist
		if Cube.Moves is None:
			Cube.Moves = {
				Cube.Top: Cube.U,
				Cube.Bottom: Cube.D,
				Cube.Left: Cube.L,
				Cube.Right: Cube.R,
				Cube.Front: Cube.F,
				Cube.Middle: Cube.M,
				Cube.Center: Cube.C,

				Cube.Top_: Cube.U_,
				Cube.Bottom_: Cube.D_,
				Cube.Left_: Cube.L_,
				Cube.Right_: Cube.R_,
				Cube.Front_: Cube.F_,
				Cube.Middle_: Cube.M_,
				Cube.Center_: Cube.C_,

				Cube.TurnRRR: Cube.RRR,
				Cube.TurnRRR_:Cube.RRR_,

				Cube.TurnUUU: Cube.UUU,
				Cube.TurnUUU_:Cube.UUU_
			}

		self.moveQueue = []
		self.ready = False

		self.moveHistory = []

		self.wasUnsolved = False

		self.cubeTimer = CubeTimer()

		self.N = N
		# Create the cubies for a N-Cube
		#
		# A 3D array - each N long.
		#
		# The Outside Array is the vertical layer - 0 is top, N is bottom
		# The Middle Array is the Row - 0 is front, N is back
		# The Inside Array is the column - 0 is left, N is right
		self.cubies = []
		# Each cubie is 1x1x1 in size centered at the point given
		startX = -(N - 1) / 2
		startY = -(N - 1) / 2
		startZ = -(N - 1) / 2
		for z in range(N):
			self.cubies.append([])
			for y in range(N):
				self.cubies[z].append([])
				for x in range(N):
					# Only add a cubie if its on the outside
					if x == 0 or y == 0 or z == 0 or x == N-1 or y == N-1 or z == N-1:
						topColor = W if z == 0 else C
						bottomColor = Y if z == N-1 else C
						leftColor = G if x == 0 else C
						rightColor = B if x == N-1 else C
						frontColor = R if y == 0 else C
						backColor = O if y == N-1 else C
						self.cubies[z][y].append(Cubie([topColor, frontColor, rightColor, backColor, leftColor, bottomColor], Point(startX + x, startY + y, startZ + z)))
					else:
						self.cubies[z][y].append(None)

	def generateButtons(self, x, y):
		w = cubemoverenderer.CubeMoveRenderer.size(self.N)
		num = int(self.N / 2)

		buttons = []

		for i in range(num):
			# Upwards
			buttons.append(button.MoveButton(x + w*(i+1), y, self, Cube.Left_, i))
			buttons.append(button.MoveButton(x + w*(self.N-i), y, self, Cube.Right, i))
			# Downwards
			buttons.append(button.MoveButton(x + w*(i+1), y + w*(self.N+1), self, Cube.Left, i))
			buttons.append(button.MoveButton(x + w*(self.N-i), y + w*(self.N+1), self, Cube.Right_, i))
			# Leftwards
			buttons.append(button.MoveButton(x, y + w*(i+1), self, Cube.Top, i))
			buttons.append(button.MoveButton(x, y + w*(self.N-i), self, Cube.Bottom_, i))
			# Rightwards
			buttons.append(button.MoveButton(x + w*(self.N+1), y + w*(i+1), self, Cube.Top_, i))
			buttons.append(button.MoveButton(x + w*(self.N+1), y + w*(self.N-i), self, Cube.Bottom, i))

		if int(self.N / 2) != self.N / 2:
			# Upwards
			buttons.append(button.MoveButton(x + w*(num+1), y, self, Cube.Center, 0))
			# Downwards
			buttons.append(button.MoveButton(x + w*(num+1), y + w*(self.N+1), self, Cube.Center_, 0))
			# Leftwards
			buttons.append(button.MoveButton(x, y + w*(num+1), self, Cube.Middle_, 0))
			# Rightwards
			buttons.append(button.MoveButton(x + w*(self.N+1), y + w*(num+1), self, Cube.Middle, 0))

		# FrontFaceBoutons
		buttons.append(button.MoveButton(x, y, self, Cube.Front_, 0))
		buttons.append(button.MoveButton(x + w*(self.N+1), y, self, Cube.Front, 0))

		return buttons

	def update(self):
		doneUpdate = True
		for zLayer in self.cubies:
			for yLayer in zLayer:
				for cubie in yLayer:
					if not cubie is None:
						if not cubie.update():
							doneUpdate = False
		if doneUpdate and len(self.moveQueue) > 0:
			doneUpdate = False
			move, offsets, animate = self.moveQueue.pop(0)
			move(offsets, animate)
		self.ready = doneUpdate

		if self.isSolved():
			if self.wasUnsolved:
				self.wasUnsolved = False
				self.cubeTimer.endTime = pygame.time.get_ticks()
				# Play the VICTORY SOUND!!!
				winSound = Sound(file = "assets/audio/WIN.wav")
				winSound.play()
				pygame.mixer.music.fadeout(1)
		else:
			self.wasUnsolved = True

		return doneUpdate

	def isSolved(self):
		frontColors = []
		backColors = []
		leftColors = []
		rightColors = []
		topColors = []
		bottomColors = []

		# Collect the colors
		for zLayer in self.cubies:
			for yLayer in zLayer:
				for cubie in yLayer:
					if cubie is None:
						continue
					frontColors.append(cubie.frontColor())
					backColors.append(cubie.backColor())
					leftColors.append(cubie.leftColor())
					rightColors.append(cubie.rightColor())
					topColors.append(cubie.topColor())
					bottomColors.append(cubie.bottomColor())

		# Check to make sure the cube is solved
		activeColor = Cubie.Clear
		for color in frontColors:
			if activeColor == Cubie.Clear:
				activeColor = color
			elif activeColor != color and color != Cubie.Clear:
				return False
		activeColor = Cubie.Clear
		for color in backColors:
			if activeColor == Cubie.Clear:
				activeColor = color
			elif activeColor != color and color != Cubie.Clear:
				return False
		activeColor = Cubie.Clear
		for color in leftColors:
			if activeColor == Cubie.Clear:
				activeColor = color
			elif activeColor != color and color != Cubie.Clear:
				return False

		activeColor = Cubie.Clear
		for color in rightColors:
			if activeColor == Cubie.Clear:
				activeColor = color
			elif activeColor != color and color != Cubie.Clear:
				return False
		activeColor = Cubie.Clear
		for color in topColors:
			if activeColor == Cubie.Clear:
				activeColor = color
			elif activeColor != color and color != Cubie.Clear:
				return False
		activeColor = Cubie.Clear
		for color in bottomColors:
			if activeColor == Cubie.Clear:
				activeColor = color
			elif activeColor != color and color != Cubie.Clear:
				return False
		return True

	def randomize(self):
		"""
		Randomly applies a single move to the cube
		"""
		operation = randint(0,13)
		offset = randint(0, self.N-1)
		if operation == 0:
			self.U(offset, True, False)
		elif operation == 1:
			self.U_(offset, True, False)
		elif operation == 2:
			self.D(offset, True, False)
		elif operation == 3:
			self.D_(offset, True, False)
		elif operation == 4:
			self.L(offset, True, False)
		elif operation == 5:
			self.L_(offset, True, False)
		elif operation == 6:
			self.R(offset, True, False)
		elif operation == 7:
			self.R_(offset, True, False)
		elif operation == 8:
			self.F(offset, True, False)
		elif operation == 9:
			self.F_(offset, True, False)
		elif operation == 10:
			self.M(int(offset / 2), True, False)
		elif operation == 11:
			self.M_(int(offset / 2), True, False)
		elif operation == 12:
			self.C(int(offset / 2), True, False)
		elif operation == 13:
			self.C_(int(offset / 2), True, False)

	def performMove(self, moveData):
		self.moveHistory.append(moveData)

		if self.cubeTimer.endTime:
			if not self.isSolved():
				self.moveHistory = []
				self.cubeTimer.startTime = None
				self.cubeTimer.endTime = None

		# If its the first move start the timer
		if len(self.moveHistory) == 1:
			self.cubeTimer.startTime = pygame.time.get_ticks()
			self.cubeTimer.endTime = None

			pygame.mixer.music.load("assets/audio/BGM.wav")
			pygame.mixer.music.play(loops=-1)

	def U(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__U, offsets, animate))
		if timed:
			self.performMove((self.Top, offsets))

	def U_(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__U_, offsets, animate))
		if timed:
			self.performMove((self.Top_, offsets))

	def D(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__D, offsets, animate))
		if timed:
			self.performMove((self.Bottom, offsets))

	def D_(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__D_, offsets, animate))
		if timed:
			self.performMove((self.Bottom_, offsets))

	def L(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__L, offsets, animate))
		if timed:
			self.performMove((self.Left, offsets))

	def L_(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__L_, offsets, animate))
		if timed:
			self.performMove((self.Left_, offsets))

	def R(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__R, offsets, animate))
		if timed:
			self.performMove((self.Right, offsets))

	def R_(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__R_, offsets, animate))
		if timed:
			self.performMove((self.Right_, offsets))

	def F(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__F, offsets, animate))
		if timed:
			self.performMove((self.Front, offsets))

	def F_(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__F_, offsets, animate))
		if timed:
			self.performMove((self.Front_, offsets))

	def B(self, offsets, animate=True, timed=True):
		self.UUU_(animate, timed)
		self.R(offsets, animate, timed)
		self.UUU(animate, timed)

	def B_(self, offsets, animate=True, timed=True):
		self.UUU_(animate, timed)
		self.R_(offsets, animate, timed)
		self.UUU(animate, timed)

	def M(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__M, offsets, animate))
		if timed:
			self.performMove((self.Middle, offsets))

	def M_(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__M_, offsets, animate))
		if timed:
			self.performMove((self.Middle_, offsets))

	def C(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__C, offsets, animate))
		if timed:
			self.performMove((self.Center, offsets))

	def C_(self, offsets, animate=True, timed=True):
		self.moveQueue.append((self.__C_, offsets, animate))
		if timed:
			self.performMove((self.Center_, offsets))

	def UUU(self, animate=True, timed=True):
		self.moveQueue.append((self.__UUU, 0, animate))
		if timed:
			self.performMove((self.TurnUUU, 0))

	def UUU_(self, animate=True, timed=True):
		self.moveQueue.append((self.__UUU_, 0, animate))
		if timed:
			self.performMove((self.TurnUUU_, 0))

	def RRR(self, animate=True, timed=True):
		self.moveQueue.append((self.__RRR, 0, animate))
		if timed:
			self.performMove((self.TurnRRR, 0))

	def RRR_(self, animate=True, timed=True):
		self.moveQueue.append((self.__RRR_, 0, animate))
		if timed:
			self.performMove((self.TurnRRR_, 0))

	def __U(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for y in range(self.N):
				for x in range(self.N):
					if not self.cubies[offset][y][x] is None:
						self.cubies[offset][y][x] = cubiesCopy[offset][x][self.N-1-y]
						self.cubies[offset][y][x].rotateZ(-90, animate)

	def __U_(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for y in range(self.N):
				for x in range(self.N):
					if not self.cubies[offset][y][x] is None:
						self.cubies[offset][y][x] = cubiesCopy[offset][self.N-1-x][y]
						self.cubies[offset][y][x].rotateZ(90, animate)

	def __D(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for y in range(self.N):
				for x in range(self.N):
					if not self.cubies[self.N-1-offset][y][x] is None:
						self.cubies[self.N-1-offset][y][x] = cubiesCopy[self.N-1-offset][self.N-1-x][y]
						self.cubies[self.N-1-offset][y][x].rotateZ(90, animate)

	def __D_(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for y in range(self.N):
				for x in range(self.N):
					if not self.cubies[self.N-1-offset][y][x] is None:
						self.cubies[self.N-1-offset][y][x] = cubiesCopy[self.N-1-offset][x][self.N-1-y]
						self.cubies[self.N-1-offset][y][x].rotateZ(-90, animate)

	def __L(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for z in range(self.N):
				for y in range(self.N):
					if not self.cubies[z][y][offset] is None:
						self.cubies[z][y][offset] = cubiesCopy[y][self.N-1-z][offset]
						self.cubies[z][y][offset].rotateX(-90, animate)

	def __L_(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for z in range(self.N):
				for y in range(self.N):
					if not self.cubies[z][y][offset] is None:
						self.cubies[z][y][offset] = cubiesCopy[self.N-1-y][z][offset]
						self.cubies[z][y][offset].rotateX(90, animate)

	def __R(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for z in range(self.N):
				for y in range(self.N):
					if not self.cubies[z][y][self.N-1-offset] is None:
						self.cubies[z][y][self.N-1-offset] = cubiesCopy[self.N-1-y][z][self.N-1-offset]
						self.cubies[z][y][self.N-1-offset].rotateX(90, animate)

	def __R_(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for z in range(self.N):
				for y in range(self.N):
					if not self.cubies[z][y][self.N-1-offset] is None:
						self.cubies[z][y][self.N-1-offset] = cubiesCopy[y][self.N-1-z][self.N-1-offset]
						self.cubies[z][y][self.N-1-offset].rotateX(-90, animate)

	def __F(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for z in range(self.N):
				for x in range(self.N):
					if not self.cubies[z][offset][x] is None:
						self.cubies[z][offset][x] = cubiesCopy[self.N-1-x][offset][z]
						self.cubies[z][offset][x].rotateY(-90, animate)

	def __F_(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for z in range(self.N):
				for x in range(self.N):
					if not self.cubies[z][offset][x] is None:
						self.cubies[z][offset][x] = cubiesCopy[x][offset][self.N-1-z]
						self.cubies[z][offset][x].rotateY(90, animate)

	def __M(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		newOffSets = []
		if self.N % 2 == 0:
			for i in offsets:
				newOffSets.append(int(self.N / 2) - 1 - i)
				newOffSets.append(int(self.N / 2) + 0 + i)
		else:
			for i in offsets:
				newOffSets.append(int(self.N / 2) - i)
				newOffSets.append(int(self.N / 2) + i)
		offsets = set(newOffSets)
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for y in range(self.N):
				for x in range(self.N):
					if not self.cubies[self.N-1-offset][y][x] is None:
						self.cubies[self.N-1-offset][y][x] = cubiesCopy[self.N-1-offset][self.N-1-x][y]
						self.cubies[self.N-1-offset][y][x].rotateZ(90, animate)

	def __M_(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		newOffSets = []
		if self.N % 2 == 0:
			for i in offsets:
				newOffSets.append(int(self.N / 2) - 1 - i)
				newOffSets.append(int(self.N / 2) + 0 + i)
		else:
			for i in offsets:
				newOffSets.append(int(self.N / 2) - i)
				newOffSets.append(int(self.N / 2) + i)
		offsets = set(newOffSets)
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for y in range(self.N):
				for x in range(self.N):
					if not self.cubies[self.N-1-offset][y][x] is None:
						self.cubies[self.N-1-offset][y][x] = cubiesCopy[self.N-1-offset][x][self.N-1-y]
						self.cubies[self.N-1-offset][y][x].rotateZ(-90, animate)

	def __C(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		newOffSets = []
		if self.N % 2 == 0:
			for i in offsets:
				newOffSets.append(int(self.N / 2) - 1 - i)
				newOffSets.append(int(self.N / 2) + 0 + i)
		else:
			for i in offsets:
				newOffSets.append(int(self.N / 2) - i)
				newOffSets.append(int(self.N / 2) + i)
		offsets = set(newOffSets)
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for z in range(self.N):
				for y in range(self.N):
					if not self.cubies[z][y][self.N-1-offset] is None:
						self.cubies[z][y][self.N-1-offset] = cubiesCopy[self.N-1-y][z][self.N-1-offset]
						self.cubies[z][y][self.N-1-offset].rotateX(90, animate)

	def __C_(self, offsets, animate=True):
		try:
			a = offsets[0]
		except:
			offsets = [offsets]
		newOffSets = []
		if self.N % 2 == 0:
			for i in offsets:
				newOffSets.append(int(self.N / 2) - 1 - i)
				newOffSets.append(int(self.N / 2) + 0 + i)
		else:
			for i in offsets:
				newOffSets.append(int(self.N / 2) - i)
				newOffSets.append(int(self.N / 2) + i)
		offsets = set(newOffSets)
		cubiesCopy = deepcopy(self.cubies)
		for offset in offsets:
			for z in range(self.N):
				for y in range(self.N):
					if not self.cubies[z][y][self.N-1-offset] is None:
						self.cubies[z][y][self.N-1-offset] = cubiesCopy[y][self.N-1-z][self.N-1-offset]
						self.cubies[z][y][self.N-1-offset].rotateX(-90, animate)

	def __UUU(self, offsets, animate=True):
		offsets = [i for i in range(self.N)]
		self.__U(offsets, animate)

	def __UUU_(self, offsets, animate=True):
		offsets = [i for i in range(self.N)]
		self.__U_(offsets, animate)

	def __RRR(self, offsets, animate=True):
		offsets = [i for i in range(self.N)]
		self.__R(offsets, animate)

	def __RRR_(self, offsets, animate=True):
		offsets = [i for i in range(self.N)]
		self.__R_(offsets, animate)
