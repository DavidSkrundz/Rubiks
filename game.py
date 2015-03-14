from button import TextButton, ImageButton
from cube import Cube
from cuberenderer import CubeRenderer
from cubesolveroptimal import CubeSolverOptimal
from cubesolverdavid import CubeSolverDavid
from cubehistoryrenderer import CubeHistoryRenderer
from runnable import Runnable
import pygame

class Game(Runnable):
	"""
	Manages the game loop and the rendering loop
	"""
	def __init__(self):
		Runnable.__init__(self)
		
		self.buttons = []
		# Some buttons
		self.buttons.append(TextButton((0, 0, 100, 60), "Reset", self.reset))
		self.buttons.append(TextButton((0, 61, 100, 60), "Scramble", self.scramble))
		self.buttons.append(TextButton((0, 122, 100, 60), "Solve", self.solve))

		# Cube controls
		buttonX = 120
		buttonY = 50
		buttonSize = 28
		
		self.buttons.append(ImageButton((buttonX + 0*(buttonSize + 1), buttonY + 0*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/U.png").convert(), lambda : self.__cube.U()))
		self.buttons.append(ImageButton((buttonX + 2*(buttonSize + 1), buttonY + 0*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/U_.png").convert(), lambda : self.__cube.U_()))
		
		self.buttons.append(ImageButton((buttonX + 1*(buttonSize + 1), buttonY + 0*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/C.png").convert(), lambda : self.__cube.C()))
		self.buttons.append(ImageButton((buttonX + 1*(buttonSize + 1), buttonY + 2*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/C_.png").convert(), lambda : self.__cube.C_()))
		
		self.buttons.append(ImageButton((buttonX + 2*(buttonSize + 1), buttonY + 2*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/D.png").convert(), lambda : self.__cube.D()))
		self.buttons.append(ImageButton((buttonX + 0*(buttonSize + 1), buttonY + 2*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/D_.png").convert(), lambda : self.__cube.D_()))
		
		self.buttons.append(ImageButton((buttonX + 5*(buttonSize + 1), buttonY + 1*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/F.png").convert(), lambda : self.__cube.F()))
		self.buttons.append(ImageButton((buttonX + 1*(buttonSize + 1), buttonY + 1*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/F_.png").convert(), lambda : self.__cube.F_()))
		
		self.buttons.append(ImageButton((buttonX + 4*(buttonSize + 1), buttonY + 2*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/L.png").convert(), lambda : self.__cube.L()))
		self.buttons.append(ImageButton((buttonX + 4*(buttonSize + 1), buttonY + 0*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/L_.png").convert(), lambda : self.__cube.L_()))
		
		self.buttons.append(ImageButton((buttonX + 2*(buttonSize + 1), buttonY + 1*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/M.png").convert(), lambda : self.__cube.M()))
		self.buttons.append(ImageButton((buttonX + 0*(buttonSize + 1), buttonY + 1*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/M_.png").convert(), lambda : self.__cube.M_()))
		
		self.buttons.append(ImageButton((buttonX + 6*(buttonSize + 1), buttonY + 0*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/R.png").convert(), lambda : self.__cube.R()))
		self.buttons.append(ImageButton((buttonX + 6*(buttonSize + 1), buttonY + 2*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/R_.png").convert(), lambda : self.__cube.R_()))
		
		
		self.__cube = None
		self.__historyRenderer = None

		self.__cubeSolver = None
		self.isSolving = None

		self.scrambleCounter = 0
		self.maxScramble = 24
		self.isPlaying = True
		self.wasScrambled = False

		self.reset()

	def reset(self):
		self.__cube = Cube(3)
		self.__historyRenderer = CubeHistoryRenderer(0, 183, 24, 300)

		self.__cubeSolver = None
		self.isSolving = False

		self.isPlaying = True
		self.wasScrambled = False

		self.scrambleCounter = 0

		pygame.mixer.music.fadeout(1)
		
	def scramble(self):
		if self.wasScrambled and self.__cube.isSolved():
			return
		if self.scrambleCounter == self.maxScramble:
			return
		
		self.scrambleCounter = 0
		self.isPlaying = False

		self.__cubeSolver = None
		self.isSolving = False

		self.__cube.moveHistory = []
		self.__cube.startTime = None
		self.__cube.endTime = None

	def solve(self):
		if self.__cube.isSolved():
			return
		
		self.wasScrambled = False
		self.isSolving = True

		self.__cube.moveHistory = []
		self.__cube.startTime = None
		self.__cube.endTime = None

# 		self.__cubeSolver = CubeSolverOptimal()
		self.__cubeSolver = CubeSolverDavid()
		self.__cubeSolver.solve(self.__cube)

	def scroll(self, up):
		"""
		1 for Up
		"""
		mouseX, mouseY = pygame.mouse.get_pos()
		if mouseX > self.__historyRenderer.x and mouseY > self.__historyRenderer.y and mouseX < self.__historyRenderer.x + self.__historyRenderer.surfaceWidth and mouseY < self.__historyRenderer.y + self.__historyRenderer.height:
			if up == 1:
				self.__historyRenderer.surfaceY = min(self.__historyRenderer.surfaceY + 10, self.__historyRenderer.surfaceHeight - self.__historyRenderer.height)
			else:
				self.__historyRenderer.surfaceY = max(self.__historyRenderer.surfaceY - 10, 0)

	def click(self, x, y, button, press):
		if press:
			for button in self.buttons:
				if x > button.rect[0] and x < button.rect[0] + button.rect[2]:
					if y > button.rect[1] and y < button.rect[1] + button.rect[3]:
						button.activate()

	def tick(self, keypressEvent):
		if self.isPlaying:
			if self.wasScrambled and self.__cube.isSolved():
				pass
				# Show win screen
			else:
				if self.isSolving and self.__cubeSolver:
					self.__cubeSolver.update()
					if self.__cubeSolver.solved and len(self.__cubeSolver.currentAlgorithmSteps) == 0:
						self.__cubeSolver = None
						self.isSolving = False
				else:
					# Handle the keypress event if it exists
					if keypressEvent:
						keyCode = keypressEvent.key
						if keyCode == pygame.K_q:
							self.__cube.U()
						elif keyCode == pygame.K_e:
							self.__cube.U_()
						elif keyCode == pygame.K_c:
							self.__cube.D()
						elif keyCode == pygame.K_z:
							self.__cube.D_()
						elif keyCode == pygame.K_h:
							self.__cube.F()
						elif keyCode == pygame.K_s:
							self.__cube.F_()
# 						elif keyCode == pygame.K_r:
# 							self.__cube.B()
# 						elif keyCode == pygame.K_v:
# 							self.__cube.B_()
						elif keyCode == pygame.K_b:
							self.__cube.L()
						elif keyCode == pygame.K_t:
							self.__cube.L_()
						elif keyCode == pygame.K_u:
							self.__cube.R()
						elif keyCode == pygame.K_m:
							self.__cube.R_()
						elif keyCode == pygame.K_w:
							self.__cube.C()
						elif keyCode == pygame.K_x:
							self.__cube.C_()
						elif keyCode == pygame.K_d:
							self.__cube.M()
						elif keyCode == pygame.K_a:
							self.__cube.M_()
						elif keyCode == pygame.K_j:
							self.__cube.T()
						elif keyCode == pygame.K_g:
							self.__cube.T_()
						elif keyCode == pygame.K_y:
							self.__cube.S()
						elif keyCode == pygame.K_n:
							self.__cube.S_()
		else:
			if self.scrambleCounter < self.maxScramble:
				self.__cube.randomize()
				self.scrambleCounter += 1
			else:
				self.isPlaying = True
				self.wasScrambled = True
		return True

	def render(self, screen):
		CubeRenderer().render(screen, self.__cube, 350, 0)
		self.__historyRenderer.render(screen, self.__cube)
		for button in self.buttons:
			button.render(screen)
