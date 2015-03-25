from cube import Cube
from cubesolver import CubeSolver
from copy import deepcopy

class CubeSolverDavid(CubeSolver):
	"""
	Solves a 3x3x3 Rubik's Cube using the method David Skrundz uses
	It takes about 130 seconds to solve myself
	"""
	StageWhiteOnTop = -1

	StageWhiteRed = 0
	StageWhiteGreen = 1
	StageWhiteOrange = 2
	StageWhiteBlue = 3

	StageWhiteRedGreen = 4
	StageWhiteGreenOrange = 5
	StageWhiteOrangeBlue = 6
	StageWhiteBlueRed = 7

	StageRedGreen = 8
	StageGreenOrange = 9
	StageOrangeBlue = 10
	StageBlueRed = 11

	StageFlipCube = 12

	StageYellowRedBlue = 13
	StageYellowRedGreen = 14
	StageYellowGreenOrange = 15

	StageRotateCorners = 16

	StageRedYellow = 17
	StageGreenYellow = 18

	StageFinal = 19

	StageH = 20
	StageFish = 21

	StageRotate = 22
	
	StageSolved = 23

	def __init__(self):
		CubeSolver.__init__(self, 3) # Solves 3x3x3 cubes
		self.stage = CubeSolverDavid.StageWhiteOnTop
		self.currentAlgorithmSteps = []
		self.currentCube = None

	def update(self):
		# Search for the next algorithm
		if not self.currentAlgorithmSteps:
			faces = self.currentCube.faces() # (top, front, right, back, left, bottom)
			if self.stage == CubeSolverDavid.StageWhiteOnTop:
				# Rotate the cube so the white face is on the top
				if faces[0][1][1] == Cube.White:
					if faces[1][1][1] != Cube.Red:
						self.currentAlgorithmSteps += [Cube.Middle]
					else:
						self.stage = CubeSolverDavid.StageWhiteRed
				elif faces[1][1][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Center]
				elif faces[2][1][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Middle_, Cube.Center]
				elif faces[3][1][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Center_]
				elif faces[4][1][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Middle, Cube.Center]
				elif faces[5][1][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Center, Cube.Center]
				else:
					raise ValueError("Unsolvable cube")

			elif self.stage == CubeSolverDavid.StageWhiteRed:
				if faces[0][2][1] == Cube.White and faces[1][0][1] == Cube.Red:
					self.stage = CubeSolverDavid.StageWhiteGreen
				elif faces[0][2][1] == Cube.Red and faces[1][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Center_, Cube.Bottom, Cube.Bottom, Cube.Center, Cube.Bottom_, Cube.Center_, Cube.Bottom, Cube.Center]

				elif faces[0][1][2] == Cube.White and faces[2][0][1] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Top]
				elif faces[0][1][2] == Cube.Red and faces[2][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top]

				elif faces[0][0][1] == Cube.White and faces[3][0][1] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Top]
				elif faces[0][0][1] == Cube.Red and faces[3][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Top]

				elif faces[0][1][0] == Cube.White and faces[4][0][1] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Top_]
				elif faces[0][1][0] == Cube.Red and faces[4][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top_]

				elif faces[1][1][2] == Cube.White and faces[2][1][0] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Right]
				elif faces[1][1][2] == Cube.Red and faces[2][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right]

				elif faces[2][1][2] == Cube.White and faces[3][1][0] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Right_]
				elif faces[2][1][2] == Cube.Red and faces[3][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right_]

				elif faces[1][1][0] == Cube.White and faces[4][1][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Left_]
				elif faces[1][1][0] == Cube.Red and faces[4][1][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Left_]

				elif faces[3][1][2] == Cube.White and faces[4][1][0] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Left]
				elif faces[3][1][2] == Cube.Red and faces[4][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Left]

				elif faces[1][2][1] == Cube.White and faces[5][0][1] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Front, Cube.Front]
				elif faces[1][2][1] == Cube.Red and faces[5][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Front, Cube.Front]

				elif faces[2][2][1] == Cube.White and faces[5][1][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Right]
				elif faces[2][2][1] == Cube.Red and faces[5][1][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right]

				elif faces[3][2][1] == Cube.White and faces[5][2][1] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[3][2][1] == Cube.Red and faces[5][2][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom]

				elif faces[4][2][1] == Cube.White and faces[5][1][0] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Left, Cube.Left]
				elif faces[4][2][1] == Cube.Red and faces[5][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Left, Cube.Left]

				else:
					raise ValueError("Unsolvable cube")
			elif self.stage == CubeSolverDavid.StageWhiteGreen:
				if faces[0][1][0] == Cube.White and faces[4][0][1] == Cube.Green:
					self.stage = CubeSolverDavid.StageWhiteOrange
				elif faces[0][1][0] == Cube.Green and faces[4][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Center_, Cube.Bottom, Cube.Bottom, Cube.Center, Cube.Bottom_, Cube.Center_, Cube.Bottom, Cube.Center, Cube.Top]

				elif faces[0][0][1] == Cube.White and faces[3][0][1] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Left, Cube.Top, Cube.Left_]
				elif faces[0][0][1] == Cube.Green and faces[3][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Left, Cube.Top, Cube.Left_]

				elif faces[0][1][2] == Cube.White and faces[2][0][1] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Top_, Cube.Left, Cube.Top, Cube.Top, Cube.Left_]
				elif faces[0][1][2] == Cube.Green and faces[2][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Top_, Cube.Left, Cube.Top, Cube.Top, Cube.Left_]

				elif faces[1][1][2] == Cube.White and faces[2][1][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Right]
				elif faces[1][1][2] == Cube.Green and faces[2][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right]

				elif faces[2][1][2] == Cube.White and faces[3][1][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Right_]
				elif faces[2][1][2] == Cube.Green and faces[3][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right_]

				elif faces[1][1][0] == Cube.White and faces[4][1][2] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Left_]
				elif faces[1][1][0] == Cube.Green and faces[4][1][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Left_]

				elif faces[3][1][2] == Cube.White and faces[4][1][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Left]
				elif faces[3][1][2] == Cube.Green and faces[4][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Left]

				elif faces[1][2][1] == Cube.White and faces[5][0][1] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Front, Cube.Front, Cube.Top, Cube.Front, Cube.Front]
				elif faces[1][2][1] == Cube.Green and faces[5][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Front, Cube.Front, Cube.Top, Cube.Front, Cube.Front]

				elif faces[2][2][1] == Cube.White and faces[5][1][2] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Right]
				elif faces[2][2][1] == Cube.Green and faces[5][1][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Right]

				elif faces[3][2][1] == Cube.White and faces[5][2][1] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[3][2][1] == Cube.Green and faces[5][2][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom]

				elif faces[4][2][1] == Cube.White and faces[5][1][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Left, Cube.Left]
				elif faces[4][2][1] == Cube.Green and faces[5][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Left, Cube.Left]

				else:
					raise ValueError("Unsolvable cube")
			elif self.stage == CubeSolverDavid.StageWhiteOrange:
				if faces[0][0][1] == Cube.White and faces[3][0][1] == Cube.Orange:
					self.stage = CubeSolverDavid.StageWhiteBlue
				elif faces[0][0][1] == Cube.Orange and faces[3][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Top_, Cube.Center_, Cube.Bottom, Cube.Bottom, Cube.Center, Cube.Bottom_, Cube.Center_, Cube.Bottom, Cube.Center, Cube.Top, Cube.Top]

				elif faces[0][1][2] == Cube.White and faces[2][0][1] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Top, Cube.Right_, Cube.Top_]
				elif faces[0][1][2] == Cube.Orange and faces[2][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Top, Cube.Right_, Cube.Top_]

				elif faces[1][1][2] == Cube.White and faces[2][1][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Right]
				elif faces[1][1][2] == Cube.Orange and faces[2][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right]

				elif faces[2][1][2] == Cube.White and faces[3][1][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Right_, Cube.Top_]
				elif faces[2][1][2] == Cube.Orange and faces[3][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Right_, Cube.Top_]

				elif faces[1][1][0] == Cube.White and faces[4][1][2] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Left_, Cube.Top]
				elif faces[1][1][0] == Cube.Orange and faces[4][1][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Left_, Cube.Top]

				elif faces[3][1][2] == Cube.White and faces[4][1][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Left, Cube.Top]
				elif faces[3][1][2] == Cube.Orange and faces[4][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Left, Cube.Top]

				elif faces[1][2][1] == Cube.White and faces[5][0][1] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Top, Cube.Front, Cube.Front, Cube.Top, Cube.Top]
				elif faces[1][2][1] == Cube.Orange and faces[5][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Top, Cube.Front, Cube.Front, Cube.Top, Cube.Top]

				elif faces[2][2][1] == Cube.White and faces[5][1][2] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Right, Cube.Right, Cube.Top_]
				elif faces[2][2][1] == Cube.Orange and faces[5][1][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Right, Cube.Right, Cube.Top_]

				elif faces[3][2][1] == Cube.White and faces[5][2][1] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom, Cube.Top, Cube.Top, Cube.Front, Cube.Front, Cube.Top, Cube.Top]
				elif faces[3][2][1] == Cube.Orange and faces[5][2][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom, Cube.Top, Cube.Top, Cube.Front, Cube.Front, Cube.Top, Cube.Top]

				elif faces[4][2][1] == Cube.White and faces[5][1][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom, Cube.Top, Cube.Right, Cube.Right, Cube.Top_]
				elif faces[4][2][1] == Cube.Orange and faces[5][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom, Cube.Top, Cube.Right, Cube.Right, Cube.Top_]

				else:
					raise ValueError("Unsolvable cube")
			elif self.stage == CubeSolverDavid.StageWhiteBlue:
				if faces[0][1][2] == Cube.White and faces[2][0][1] == Cube.Blue:
					self.stage = CubeSolverDavid.StageWhiteRedGreen
				elif faces[0][1][2] == Cube.Blue and faces[2][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Center_, Cube.Bottom, Cube.Bottom, Cube.Center, Cube.Bottom_, Cube.Center_, Cube.Bottom, Cube.Center, Cube.Top_]

				elif faces[1][1][2] == Cube.White and faces[2][1][0] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Right]
				elif faces[1][1][2] == Cube.Blue and faces[2][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right]

				elif faces[2][1][2] == Cube.White and faces[3][1][0] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Right_]
				elif faces[2][1][2] == Cube.Blue and faces[3][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right_]

				elif faces[1][1][0] == Cube.White and faces[4][1][2] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Top, Cube.Left_, Cube.Top, Cube.Top]
				elif faces[1][1][0] == Cube.Blue and faces[4][1][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Top, Cube.Left_, Cube.Top, Cube.Top]

				elif faces[3][1][2] == Cube.White and faces[4][1][0] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Top, Cube.Left, Cube.Top, Cube.Top]
				elif faces[3][1][2] == Cube.Blue and faces[4][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Top, Cube.Left, Cube.Top, Cube.Top]

				elif faces[1][2][1] == Cube.White and faces[5][0][1] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Right, Cube.Right]
				elif faces[1][2][1] == Cube.Blue and faces[5][0][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Right, Cube.Right]

				elif faces[2][2][1] == Cube.White and faces[5][1][2] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Right]
				elif faces[2][2][1] == Cube.Blue and faces[5][1][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Right]

				elif faces[3][2][1] == Cube.White and faces[5][2][1] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right, Cube.Right]
				elif faces[3][2][1] == Cube.Blue and faces[5][2][1] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right, Cube.Right]

				elif faces[4][2][1] == Cube.White and faces[5][1][0] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom, Cube.Right, Cube.Right]
				elif faces[4][2][1] == Cube.Blue and faces[5][1][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom, Cube.Right, Cube.Right]

				else:
					raise ValueError("Unsolvable cube")

			elif self.stage == CubeSolverDavid.StageWhiteRedGreen:
				if faces[0][2][0] == Cube.White and faces[1][0][0] == Cube.Red and faces[4][0][2] == Cube.Green:
					self.stage = CubeSolverDavid.StageWhiteBlueRed
				elif faces[0][2][0] == Cube.Green and faces[1][0][0] == Cube.White and faces[4][0][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Bottom, Cube.Left, Cube.Bottom_, Cube.Left_]
				elif faces[0][2][0] == Cube.Red and faces[1][0][0] == Cube.Green and faces[4][0][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Front_, Cube.Bottom, Cube.Front, Cube.Left, Cube.Bottom, Cube.Left_]

				elif faces[0][0][0] == Cube.White and faces[4][0][0] == Cube.Red and faces[3][0][2] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Left_, Cube.Bottom, Cube.Left]
				elif faces[0][0][0] == Cube.Green and faces[4][0][0] == Cube.White and faces[3][0][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Left_, Cube.Bottom, Cube.Left]
				elif faces[0][0][0] == Cube.Red and faces[4][0][0] == Cube.Green and faces[3][0][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Left_, Cube.Bottom, Cube.Left]

				elif faces[0][0][2] == Cube.White and faces[3][0][0] == Cube.Red and faces[2][0][2] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Bottom, Cube.Right_]
				elif faces[0][0][2] == Cube.Green and faces[3][0][0] == Cube.White and faces[2][0][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Bottom, Cube.Right_]
				elif faces[0][0][2] == Cube.Red and faces[3][0][0] == Cube.Green and faces[2][0][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Bottom, Cube.Right_]

				elif faces[0][2][2] == Cube.White and faces[2][0][0] == Cube.Red and faces[1][0][2] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Right_, Cube.Bottom, Cube.Right]
				elif faces[0][2][2] == Cube.Green and faces[2][0][0] == Cube.White and faces[1][0][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Right_, Cube.Bottom, Cube.Right]
				elif faces[0][2][2] == Cube.Red and faces[2][0][0] == Cube.Green and faces[1][0][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right_, Cube.Bottom, Cube.Right]

				elif faces[1][2][0] == Cube.White and faces[4][2][2] == Cube.Green and faces[5][0][0] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Left, Cube.Bottom_, Cube.Left_]
				elif faces[1][2][0] == Cube.Green and faces[4][2][2] == Cube.Red and faces[5][0][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Left, Cube.Bottom_, Cube.Left_]
				elif faces[1][2][0] == Cube.Red and faces[4][2][2] == Cube.White and faces[5][0][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Left, Cube.Bottom_, Cube.Left_]

				elif faces[1][2][2] == Cube.Green and faces[2][2][0] == Cube.White and faces[5][0][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom_]
				elif faces[1][2][2] == Cube.Red and faces[2][2][0] == Cube.Green and faces[5][0][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom_]
				elif faces[1][2][2] == Cube.White and faces[2][2][0] == Cube.Red and faces[5][0][2] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom_]

				elif faces[2][2][2] == Cube.Green and faces[3][2][0] == Cube.White and faces[5][2][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
				elif faces[2][2][2] == Cube.Red and faces[3][2][0] == Cube.Green and faces[5][2][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
				elif faces[2][2][2] == Cube.White and faces[3][2][0] == Cube.Red and faces[5][2][2] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]

				elif faces[3][2][2] == Cube.Green and faces[4][2][0] == Cube.White and faces[5][2][0] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[3][2][2] == Cube.Red and faces[4][2][0] == Cube.Green and faces[5][2][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[3][2][2] == Cube.White and faces[4][2][0] == Cube.Red and faces[5][2][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom]

				else:
					raise ValueError("Unsolvable cube")
			elif self.stage == CubeSolverDavid.StageWhiteBlueRed:
				if faces[0][2][2] == Cube.White and faces[2][0][0] == Cube.Blue and faces[1][0][2] == Cube.Red:
					self.stage = CubeSolverDavid.StageWhiteGreenOrange
				elif faces[0][2][2] == Cube.Red and faces[2][0][0] == Cube.White and faces[1][0][2] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Right_, Cube.Bottom_, Cube.Right, Cube.Bottom, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
				elif faces[0][2][2] == Cube.Blue and faces[2][0][0] == Cube.Red and faces[1][0][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Front, Cube.Bottom, Cube.Front_, Cube.Bottom, Cube.Bottom, Cube.Right_, Cube.Bottom, Cube.Right]

				elif faces[0][0][0] == Cube.White and faces[4][0][0] == Cube.Blue and faces[3][0][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Left_, Cube.Bottom, Cube.Left]
				elif faces[0][0][0] == Cube.Red and faces[4][0][0] == Cube.White and faces[3][0][2] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Left_, Cube.Bottom, Cube.Left]
				elif faces[0][0][0] == Cube.Blue and faces[4][0][0] == Cube.Red and faces[3][0][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Left_, Cube.Bottom, Cube.Left]

				elif faces[0][0][2] == Cube.White and faces[3][0][0] == Cube.Blue and faces[2][0][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Bottom, Cube.Right_]
				elif faces[0][0][2] == Cube.Red and faces[3][0][0] == Cube.White and faces[2][0][2] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Bottom, Cube.Right_]
				elif faces[0][0][2] == Cube.Blue and faces[3][0][0] == Cube.Red and faces[2][0][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Bottom, Cube.Right_]

				elif faces[1][2][0] == Cube.White and faces[4][2][2] == Cube.Red and faces[5][0][0] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Right_, Cube.Bottom, Cube.Right]
				elif faces[1][2][0] == Cube.Red and faces[4][2][2] == Cube.Blue and faces[5][0][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right_, Cube.Bottom, Cube.Right]
				elif faces[1][2][0] == Cube.Blue and faces[4][2][2] == Cube.White and faces[5][0][0] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Right_, Cube.Bottom, Cube.Right]

				elif faces[1][2][2] == Cube.Red and faces[2][2][0] == Cube.White and faces[5][0][2] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom_]
				elif faces[1][2][2] == Cube.Blue and faces[2][2][0] == Cube.Red and faces[5][0][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom_]
				elif faces[1][2][2] == Cube.White and faces[2][2][0] == Cube.Blue and faces[5][0][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom_]

				elif faces[2][2][2] == Cube.Red and faces[3][2][0] == Cube.White and faces[5][2][2] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
				elif faces[2][2][2] == Cube.Blue and faces[3][2][0] == Cube.Red and faces[5][2][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
				elif faces[2][2][2] == Cube.White and faces[3][2][0] == Cube.Blue and faces[5][2][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]

				elif faces[3][2][2] == Cube.Red and faces[4][2][0] == Cube.White and faces[5][2][0] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[3][2][2] == Cube.Blue and faces[4][2][0] == Cube.Red and faces[5][2][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[3][2][2] == Cube.White and faces[4][2][0] == Cube.Blue and faces[5][2][0] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom]

				else:
					raise ValueError("Unsolvable cube")
			elif self.stage == CubeSolverDavid.StageWhiteGreenOrange:
				if faces[0][0][0] == Cube.White and faces[3][0][2] == Cube.Orange and faces[4][0][0] == Cube.Green:
					self.stage = CubeSolverDavid.StageWhiteOrangeBlue
				elif faces[0][0][0] == Cube.Green and faces[3][0][2] == Cube.White and faces[4][0][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Left, Cube.Bottom, Cube.Left_, Cube.Bottom, Cube.Bottom, Cube.Front_, Cube.Bottom, Cube.Front, Cube.Top]
				elif faces[0][0][0] == Cube.Orange and faces[3][0][2] == Cube.Green and faces[4][0][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Bottom, Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Top]

				elif faces[0][0][2] == Cube.White and faces[3][0][0] == Cube.Green and faces[2][0][2] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Bottom, Cube.Right_]
				elif faces[0][0][2] == Cube.Orange and faces[3][0][0] == Cube.White and faces[2][0][2] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Bottom, Cube.Right_]
				elif faces[0][0][2] == Cube.Green and faces[3][0][0] == Cube.Orange and faces[2][0][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Bottom, Cube.Right_]

				elif faces[1][2][0] == Cube.White and faces[4][2][2] == Cube.Orange and faces[5][0][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Bottom, Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Top]
				elif faces[1][2][0] == Cube.Orange and faces[4][2][2] == Cube.Green and faces[5][0][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Bottom, Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Top]
				elif faces[1][2][0] == Cube.Green and faces[4][2][2] == Cube.White and faces[5][0][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Top_, Cube.Bottom, Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Top]

				elif faces[1][2][2] == Cube.Orange and faces[2][2][0] == Cube.White and faces[5][0][2] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom_]
				elif faces[1][2][2] == Cube.Green and faces[2][2][0] == Cube.Orange and faces[5][0][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom_]
				elif faces[1][2][2] == Cube.White and faces[2][2][0] == Cube.Green and faces[5][0][2] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom_]

				elif faces[2][2][2] == Cube.Orange and faces[3][2][0] == Cube.White and faces[5][2][2] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
				elif faces[2][2][2] == Cube.Green and faces[3][2][0] == Cube.Orange and faces[5][2][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
				elif faces[2][2][2] == Cube.White and faces[3][2][0] == Cube.Green and faces[5][2][2] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]

				elif faces[3][2][2] == Cube.Orange and faces[4][2][0] == Cube.White and faces[5][2][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[3][2][2] == Cube.Green and faces[4][2][0] == Cube.Orange and faces[5][2][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[3][2][2] == Cube.White and faces[4][2][0] == Cube.Green and faces[5][2][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom]

				else:
					raise ValueError("Unsolvable cube")
			elif self.stage == CubeSolverDavid.StageWhiteOrangeBlue:
				if faces[0][0][2] == Cube.White and faces[3][0][0] == Cube.Orange and faces[2][0][2] == Cube.Blue:
					self.stage = CubeSolverDavid.StageRedGreen
				elif faces[0][0][2] == Cube.Blue and faces[3][0][0] == Cube.White and faces[2][0][2] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Right, Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom_, Cube.Right_]
				elif faces[0][0][2] == Cube.Orange and faces[3][0][0] == Cube.Blue and faces[2][0][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Top_]

				elif faces[1][2][0] == Cube.White and faces[4][2][2] == Cube.Blue and faces[5][0][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Top_]
				elif faces[1][2][0] == Cube.Blue and faces[4][2][2] == Cube.Orange and faces[5][0][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Top_]
				elif faces[1][2][0] == Cube.Orange and faces[4][2][2] == Cube.White and faces[5][0][0] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Top_]

				elif faces[1][2][2] == Cube.Blue and faces[2][2][0] == Cube.White and faces[5][0][2] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom_]
				elif faces[1][2][2] == Cube.Orange and faces[2][2][0] == Cube.Blue and faces[5][0][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom_]
				elif faces[1][2][2] == Cube.White and faces[2][2][0] == Cube.Orange and faces[5][0][2] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom_]

				elif faces[2][2][2] == Cube.Blue and faces[3][2][0] == Cube.White and faces[5][2][2] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
				elif faces[2][2][2] == Cube.Orange and faces[3][2][0] == Cube.Blue and faces[5][2][2] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
				elif faces[2][2][2] == Cube.White and faces[3][2][0] == Cube.Orange and faces[5][2][2] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]

				elif faces[3][2][2] == Cube.Blue and faces[4][2][0] == Cube.White and faces[5][2][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[3][2][2] == Cube.Orange and faces[4][2][0] == Cube.Blue and faces[5][2][0] == Cube.White:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[3][2][2] == Cube.White and faces[4][2][0] == Cube.Orange and faces[5][2][0] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom]

				else:
					raise ValueError("Unsolvable cube")

