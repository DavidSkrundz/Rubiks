from cubesolver import CubeSolver
from cubie import Cubie
import math
from cube import Cube

W = Cubie.White
R = Cubie.Red
O = Cubie.Orange
G = Cubie.Green
B = Cubie.Blue
Y = Cubie.Yellow
C = Cubie.Clear

def colorToInt(color):
	if color == W:
		return 3
	if color == R:
		return 5
	if color == B:
		return 4
	if color == O:
		return 0
	if color == G:
		return 1
	if color == Y:
		return 2

class SearchSolver(CubeSolver):
	def __init__(self):
		CubeSolver.__init__(self)

		# Constant - The cubie pairs
		# Some magic
		self.pieces = [15,16,16,21,21,15,13,9,9,17,17,13,14,20,20,4,4,14,12,5,5,8,8,12,3,23,23,18,18,3,1,19,19,11,11,1,2,6,6,22,22,2,0,10,10,7,7,0]

		self.posit = []

		self.perm = [-1] * 5040
		self.permmv = [-1] * 5040
		self.twst = [-1] * 729
		self.twstmv = [-1] * 729

		self.sol = [-1] * 12
		self.adj = [[0] * 6 for _ in range(6)]

		self.stage = 0

	def countAdjacentPairs(self):
		n = self.currentCube.N - 1

		# Construct an array of the color of the faces
		self.posit = []
		# Bottom
		self.posit += [colorToInt(self.currentCube.cubies[n][n][0].topColor())]
		self.posit += [colorToInt(self.currentCube.cubies[n][n][n].topColor())]
		self.posit += [colorToInt(self.currentCube.cubies[n][0][0].topColor())]
		self.posit += [colorToInt(self.currentCube.cubies[n][0][n].topColor())]
		# Left
		self.posit += [colorToInt(self.currentCube.cubies[0][0][0].rightColor())]
		self.posit += [colorToInt(self.currentCube.cubies[0][n][0].rightColor())]
		self.posit += [colorToInt(self.currentCube.cubies[n][0][0].rightColor())]
		self.posit += [colorToInt(self.currentCube.cubies[n][n][0].rightColor())]
		# Back
		self.posit += [colorToInt(self.currentCube.cubies[0][n][0].backColor())]
		self.posit += [colorToInt(self.currentCube.cubies[0][n][n].backColor())]
		self.posit += [colorToInt(self.currentCube.cubies[n][n][0].backColor())]
		self.posit += [colorToInt(self.currentCube.cubies[n][n][n].backColor())]
		# Top
		self.posit += [colorToInt(self.currentCube.cubies[0][n][0].bottomColor())]
		self.posit += [colorToInt(self.currentCube.cubies[0][n][n].bottomColor())]
		self.posit += [colorToInt(self.currentCube.cubies[0][0][0].bottomColor())]
		self.posit += [colorToInt(self.currentCube.cubies[0][0][n].bottomColor())]
		# Right
		self.posit += [colorToInt(self.currentCube.cubies[0][0][n].leftColor())]
		self.posit += [colorToInt(self.currentCube.cubies[0][n][n].leftColor())]
		self.posit += [colorToInt(self.currentCube.cubies[n][0][n].leftColor())]
		self.posit += [colorToInt(self.currentCube.cubies[n][n][n].leftColor())]
		# Front
		self.posit += [colorToInt(self.currentCube.cubies[0][0][0].frontColor())]
		self.posit += [colorToInt(self.currentCube.cubies[0][0][n].frontColor())]
		self.posit += [colorToInt(self.currentCube.cubies[n][0][0].frontColor())]
		self.posit += [colorToInt(self.currentCube.cubies[n][0][n].frontColor())]

		for a in range(0, 48, 2):
			self.adj[self.posit[self.pieces[a]]][self.posit[self.pieces[a+1]]] += 1

	def search(self, d, q, t, l, lm):
		if l == 0:
			if q == 0 and t == 0:
				return True
		else:
			if self.perm[q] > l or self.twst[t] > l:
				return False
			p = None
			s = None
			a = None
			for m in range(3):
				if m != lm:
					p = q
					s = t
					for a in range(3):
						p = self.permmv[p][m]
						s = self.twstmv[s][m]
						self.sol[d] = 10*m+a
						if self.search(d+1, p, s, l-1, m):
							return True
		return False

	def calcPerm(self):
		#calculate solving arrays
		#first permutation
		for p in range(5040):
			self.perm[p] = -1
			self.permmv[p] = [-1] * 3
			for m in range(3):
				self.permmv[p][m] = self.getprmmv(p,m)

		self.perm[0]=0;
		for l in range(7):
			n = 0
			for p in range(5040):
				if self.perm[p] == l:
					for m in range(3):
						q = p
						for c in range(3):
							q = self.permmv[q][m]
							if self.perm[q] == -1:
								self.perm[q] = l+1
								n += 1
		#then twist
		for p in range(729):
			self.twst[p] = -1
			self.twstmv[p] = [-1] * 3
			for m in range(3):
				self.twstmv[p][m] = self.gettwsmv(p,m)
		self.twst[0] = 0
		for l in range(6):
			n = 0
			for p in range(729):
				if self.twst[p] == l:
					for m in range(3):
						q = p
						for c in range(3):
							q = self.twstmv[q][m]
							if self.twst[q] == -1:
								self.twst[q] = l+1
								n += 1

	def getprmmv(self, p, m):
		b = None
		c = None
		ps = [-1] * 5040
		q = p
		for a in range(1, 8):
			b = q % a
			q = int((q-b)/a)
			for c in range(a-1, b-1, -1):
				ps[c+1] = ps[c]
			ps[b] = 7-a

		if m == 0:
			c=ps[0]
			ps[0]=ps[1]
			ps[1]=ps[3]
			ps[3]=ps[2]
			ps[2]=c
		elif m == 1:
			c=ps[0]
			ps[0]=ps[4]
			ps[4]=ps[5]
			ps[5]=ps[1]
			ps[1]=c
		elif m == 2:
			c=ps[0]
			ps[0]=ps[2]
			ps[2]=ps[6]
			ps[6]=ps[4]
			ps[4]=c

		q = 0
		for a in range(7):
			b = 0
			for c in range(7):
				if ps[c] == a:
					break
				if ps[c] > a:
					b += 1
			q = q*(7-a)+b
		return q

	def gettwsmv(self, p, m):
		a = None
		b = None
		c = None
		d = None
		q = None
		ps = [-1] * 7
		q = p
		d = 0
		for a in range(6):
			c = math.floor(q/3)
			b=q-3*c
			q=c
			ps[a]=b
			d-=b
			if d < 0:
				d += 3
		ps[6] = d
		if m == 0:
			c=ps[0]
			ps[0]=ps[1]
			ps[1]=ps[3]
			ps[3]=ps[2]
			ps[2]=c
		elif m == 1:
			c=ps[0]
			ps[0]=ps[4]
			ps[4]=ps[5]
			ps[5]=ps[1]
			ps[1]=c
			ps[0]+=2
			ps[1]+=1
			ps[5]+=2
			ps[4]+=1
		elif m == 2:
			c=ps[0]
			ps[0]=ps[2]
			ps[2]=ps[6]
			ps[6]=ps[4]
			ps[4]=c
			ps[2]+=2
			ps[0]+=1
			ps[4]+=2
			ps[6]+=1
		q= 0
		for a in range(5, -1, -1):
			q=q*3+(ps[a]%3)
		return q

	def update(self):
		CubeSolver.update(self)

		if self.stage:
			if self.currentAlgorithmSteps:
				return
			self.solved = True

		self.countAdjacentPairs()
		self.calcPerm()

		opp = [-1] * 6
		for a in range(6):
			for b in range(6):
				if a != b and self.adj[a][b]+self.adj[b][a]==0:
					opp[a] = b
					opp[b] = a

		# Each piece is determined by which of each pair of opposite colours it uses.
		ps = [-1] * 8
		tws = [-1] * 8
		a = 0
		for d in range(7):
			p = 0
			for b in range(a, a+6, 2):
				if self.posit[self.pieces[b]] == self.posit[self.pieces[42]]:
					p += 4
				if self.posit[self.pieces[b]] == self.posit[self.pieces[44]]:
					p += 1
				if self.posit[self.pieces[b]] == self.posit[self.pieces[46]]:
					p += 2
			ps[d] = p

			if self.posit[self.pieces[a]] == self.posit[self.pieces[42]] or self.posit[self.pieces[a]] == opp[self.posit[self.pieces[42]]]:
				tws[d] = 0
			elif self.posit[self.pieces[a+2]] == self.posit[self.pieces[42]] or self.posit[self.pieces[a+2]] == opp[self.posit[self.pieces[42]]]:
				tws[d] = 1
			else:
				tws[d] = 2
			a += 6
		# convert position to numbers
		q = 0
		for a in range(7):
			b = 0
			for c in range(7):
				if ps[c] == a:
					break
				if ps[c] > a:
					b += 1
			q = q * (7 - a) + b
		t = 0
		for a in range(5, -1, -1):
			t = t*3 + tws[a] - 3*math.floor(tws[a]/3)

		if q != 0 or t != 0:
			# Solution max len == 11
			for l in range(12):
				if self.search(0, q, t, l, -1):
					break

			# Process the solution
			for moveNum in self.sol:
				# 0x - U
				# 1x - R
				# 2x - F
				#
				# x0 - 1
				# x1 - 2
				# x2 - '
				if moveNum < 10: # U
					if moveNum % 10 == 0: # 1
						self.currentAlgorithmSteps += [(Cube.Top, 0)]
					elif moveNum % 10 == 1: # 2
						self.currentAlgorithmSteps += [(Cube.Top, 0), (Cube.Top, 0)]
					elif moveNum % 10 == 2: # '
						self.currentAlgorithmSteps += [(Cube.Top_, 0)]
					else: # ERR
						pass
				elif moveNum < 20: # R
					if moveNum % 10 == 0: # 1
						self.currentAlgorithmSteps += [(Cube.Right, 0)]
					elif moveNum % 10 == 1: # 2
						self.currentAlgorithmSteps += [(Cube.Right, 0), (Cube.Right, 0)]
					elif moveNum % 10 == 2: # '
						self.currentAlgorithmSteps += [(Cube.Right_, 0)]
					else: # ERR
						pass
				elif moveNum < 30: # F
					if moveNum % 10 == 0: # 1
						self.currentAlgorithmSteps += [(Cube.Front, 0)]
					elif moveNum % 10 == 1: # 2
						self.currentAlgorithmSteps += [(Cube.Front, 0), (Cube.Front, 0)]
					elif moveNum % 10 == 2: # '
						self.currentAlgorithmSteps += [(Cube.Front_, 0)]
					else: # ERR
						pass
				else: # ERR
					pass
		self.stage += 1

# 			print(t)
