"""
New cube
"""
from cubie import Cubie

W = Cubie.White
R = Cubie.Red
O = Cubie.Orange
G = Cubie.Green
B = Cubie.Blue
Y = Cubie.Yellow
C = Cubie.Clear

from helpers import Point

class Cube:
	"""
	Cube class
	"""
	Top = 1
	Bottom = 2
	Left = 3
	Right = 4
	Front = 5
	Middle = 6
	Centerr = 7

	Top_ = -1
	Bottom_ = -2
	Left_ = -3
	Right_ = -4
	Front_ = -5
	Middle_ = -6
	Center_ = -7

	Moves = None

	def __init__(self):
		if Cube.Moves is None:
			Cube.Moves = {
				1: Cube.U,
				2: Cube.D,
				3: Cube.L,
				4: Cube.R,
				5: Cube.F,
				6: Cube.M,
				7: Cube.C,

				-1: Cube.U_,
				-2: Cube.D_,
				-3: Cube.L_,
				-4: Cube.R_,
				-5: Cube.F_,
				-6: Cube.M_,
				-7: Cube.C_,

				11: Cube.RRR,
				-11:Cube.RRR_,

				12: Cube.UUU,
				-12:Cube.UUU_
			}

		self.cubies = [
						# Top
						Cubie([W, C, C, O, B, C], Point(-1, +1, +1)), # 0
						Cubie([W, C, C, O, C, C], Point(+0, +1, +1)), # 1
						Cubie([W, C, G, O, C, C], Point(+1, +1, +1)), # 2

						Cubie([W, C, C, C, B, C], Point(-1, +0, +1)), # 3
						Cubie([W, C, C, C, C, C], Point(+0, +0, +1)), # 4
						Cubie([W, C, G, C, C, C], Point(+1, +0, +1)), # 5

						Cubie([W, R, C, C, B, C], Point(-1, -1, +1)), # 6
						Cubie([W, R, C, C, C, C], Point(+0, -1, +1)), # 7
						Cubie([W, R, G, C, C, C], Point(+1, -1, +1)), # 8

						# Middle
						Cubie([C, R, C, C, B, C], Point(-1, -1, +0)), # 9
						Cubie([C, R, C, C, C, C], Point(+0, -1, +0)), # 10
						Cubie([C, R, G, C, C, C], Point(+1, -1, +0)), # 11

						Cubie([C, C, G, C, C, C], Point(+1, +0, +0)), # 12

						Cubie([C, C, G, O, C, C], Point(+1, +1, +0)), # 13
						Cubie([C, C, C, O, C, C], Point(+0, +1, +0)), # 14
						Cubie([C, C, C, O, B, C], Point(-1, +1, +0)), # 15

						Cubie([C, C, C, C, B, C], Point(-1, +0, +0)), # 16

						# Bottom
						Cubie([C, R, C, C, B, Y], Point(-1, -1, -1)), # 17
						Cubie([C, R, C, C, C, Y], Point(+0, -1, -1)), # 18
						Cubie([C, R, G, C, C, Y], Point(+1, -1, -1)), # 19

						Cubie([C, C, C, C, B, Y], Point(-1, +0, -1)), # 20
						Cubie([C, C, C, C, C, Y], Point(+0, +0, -1)), # 21
						Cubie([C, C, G, C, C, Y], Point(+1, +0, -1)), # 22

						Cubie([C, C, C, O, B, Y], Point(-1, +1, -1)), # 23
						Cubie([C, C, C, O, C, Y], Point(+0, +1, -1)), # 24
						Cubie([C, C, G, O, C, Y], Point(+1, +1, -1)), # 25
					]

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

	def update(self):
		doneUpdate = True
		for cubie in self.cubies:
			if not cubie.update():
				doneUpdate = False
		return doneUpdate

	def U_(self):
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
			self.cubies[i].rotateZ(-90)

	def U(self):
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
			self.cubies[i].rotateZ(90)

	def F_(self):
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
			self.cubies[i].rotateY(90)

	def F(self):
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
			self.cubies[i].rotateY(-90)

	def R_(self):
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

		for i in [0,3,6,9,15,16,17,20,23]:
			self.cubies[i].rotateX(90)

	def R(self):
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

		for i in [0,3,6,9,15,16,17,20,23]:
			self.cubies[i].rotateX(-90)

	def L_(self):
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
			self.cubies[i].rotateX(-90)

	def L(self):
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
			self.cubies[i].rotateX(90)

	def D_(self):
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

		for i in [17,18,19,20,22,23,24,25]:
			self.cubies[i].rotateZ(90)

	def D(self):
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

		for i in [17,18,19,20,22,23,24,25]:
			self.cubies[i].rotateZ(-90)

	def M_(self):
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
			self.cubies[i].rotateZ(90)

	def M(self):
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
			self.cubies[i].rotateZ(-90)

	def C(self):
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
			self.cubies[i].rotateX(-90)

	def C_(self):
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
			self.cubies[i].rotateX(90)

	def UUU(self):
		self.U_()
		self.M()
		self.D()

	def UUU_(self):
		self.U()
		self.M_()
		self.D_()

	def RRR(self):
		self.R()
		self.C()
		self.L_()

	def RRR_(self):
		self.R_()
		self.C_()
		self.L()