# Before here it messes up

			elif self.stage == CubeSolverDavid.StageRedGreen:
				if faces[1][1][0] == Cube.Red and faces[4][1][2] == Cube.Green:
					self.stage = CubeSolverDavid.StageGreenOrange
					self.currentAlgorithmSteps += [Cube.Middle]
				elif faces[1][1][0] == Cube.Green and faces[4][1][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Bottom_, Cube.Front_, Cube.Bottom, Cube.Front]

				elif faces[1][1][2] == Cube.Red and faces[2][1][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
				elif faces[1][1][2] == Cube.Green and faces[2][1][0] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]

				elif faces[2][1][2] == Cube.Red and faces[3][1][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Middle_]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
					self.currentAlgorithmSteps += [Cube.Middle]
				elif faces[2][1][2] == Cube.Green and faces[3][1][0] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Middle_]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
					self.currentAlgorithmSteps += [Cube.Middle]

				elif faces[3][1][2] == Cube.Red and faces[4][1][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Middle_, Cube.Middle_]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
					self.currentAlgorithmSteps += [Cube.Middle, Cube.Middle]
				elif faces[3][1][2] == Cube.Green and faces[4][1][0] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Middle_, Cube.Middle_]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
					self.currentAlgorithmSteps += [Cube.Middle, Cube.Middle]

				elif faces[1][2][1] == Cube.Red and faces[5][0][1] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Bottom_, Cube.Front_, Cube.Bottom, Cube.Front]
				elif faces[1][2][1] == Cube.Green and faces[5][0][1] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Middle]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Middle_]

				elif faces[2][2][1] == Cube.Red and faces[5][1][2] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom_]
				elif faces[2][2][1] == Cube.Green and faces[5][1][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom_]

				elif faces[3][2][1] == Cube.Red and faces[5][2][1] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
				elif faces[3][2][1] == Cube.Green and faces[5][2][1] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]

				elif faces[4][2][1] == Cube.Red and faces[5][1][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[4][2][1] == Cube.Green and faces[5][1][0] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom]

				else:
					raise ValueError("Unsolvable cube")
			elif self.stage == CubeSolverDavid.StageGreenOrange:
				if faces[1][1][0] == Cube.Green and faces[4][1][2] == Cube.Orange:
					self.stage = CubeSolverDavid.StageOrangeBlue
					self.currentAlgorithmSteps += [Cube.Middle]
				elif faces[1][1][0] == Cube.Orange and faces[4][1][2] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Bottom_, Cube.Front_, Cube.Bottom, Cube.Front]

				elif faces[2][1][2] == Cube.Green and faces[3][1][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Middle_]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
					self.currentAlgorithmSteps += [Cube.Middle]
				elif faces[2][1][2] == Cube.Orange and faces[3][1][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Middle_]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
					self.currentAlgorithmSteps += [Cube.Middle]

				elif faces[3][1][2] == Cube.Green and faces[4][1][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Middle_, Cube.Middle_]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
					self.currentAlgorithmSteps += [Cube.Middle, Cube.Middle]
				elif faces[3][1][2] == Cube.Orange and faces[4][1][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Middle_, Cube.Middle_]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
					self.currentAlgorithmSteps += [Cube.Middle, Cube.Middle]

				elif faces[1][2][1] == Cube.Green and faces[5][0][1] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Bottom_, Cube.Front_, Cube.Bottom, Cube.Front]
				elif faces[1][2][1] == Cube.Orange and faces[5][0][1] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Middle]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Middle_]

				elif faces[2][2][1] == Cube.Green and faces[5][1][2] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom_]
				elif faces[2][2][1] == Cube.Orange and faces[5][1][2] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom_]

				elif faces[3][2][1] == Cube.Green and faces[5][2][1] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
				elif faces[3][2][1] == Cube.Orange and faces[5][2][1] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]

				elif faces[4][2][1] == Cube.Green and faces[5][1][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[4][2][1] == Cube.Orange and faces[5][1][0] == Cube.Green:
					self.currentAlgorithmSteps += [Cube.Bottom]

				else:
					raise ValueError("Unsolvable cube")
			elif self.stage == CubeSolverDavid.StageOrangeBlue:
				if faces[1][1][0] == Cube.Orange and faces[4][1][2] == Cube.Blue:
					self.stage = CubeSolverDavid.StageBlueRed
					self.currentAlgorithmSteps += [Cube.Middle]
				elif faces[1][1][0] == Cube.Blue and faces[4][1][2] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Bottom_, Cube.Front_, Cube.Bottom, Cube.Front]

				elif faces[3][1][2] == Cube.Orange and faces[4][1][0] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Middle_, Cube.Middle_]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
					self.currentAlgorithmSteps += [Cube.Middle, Cube.Middle]
				elif faces[3][1][2] == Cube.Blue and faces[4][1][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Middle_, Cube.Middle_]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
					self.currentAlgorithmSteps += [Cube.Middle, Cube.Middle]

				elif faces[1][2][1] == Cube.Orange and faces[5][0][1] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Bottom_, Cube.Front_, Cube.Bottom, Cube.Front]
				elif faces[1][2][1] == Cube.Blue and faces[5][0][1] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Middle]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Middle_]

				elif faces[2][2][1] == Cube.Orange and faces[5][1][2] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom_]
				elif faces[2][2][1] == Cube.Blue and faces[5][1][2] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom_]

				elif faces[3][2][1] == Cube.Orange and faces[5][2][1] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
				elif faces[3][2][1] == Cube.Blue and faces[5][2][1] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]

				elif faces[4][2][1] == Cube.Orange and faces[5][1][0] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[4][2][1] == Cube.Blue and faces[5][1][0] == Cube.Orange:
					self.currentAlgorithmSteps += [Cube.Bottom]

				else:
					raise ValueError("Unsolvable cube")
			elif self.stage == CubeSolverDavid.StageBlueRed:
				if faces[1][1][0] == Cube.Blue and faces[4][1][2] == Cube.Red:
					self.stage = CubeSolverDavid.StageFlipCube
					self.currentAlgorithmSteps += [Cube.Middle]
				elif faces[1][1][0] == Cube.Red and faces[4][1][2] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Bottom_, Cube.Front_, Cube.Bottom, Cube.Front]

				elif faces[1][2][1] == Cube.Blue and faces[5][0][1] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Left, Cube.Bottom_, Cube.Left_, Cube.Bottom_, Cube.Front_, Cube.Bottom, Cube.Front]
				elif faces[1][2][1] == Cube.Red and faces[5][0][1] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Middle]
					self.currentAlgorithmSteps += [Cube.Bottom_, Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom, Cube.Front, Cube.Bottom_, Cube.Front_]
					self.currentAlgorithmSteps += [Cube.Middle_]

				elif faces[2][2][1] == Cube.Blue and faces[5][1][2] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom_]
				elif faces[2][2][1] == Cube.Red and faces[5][1][2] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom_]

				elif faces[3][2][1] == Cube.Blue and faces[5][2][1] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]
				elif faces[3][2][1] == Cube.Red and faces[5][2][1] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom, Cube.Bottom]

				elif faces[4][2][1] == Cube.Blue and faces[5][1][0] == Cube.Red:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[4][2][1] == Cube.Red and faces[5][1][0] == Cube.Blue:
					self.currentAlgorithmSteps += [Cube.Bottom]

				else:
					raise ValueError("Unsolvable cube")

			elif self.stage == CubeSolverDavid.StageFlipCube:
				self.stage = CubeSolverDavid.StageYellowRedBlue
				self.currentAlgorithmSteps += [Cube.Left, Cube.Left, Cube.Center, Cube.Center, Cube.Right, Cube.Right]
				self.currentAlgorithmSteps += [Cube.Top, Cube.Top, Cube.Middle, Cube.Middle, Cube.Bottom, Cube.Bottom]

			elif self.stage == CubeSolverDavid.StageYellowRedBlue:
				if not ((faces[0][2][0] == Cube.Blue or faces[1][0][0] == Cube.Blue or faces[4][0][2] == Cube.Blue) and (faces[0][2][0] == Cube.Red or faces[1][0][0] == Cube.Red or faces[4][0][2] == Cube.Red)):
					self.currentAlgorithmSteps += [Cube.Top]
				else:
					self.currentAlgorithmSteps += [Cube.Top]
					self.stage = CubeSolverDavid.StageYellowRedGreen
			elif self.stage == CubeSolverDavid.StageYellowRedGreen:
				if not ((faces[0][2][0] == Cube.Green or faces[1][0][0] == Cube.Green or faces[4][0][2] == Cube.Green) and (faces[0][2][0] == Cube.Red or faces[1][0][0] == Cube.Red or faces[4][0][2] == Cube.Red)):
					self.currentAlgorithmSteps += [Cube.Left_, Cube.Top_, Cube.Left, Cube.Front, Cube.Top, Cube.Front_, Cube.Left_, Cube.Top, Cube.Left, Cube.Top, Cube.Top]
					self.currentAlgorithmSteps += [Cube.Top]
					self.currentAlgorithmSteps += [Cube.Left_, Cube.Top_, Cube.Left, Cube.Front, Cube.Top, Cube.Front_, Cube.Left_, Cube.Top, Cube.Left, Cube.Top, Cube.Top]
					self.currentAlgorithmSteps += [Cube.Top_]
				else:
					self.currentAlgorithmSteps += [Cube.Top]
					self.stage = CubeSolverDavid.StageYellowGreenOrange
			elif self.stage == CubeSolverDavid.StageYellowGreenOrange:
				if not ((faces[0][2][0] == Cube.Green or faces[1][0][0] == Cube.Green or faces[4][0][2] == Cube.Green) and (faces[0][2][0] == Cube.Orange or faces[1][0][0] == Cube.Orange or faces[4][0][2] == Cube.Orange)):
					self.currentAlgorithmSteps += [Cube.Left_, Cube.Top_, Cube.Left, Cube.Front, Cube.Top, Cube.Front_, Cube.Left_, Cube.Top, Cube.Left, Cube.Top, Cube.Top]
				else:
					self.currentAlgorithmSteps += [Cube.Top, Cube.Top]
					self.stage = CubeSolverDavid.StageRotateCorners

			elif self.stage == CubeSolverDavid.StageRotateCorners:
				if faces[0][2][2] == Cube.Yellow and faces[0][0][2] == Cube.Yellow and faces[0][0][0] == Cube.Yellow and faces[0][2][0] == Cube.Yellow:
					if faces[1][0][0] == Cube.Red:
						self.stage = CubeSolverDavid.StageRedYellow
					else:
						self.currentAlgorithmSteps += [Cube.Top]
				else:
					if faces[0][2][2] == Cube.Yellow:
						self.currentAlgorithmSteps += [Cube.Top]
					else:
						self.currentAlgorithmSteps += [Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom_]
						self.currentAlgorithmSteps += [Cube.Right_, Cube.Bottom, Cube.Right, Cube.Bottom_]

			elif self.stage == CubeSolverDavid.StageRedYellow:
				if faces[0][2][1] == Cube.Red or faces[1][0][1] == Cube.Red:
					self.stage = CubeSolverDavid.StageGreenYellow
				else:
					if faces[0][1][2] == Cube.Red or faces[2][0][1] == Cube.Red:
						self.currentAlgorithmSteps += [Cube.Top_]
						self.currentAlgorithmSteps += [Cube.Center, Cube.Top, Cube.Center_, Cube.Top, Cube.Top, Cube.Center, Cube.Top, Cube.Center_]
						self.currentAlgorithmSteps += [Cube.Top]
					elif faces[0][0][1] == Cube.Red or faces[3][0][1] == Cube.Red:
						self.currentAlgorithmSteps += [Cube.Top]
						self.currentAlgorithmSteps += [Cube.Center, Cube.Top, Cube.Center_, Cube.Top, Cube.Top, Cube.Center, Cube.Top, Cube.Center_]
						self.currentAlgorithmSteps += [Cube.Top_]
					else:
						self.currentAlgorithmSteps += [Cube.Top, Cube.Top]
						self.currentAlgorithmSteps += [Cube.Center, Cube.Top, Cube.Center_, Cube.Top, Cube.Top, Cube.Center, Cube.Top, Cube.Center_]
						self.currentAlgorithmSteps += [Cube.Top, Cube.Top]
			elif self.stage == CubeSolverDavid.StageGreenYellow:
				if faces[0][1][2] == Cube.Green or faces[2][0][1] == Cube.Green:
					self.stage = CubeSolverDavid.StageFinal
				else:
					if faces[0][1][0] == Cube.Green or faces[4][0][1] == Cube.Green:
						self.currentAlgorithmSteps += [Cube.Center, Cube.Top_, Cube.Center_, Cube.Top, Cube.Top, Cube.Center, Cube.Top_, Cube.Center_]
					else:
						self.currentAlgorithmSteps += [Cube.Center, Cube.Top, Cube.Center_, Cube.Top, Cube.Top, Cube.Center, Cube.Top, Cube.Center_]

			elif self.stage == CubeSolverDavid.StageFinal:
				a = faces[0][0][1] == Cube.Yellow
				b = faces[0][1][0] == Cube.Yellow
				c = faces[0][2][1] == Cube.Yellow
				d = faces[0][1][2] == Cube.Yellow
				s = a + b + c + d
				if s == 4:
					pass
				elif s == 2:
					if a == c:
						self.stage = CubeSolverDavid.StageH
					else:
						self.stage = CubeSolverDavid.StageFish
				else:
					self.stage = CubeSolverDavid.StageSolved
					self.currentAlgorithmSteps += [
													Cube.Center_, Cube.Bottom, Cube.Bottom, Cube.Center, Cube.Bottom_, Cube.Center_, Cube.Bottom, Cube.Center,
													Cube.Top, Cube.Middle_, Cube.Bottom_,
													Cube.Center_, Cube.Bottom, Cube.Bottom, Cube.Center, Cube.Bottom_, Cube.Center_, Cube.Bottom, Cube.Center,
													Cube.Top, Cube.Middle_, Cube.Bottom_,
													Cube.Center_, Cube.Bottom, Cube.Bottom, Cube.Center, Cube.Bottom_, Cube.Center_, Cube.Bottom, Cube.Center,
													Cube.Top, Cube.Middle_, Cube.Bottom_,
													Cube.Center_, Cube.Bottom, Cube.Bottom, Cube.Center, Cube.Bottom_, Cube.Center_, Cube.Bottom, Cube.Center
												]

			elif self.stage == CubeSolverDavid.StageH:
				if faces[0][2][1] == Cube.Yellow:
					self.currentAlgorithmSteps += [Cube.Top]
				self.currentAlgorithmSteps += [
												Cube.Center_, Cube.Bottom, Cube.Bottom, Cube.Center, Cube.Bottom_, Cube.Center_, Cube.Bottom, Cube.Center,
												Cube.Top, Cube.Middle_, Cube.Bottom_, Cube.Top, Cube.Middle_, Cube.Bottom_,
												Cube.Center_, Cube.Bottom, Cube.Bottom, Cube.Center, Cube.Bottom_, Cube.Center_, Cube.Bottom, Cube.Center,

												Cube.Top, Cube.Middle_, Cube.Bottom_, Cube.Top, Cube.Middle_, Cube.Bottom_,
												Cube.Left, Cube.Left, Cube.Center, Cube.Center, Cube.Right, Cube.Right,

												Cube.Center, Cube.Top_, Cube.Center_, Cube.Top, Cube.Top, Cube.Center, Cube.Top_, Cube.Center_
											]
				self.stage = CubeSolverDavid.StageFish
			elif self.stage == CubeSolverDavid.StageFish:
				# Properly orient for fish algorithm
				topColor = faces[0][0][0]
				if (faces[0][2][1] == topColor or faces[0][1][2] == topColor):
					self.currentAlgorithmSteps += [Cube.Top]
				else:
					self.currentAlgorithmSteps += [
												Cube.Center_, Cube.Bottom, Cube.Bottom, Cube.Center, Cube.Bottom_, Cube.Center_, Cube.Bottom, Cube.Center,
												Cube.Top, Cube.Middle_, Cube.Bottom_,
												Cube.Center_, Cube.Bottom, Cube.Bottom, Cube.Center, Cube.Bottom_, Cube.Center_, Cube.Bottom, Cube.Center,

												Cube.Left, Cube.Left, Cube.Center, Cube.Center, Cube.Right, Cube.Right,

												Cube.Center, Cube.Top_, Cube.Center_, Cube.Top, Cube.Top, Cube.Center, Cube.Top_, Cube.Center_,
												Cube.Top, Cube.Middle_, Cube.Bottom_,
												Cube.Center, Cube.Top_, Cube.Center_, Cube.Top, Cube.Top, Cube.Center, Cube.Top_, Cube.Center_
											]
					self.stage = CubeSolverDavid.StageRotate
			elif self.stage == CubeSolverDavid.StageRotate:
				if faces[1][2][1] != faces[1][1][1]:
					self.currentAlgorithmSteps += [Cube.Bottom]
				elif faces[1][0][1] != faces[1][1][1]:
					self.currentAlgorithmSteps += [Cube.Top]
				else:
					self.stage = CubeSolverDavid.StageSolved
			
			elif self.stage == CubeSolverDavid.StageSolved:
				self.solved = True

			else:
				raise ValueError("Unsolvable cube")
		CubeSolver.update(self)
