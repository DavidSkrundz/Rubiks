"""
New New Cube
"""
from cubie import Cubie
from random import randint
from helpers import Point

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
	Bottom = 2
	Left = 3
	Right = 4
	Front = 5
	Middle = 6
	Center = 7

	Top_ = -1
	Bottom_ = -2
	Left_ = -3
	Right_ = -4
	Front_ = -5
	Middle_ = -6
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







	def isSolved(self):
		frontColors = []
		backColors = []
		leftColors = []
		rightColors = []
		topColors = []
		bottomColors = []

		# Collect the colors
		for cubie in self.cubies:
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

	def update(self):
		doneUpdate = True
		for cubie in self.cubies:
			if not cubie.update():
				doneUpdate = False
		return doneUpdate

	def U_(self, animate=True):
		tempCubie = self.cubies[0]
		self.cubies[0] = self.cubies[6]
		self.cubies[6] = self.cubies[8]
		self.cubies[8] = self.cubies[2]
		self.cubies[2] = tempCubie
		tempCubie = self.cubies[1]
		self.cubies[1] = self.cubies[3]
		self.cubies[3] = self.cubies[7]
		self.cubies[7] = self.cubies[5]
		self.cubies[5] = tempCubie

		for i in [0,1,2,3,4,5,6,7,8]:
			if animate:
				self.cubies[i].rotateZ(-90, animate)
			else:
				self.cubies[i].rotateZ_(-90, animate)

	def U(self, animate=True):
		tempCubie = self.cubies[0]
		self.cubies[0] = self.cubies[2]
		self.cubies[2] = self.cubies[8]
		self.cubies[8] = self.cubies[6]
		self.cubies[6] = tempCubie
		tempCubie = self.cubies[1]
		self.cubies[1] = self.cubies[5]
		self.cubies[5] = self.cubies[7]
		self.cubies[7] = self.cubies[3]
		self.cubies[3] = tempCubie

		for i in [0,1,2,3,4,5,6,7,8]:
			if animate:
				self.cubies[i].rotateZ(90, animate)
			else:
				self.cubies[i].rotateZ_(90, animate)

	def F_(self, animate=True):
		tempCubie = self.cubies[6]
		self.cubies[6] = self.cubies[17]
		self.cubies[17] = self.cubies[19]
		self.cubies[19] = self.cubies[8]
		self.cubies[8] = tempCubie
		tempCubie = self.cubies[7]
		self.cubies[7] = self.cubies[9]
		self.cubies[9] = self.cubies[18]
		self.cubies[18] = self.cubies[11]
		self.cubies[11] = tempCubie

		for i in [6,7,8,9,10,11,17,18,19]:
			if animate:
				self.cubies[i].rotateY(90, animate)
			else:
				self.cubies[i].rotateY_(90, animate)

	def F(self, animate=True):
		tempCubie = self.cubies[6]
		self.cubies[6] = self.cubies[8]
		self.cubies[8] = self.cubies[19]
		self.cubies[19] = self.cubies[17]
		self.cubies[17] = tempCubie
		tempCubie = self.cubies[7]
		self.cubies[7] = self.cubies[11]
		self.cubies[11] = self.cubies[18]
		self.cubies[18] = self.cubies[9]
		self.cubies[9] = tempCubie

		for i in [6,7,8,9,10,11,17,18,19]:
			if animate:
				self.cubies[i].rotateY(-90, animate)
			else:
				self.cubies[i].rotateY_(-90, animate)

	def R_(self, animate=True):
		tempCubie = self.cubies[0]
		self.cubies[0] = self.cubies[23]
		self.cubies[23] = self.cubies[17]
		self.cubies[17] = self.cubies[6]
		self.cubies[6] = tempCubie
		tempCubie = self.cubies[3]
		self.cubies[3] = self.cubies[15]
		self.cubies[15] = self.cubies[20]
		self.cubies[20] = self.cubies[9]
		self.cubies[9] = tempCubie

		for i in [0,3,6,9,12,15,16,17,20,23]:
			if animate:
				self.cubies[i].rotateX(90, animate)
			else:
				self.cubies[i].rotateX_(90, animate)

	def R(self, animate=True):
		tempCubie = self.cubies[0]
		self.cubies[0] = self.cubies[6]
		self.cubies[6] = self.cubies[17]
		self.cubies[17] = self.cubies[23]
		self.cubies[23] = tempCubie
		tempCubie = self.cubies[3]
		self.cubies[3] = self.cubies[9]
		self.cubies[9] = self.cubies[20]
		self.cubies[20] = self.cubies[15]
		self.cubies[15] = tempCubie

		for i in [0,3,6,9,12,15,16,17,20,23]:
			if animate:
				self.cubies[i].rotateX(-90, animate)
			else:
				self.cubies[i].rotateX_(-90, animate)

	def L_(self, animate=True):
		tempCubie = self.cubies[8]
		self.cubies[8] = self.cubies[19]
		self.cubies[19] = self.cubies[25]
		self.cubies[25] = self.cubies[2]
		self.cubies[2] = tempCubie
		tempCubie = self.cubies[5]
		self.cubies[5] = self.cubies[11]
		self.cubies[11] = self.cubies[22]
		self.cubies[22] = self.cubies[13]
		self.cubies[13] = tempCubie

		for i in [2,5,8,11,13,19,22,25]:
			if animate:
				self.cubies[i].rotateX(-90, animate)
			else:
				self.cubies[i].rotateX_(-90, animate)

	def L(self, animate=True):
		tempCubie = self.cubies[8]
		self.cubies[8] = self.cubies[2]
		self.cubies[2] = self.cubies[25]
		self.cubies[25] = self.cubies[19]
		self.cubies[19] = tempCubie
		tempCubie = self.cubies[5]
		self.cubies[5] = self.cubies[13]
		self.cubies[13] = self.cubies[22]
		self.cubies[22] = self.cubies[11]
		self.cubies[11] = tempCubie

		for i in [2,5,8,11,13,19,22,25]:
			if animate:
				self.cubies[i].rotateX(90, animate)
			else:
				self.cubies[i].rotateX_(90, animate)

	def D_(self, animate=True):
		tempCubie = self.cubies[17]
		self.cubies[17] = self.cubies[23]
		self.cubies[23] = self.cubies[25]
		self.cubies[25] = self.cubies[19]
		self.cubies[19] = tempCubie
		tempCubie = self.cubies[18]
		self.cubies[18] = self.cubies[20]
		self.cubies[20] = self.cubies[24]
		self.cubies[24] = self.cubies[22]
		self.cubies[22] = tempCubie

		for i in [17,18,19,20,21,22,23,24,25]:
			if animate:
				self.cubies[i].rotateZ(90, animate)
			else:
				self.cubies[i].rotateZ_(90, animate)

	def D(self, animate=True):
		tempCubie = self.cubies[17]
		self.cubies[17] = self.cubies[19]
		self.cubies[19] = self.cubies[25]
		self.cubies[25] = self.cubies[23]
		self.cubies[23] = tempCubie
		tempCubie = self.cubies[18]
		self.cubies[18] = self.cubies[22]
		self.cubies[22] = self.cubies[24]
		self.cubies[24] = self.cubies[20]
		self.cubies[20] = tempCubie

		for i in [17,18,19,20,21,22,23,24,25]:
			if animate:
				self.cubies[i].rotateZ(-90, animate)
			else:
				self.cubies[i].rotateZ_(-90, animate)

	def M_(self, animate=True):
		tempCubie = self.cubies[9]
		self.cubies[9] = self.cubies[15]
		self.cubies[15] = self.cubies[13]
		self.cubies[13] = self.cubies[11]
		self.cubies[11] = tempCubie
		tempCubie = self.cubies[10]
		self.cubies[10] = self.cubies[16]
		self.cubies[16] = self.cubies[14]
		self.cubies[14] = self.cubies[12]
		self.cubies[12] = tempCubie

		for i in [9,10,11,12,13,14,15,16]:
			if animate:
				self.cubies[i].rotateZ(90, animate)
			else:
				self.cubies[i].rotateZ_(90, animate)

	def M(self, animate=True):
		tempCubie = self.cubies[9]
		self.cubies[9] = self.cubies[11]
		self.cubies[11] = self.cubies[13]
		self.cubies[13] = self.cubies[15]
		self.cubies[15] = tempCubie
		tempCubie = self.cubies[10]
		self.cubies[10] = self.cubies[12]
		self.cubies[12] = self.cubies[14]
		self.cubies[14] = self.cubies[16]
		self.cubies[16] = tempCubie

		for i in [9,10,11,12,13,14,15,16]:
			if animate:
				self.cubies[i].rotateZ(-90, animate)
			else:
				self.cubies[i].rotateZ_(-90, animate)

	def C(self, animate=True):
		tempCubie = self.cubies[1]
		self.cubies[1] = self.cubies[7]
		self.cubies[7] = self.cubies[18]
		self.cubies[18] = self.cubies[24]
		self.cubies[24] = tempCubie
		tempCubie = self.cubies[4]
		self.cubies[4] = self.cubies[10]
		self.cubies[10] = self.cubies[21]
		self.cubies[21] = self.cubies[14]
		self.cubies[14] = tempCubie

		for i in [1,4,7,10,14,18,21,24]:
			if animate:
				self.cubies[i].rotateX(-90, animate)
			else:
				self.cubies[i].rotateX_(-90, animate)

	def C_(self, animate=True):
		tempCubie = self.cubies[1]
		self.cubies[1] = self.cubies[24]
		self.cubies[24] = self.cubies[18]
		self.cubies[18] = self.cubies[7]
		self.cubies[7] = tempCubie
		tempCubie = self.cubies[4]
		self.cubies[4] = self.cubies[14]
		self.cubies[14] = self.cubies[21]
		self.cubies[21] = self.cubies[10]
		self.cubies[10] = tempCubie

		for i in [1,4,7,10,14,18,21,24]:
			if animate:
				self.cubies[i].rotateX(90, animate)
			else:
				self.cubies[i].rotateX_(90, animate)

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
