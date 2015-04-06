from cube import Cube

class CubeSolver:
	"""
	The base class for cube solvers
	"""
	def __init__(self):
		self.currentAlgorithmSteps = []
		self.currentCube = None
		self.solved = True

	def solve(self, cube):
		if self.currentCube:
			raise ValueError("I'm already solving a cube you scrub")
		self.currentCube = cube
		self.solved = False

	def update(self):
		"""
		Call this from subclasses, and don't forget to setup some algorithms
		"""
		if self.currentAlgorithmSteps:
			# Perform the next algorithm step
			(step, offset) = self.currentAlgorithmSteps.pop(0)
			if step == Cube.Top:
				self.currentCube.U(offset)
			elif step == Cube.Top_:
				self.currentCube.U_(offset)
			elif step == Cube.Bottom:
				self.currentCube.D(offset)
			elif step == Cube.Bottom_:
				self.currentCube.D_(offset)
			elif step == Cube.Left:
				self.currentCube.L(offset)
			elif step == Cube.Left_:
				self.currentCube.L_(offset)
			elif step == Cube.Right:
				self.currentCube.R(offset)
			elif step == Cube.Right_:
				self.currentCube.R_(offset)
			elif step == Cube.Front:
				self.currentCube.F(offset)
			elif step == Cube.Front_:
				self.currentCube.F_(offset)
			elif step == Cube.Back:
				self.currentCube.B(offset)
			elif step == Cube.Back_:
				self.currentCube.B_(offset)
			elif step == Cube.Center:
				self.currentCube.C(offset)
			elif step == Cube.Center_:
				self.currentCube.C_(offset)
			elif step == Cube.Middle:
				self.currentCube.M(offset)
			elif step == Cube.Middle_:
				self.currentCube.M_(offset)
