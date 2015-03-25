from cube import Cube
from cubesolver import CubeSolver
from copy import deepcopy

import sys
sys.setrecursionlimit(10000)

class CubeSolverOptimal(CubeSolver):

	__functions = []
	__names = []

	def __init__(self):
		if len(CubeSolverOptimal.__functions) == 0:
			CubeSolverOptimal.__functions = [
							self.F, self.F_,
							self.L, self.L_, self.R, self.R_,
							self.U, self.U_, self.D, self.D_,
							self.M, self.M_, self.C, self.C_
							]

			CubeSolverOptimal.__names = [
						Cube.Front, Cube.Front_,
						Cube.Left, Cube.Left_, Cube.Right, Cube.Right_,
						Cube.Top, Cube.Top_, Cube.Bottom, Cube.Bottom_,
						Cube.Middle, Cube.Middle_, Cube.Center, Cube.Center_
					]
			# CubeSolverOptimal.__functions = [
# 							self.F, self.F_, self.B, self.B_,
# 							self.L, self.L_, self.R, self.R_,
# 							self.U, self.U_, self.D, self.D_,
# 							self.M, self.M_, self.C, self.C_
# 							]
# 
# 			CubeSolverOptimal.__names = [
# 						Cube.Front, Cube.Front_, Cube.Back, Cube.Back_,
# 						Cube.Left, Cube.Left_, Cube.Right, Cube.Right_,
# 						Cube.Top, Cube.Top_, Cube.Bottom, Cube.Bottom_,
# 						Cube.Middle, Cube.Middle_, Cube.Center, Cube.Center_
# 					]

		CubeSolver.__init__(self, 3) # Solves 3x3x3 cubes
		self.currentAlgorithmSteps = []
		self.currentCube = None
		self.solved = True

	def update(self):
		CubeSolver.update(self)
		# Search for the next algorithm
		if not self.currentAlgorithmSteps and not self.solved:
			cubeCopy = deepcopy(self.currentCube)
			solution = self.findSolution(cubeCopy)
			self.currentAlgorithmSteps = solution
			self.solved = True


	def findSolution(self, cube, moveList=None):
		pass
	
	def F(self, cube):
		cube.F()
	def F_(self, cube):
		cube.F_()
	def B(self, cube):
		cube.B()
	def B_(self, cube):
		cube.B_()
	def L(self, cube):
		cube.L_()
	def L_(self, cube):
		cube.L_()
	def R(self, cube):
		cube.R()
	def R_(self, cube):
		cube.R_()
	def U(self, cube):
		cube.U()
	def U_(self, cube):
		cube.U_()
	def D(self, cube):
		cube.D()
	def D_(self, cube):
		cube.D_()
	def M(self, cube):
		cube.M()
	def M_(self, cube):
		cube.M_()
	def C(self, cube):
		cube.C()
	def C_(self, cube):
		cube.C_()
