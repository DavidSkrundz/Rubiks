from cube import Cube

class CubeSolver:
	"""
	The base class for cube solvers
	"""
	def __init__(self, n):
		self.n = n
		self.currentAlgorithmSteps = []
		self.currentCube = None
		self.solved = True

	def solve(self, cube):
		if self.currentCube:
			raise ValueError("I'm already solving a cube you scrub")
		if cube.N != self.n:
			raise ValueError("Cube size does not match solution size")
		self.currentCube = cube
		self.solved = False

	def update(self):
		"""
		Call this from subclasses, and don't forget to setup some algorithms
		"""
		if self.currentAlgorithmSteps:
			# Perform the next algorithm step
			step = self.currentAlgorithmSteps.pop(0)
			if step == Cube.Top:
				self.currentCube.U()
			elif step == Cube.Top_:
				self.currentCube.U_()
			elif step == Cube.Bottom:
				self.currentCube.D()
			elif step == Cube.Bottom_:
				self.currentCube.D_()
			elif step == Cube.Left:
				self.currentCube.L()
			elif step == Cube.Left_:
				self.currentCube.L_()
			elif step == Cube.Right:
				self.currentCube.R()
			elif step == Cube.Right_:
				self.currentCube.R_()
			elif step == Cube.Front:
				self.currentCube.F()
			elif step == Cube.Front_:
				self.currentCube.F_()
			elif step == Cube.Back:
				self.currentCube.B()
			elif step == Cube.Back_:
				self.currentCube.B_()
			elif step == Cube.Center:
				self.currentCube.C()
			elif step == Cube.Center_:
				self.currentCube.C_()
			elif step == Cube.Middle:
				self.currentCube.M()
			elif step == Cube.Middle_:
				self.currentCube.M_()
