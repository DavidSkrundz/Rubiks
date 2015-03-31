"""
New New Cube
"""
from cubie import Cubie
from random import randint
from helpers import Point
import cubemoverenderer
import button
from copy import deepcopy

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

	Top_ = -1
	Bottom_ = 2
	Left_ = 3
	Right_ = -4
	Front_ = -5
	Middle_ = 6
	Center_ = -7

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

		self.N = N
		# Create the cubies for a N-Cube
		#
		# A 3D array - each N long.
		#
		# The Outside Array is the vertical layer - 0 is top, N is bottom
		# The Middle Array is the Row - 0 is top, N is bottom
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
		if operation == 0:
			self.U()
		elif operation == 1:
			self.U_()
		elif operation == 2:
			self.D()
		elif operation == 3:
			self.D_()
		elif operation == 4:
			self.L()
		elif operation == 5:
			self.L_()
		elif operation == 6:
			self.R()
		elif operation == 7:
			self.R_()
		elif operation == 8:
			self.F()
		elif operation == 9:
			self.F_()
		elif operation == 10:
			self.M()
		elif operation == 11:
			self.M_()
		elif operation == 12:
			self.C()
		elif operation == 13:
			self.C_()

	def U(self, offsets, animate=True):
		self.moveQueue.append((self.__U, offsets, animate))

	def U_(self, offsets, animate=True):
		self.moveQueue.append((self.__U_, offsets, animate))

	def D(self, offsets, animate=True):
		self.moveQueue.append((self.__D, offsets, animate))

	def D_(self, offsets, animate=True):
		self.moveQueue.append((self.__D_, offsets, animate))

	def L(self, offsets, animate=True):
		self.moveQueue.append((self.__L, offsets, animate))

	def L_(self, offsets, animate=True):
		self.moveQueue.append((self.__L_, offsets, animate))

	def R(self, offsets, animate=True):
		self.moveQueue.append((self.__R, offsets, animate))

	def R_(self, offsets, animate=True):
		self.moveQueue.append((self.__R_, offsets, animate))

	def F(self, offsets, animate=True):
		self.moveQueue.append((self.__F, offsets, animate))

	def F_(self, offsets, animate=True):
		self.moveQueue.append((self.__F_, offsets, animate))

	def M(self, offsets, animate=True):
		self.moveQueue.append((self.__M, offsets, animate))

	def M_(self, offsets, animate=True):
		self.moveQueue.append((self.__M_, offsets, animate))

	def C(self, offsets, animate=True):
		self.moveQueue.append((self.__C, offsets, animate))

	def C_(self, offsets, animate=True):
		self.moveQueue.append((self.__C_, offsets, animate))

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
						if animate:
							self.cubies[offset][y][x].rotateZ(-90, animate)
						else:
							self.cubies[offset][y][x].rotateZ_(-90, animate)

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
						if animate:
							self.cubies[offset][y][x].rotateZ(90, animate)
						else:
							self.cubies[offset][y][x].rotateZ_(90, animate)

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
						if animate:
							self.cubies[self.N-1-offset][y][x].rotateZ(90, animate)
						else:
							self.cubies[self.N-1-offset][y][x].rotateZ_(90, animate)

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
						if animate:
							self.cubies[self.N-1-offset][y][x].rotateZ(-90, animate)
						else:
							self.cubies[self.N-1-offset][y][x].rotateZ_(-90, animate)

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
						if animate:
							self.cubies[z][y][offset].rotateX(-90, animate)
						else:
							self.cubies[z][y][offset].rotateX_(-90, animate)

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
						if animate:
							self.cubies[z][y][offset].rotateX(90, animate)
						else:
							self.cubies[z][y][offset].rotateX_(90, animate)

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
						if animate:
							self.cubies[z][y][self.N-1-offset].rotateX(90, animate)
						else:
							self.cubies[z][y][self.N-1-offset].rotateX_(90, animate)

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
						if animate:
							self.cubies[z][y][self.N-1-offset].rotateX(-90, animate)
						else:
							self.cubies[z][y][self.N-1-offset].rotateX_(-90, animate)

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
						if animate:
							self.cubies[z][offset][x].rotateY(-90, animate)
						else:
							self.cubies[z][offset][x].rotateY_(-90, animate)

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
						if animate:
							self.cubies[z][offset][x].rotateY(90, animate)
						else:
							self.cubies[z][offset][x].rotateY_(90, animate)

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
						if animate:
							self.cubies[self.N-1-offset][y][x].rotateZ(90, animate)
						else:
							self.cubies[self.N-1-offset][y][x].rotateZ_(90, animate)




	def UUU(self, animate=True):
		self.U_(animate)
		self.M(animate)
		self.D(animate)

	def UUU_(self, animate=True):
		self.U(animate)
		self.M_(animate)
		self.D_(animate)

	def RRR(self, animate=True):
		self.R(animate)
		self.C(animate)
		self.L_(animate)

	def RRR_(self, animate=True):
		self.R_(animate)
		self.C_(animate)
		self.L(animate)
