from button import TextButton, ImageButton
from cube import Cube
from runnable import Runnable
from cuberenderer import CubeRenderer
import pygame
from pygame.mixer import Sound
from pygame.event import Event
from cubemoverenderer import CubeMoveRenderer
from searchsolver import SearchSolver
from cubehistoryrenderer import CubeHistoryRenderer

handCursor = (
	"                        ",
	"                        ",
	"                        ",
	"                        ",
	"                        ",
	"        ..              ",
	"     ...XX...           ",
	"    .XX.XX.XX..         ",
	"    .XX.XX.XX.X.        ",
	"... .XX.XX.XX.XX.       ",
	".XX..XXXXXXXX.XX.       ",
	".XXX.XXXXXXXXXXX.       ",
	" .XXXXXXXXXXXXXX.       ",
	"  .XXXXXXXXXXXXX.       ",
	"  .XXXXXXXXXXXXX.       ",
	"   .XXXXXXXXXXXX.       ",
	"   .XXXXXXXXXXX.        ",
	"    .XXXXXXXXXX.        ",
	"    .XXXXXXXXXX.        ",
	"     .XXXXXXXX.         ",
	"     .XXXXXXXX.         ",
	"     ..........         ",
	"                        ",
	"                        ")

handCursorClick = (
	"     ..                 ",
	"    .XX.                ",
	"    .XX.                ",
	"    .XX.                ",
	"    .XX.                ",
	"    .XX...              ",
	"    .XX.XX...           ",
	"    .XX.XX.XX..         ",
	"    .XX.XX.XX.X.        ",
	"... .XX.XX.XX.XX.       ",
	".XX..XXXXXXXX.XX.       ",
	".XXX.XXXXXXXXXXX.       ",
	" .XXXXXXXXXXXXXX.       ",
	"  .XXXXXXXXXXXXX.       ",
	"  .XXXXXXXXXXXXX.       ",
	"   .XXXXXXXXXXXX.       ",
	"   .XXXXXXXXXXX.        ",
	"    .XXXXXXXXXX.        ",
	"    .XXXXXXXXXX.        ",
	"     .XXXXXXXX.         ",
	"     .XXXXXXXX.         ",
	"     ..........         ",
	"                        ",
	"                        ")


class Game(Runnable):
	"""
	Manages the game loop and the rendering loop
	"""
	def __init__(self, application):
		Runnable.__init__(self)

		self.RunningApplication = application
		self.RunningApplication.setCursor(handCursor, 5, 1)

		self.buttons = None

		self.__cube = None
		self.__cubeRenderer = None

		self.scrambleCounter = None
		self.maxScramble = None
		self.wasScrambled = None

		self.reset()

	def reset(self, arg=None):
		N = 5
		self.__cube = Cube(N)
		self.__cubeRenderer = CubeRenderer(200, 100)

		self.buttons = []
		self.buttons.append(TextButton((0, 0, 100, 60), "Reset", self.reset))
		self.buttons.append(TextButton((0, 61, 100, 60), "Scramble", self.scramble))

		if N == 2:
			self.buttons.append(TextButton((0, 122, 100, 60), "Solve", self.solve))
		self.buttons += self.__cube.generateButtons(400, 0)

		self.music = False

		self.playing = True
		self.isPlaying = False
		self.didPlay = False
		self.wasNotSolved = False
		self.__historyRenderer = CubeHistoryRenderer(0, 400, 700, 300)

		self.solving = False
		self.cubeSolver = None

		self.wasScrambled = False
		self.maxScramble = 15*N
		self.scrambleCounter = self.maxScramble

		pygame.mixer.music.fadeout(1)

	def scramble(self, arg=None):
		self.reset()
		self.scrambleCounter = 0

	def solve(self, arg=None):
		self.solving = True
		self.cubeSolver = SearchSolver()
		self.cubeSolver.solve(self.__cube)

	def scroll(self, up):
		"""
		1 for Up
		"""
		mouseX, mouseY = pygame.mouse.get_pos()
# 		if mouseX > self.__historyRenderer.x and mouseY > self.__historyRenderer.y and mouseX < self.__historyRenderer.x + self.__historyRenderer.surfaceWidth and mouseY < self.__historyRenderer.y + self.__historyRenderer.height:
# 			if up == 1:
# 				self.__historyRenderer.surfaceY = min(self.__historyRenderer.surfaceY + 10, self.__historyRenderer.surfaceHeight - self.__historyRenderer.height)
# 			else:
# 				self.__historyRenderer.surfaceY = max(self.__historyRenderer.surfaceY - 10, 0)

	def mouseMove(self, event):
		self.__cubeRenderer.mouseMove(event.pos[0], event.pos[1], event.rel[0], event.rel[1])
		# Check Mouse Cursor and whatnot
		self.RunningApplication.setCursor(handCursor, 5, 7)
		if self.__cubeRenderer.mouseOver(event.pos[0], event.pos[1]):
			self.RunningApplication.setCursor(handCursorClick, 5, 1)
		x = event.pos[0]
		y = event.pos[1]
		for button in self.buttons:
			if x > button.rect[0] and x < button.rect[0] + button.rect[2]:
				if y > button.rect[1] and y < button.rect[1] + button.rect[3]:
					self.RunningApplication.setCursor(handCursorClick, 5, 1)

	def click(self, x, y, button, press):
		if not press:
			self.RunningApplication.setCursor(handCursor, 5, 1)
			self.mouseMove(Event(4, {'pos': (x, y), 'buttons': (0, 0, 0), 'rel': (0, 0)}))
		self.__cubeRenderer.click(x, y, button, press)
		if press:
			for button in self.buttons:
				if x > button.rect[0] and x < button.rect[0] + button.rect[2]:
					if y > button.rect[1] and y < button.rect[1] + button.rect[3]:
						button.activate()

	def tick(self, keypressEvent):
		if self.solving == True and not self.cubeSolver.solved:
			self.cubeSolver.update()
			return
		if self.scrambleCounter == self.maxScramble:
			# The user may have control over the cube
			if self.isPlaying:
				self.__cube.update()
				# The user has control over the cube
				if self.playing:
					if not self.__cube.isSolved():
						self.wasNotSolved = True
					if self.__cube.isSolved() and self.__cube.ready and self.wasNotSolved:
						self.playing = False
# 						# Play the VICTORY SOUND!!!
# 						winSound = Sound(file = "assets/audio/WIN.wav")
# 						winSound.play()
# 						pygame.mixer.music.fadeout(1)
# 						self.music = False
					else:
						# Handle user input
						if keypressEvent:
							keyCode = keypressEvent.key
							rotateFunction = None
							if keyCode == pygame.K_q:
								rotateFunction = self.__cube.U
							elif keyCode == pygame.K_e:
								rotateFunction = self.__cube.U_
							elif keyCode == pygame.K_c:
								rotateFunction = self.__cube.D
							elif keyCode == pygame.K_z:
								rotateFunction = self.__cube.D_
							elif keyCode == pygame.K_h:
								rotateFunction = self.__cube.F
							elif keyCode == pygame.K_s:
								rotateFunction = self.__cube.F_
							elif keyCode == pygame.K_b:
								rotateFunction = self.__cube.L
							elif keyCode == pygame.K_t:
								rotateFunction = self.__cube.L_
							elif keyCode == pygame.K_u:
								rotateFunction = self.__cube.R
							elif keyCode == pygame.K_m:
								rotateFunction = self.__cube.R_
							elif keyCode == pygame.K_w:
								rotateFunction = self.__cube.C
							elif keyCode == pygame.K_x:
								rotateFunction = self.__cube.C_
							elif keyCode == pygame.K_d:
								rotateFunction = self.__cube.M
							elif keyCode == pygame.K_a:
								rotateFunction = self.__cube.M_
							elif keyCode == pygame.K_j:
								self.__cube.UUU_()
							elif keyCode == pygame.K_g:
								self.__cube.UUU()
							elif keyCode == pygame.K_y:
								self.__cube.RRR()
							elif keyCode == pygame.K_n:
								self.__cube.RRR_()
							if rotateFunction != None:
								if not self.music:
									self.music = True
# 									pygame.mixer.music.load("assets/audio/BGM.wav")
# 									pygame.mixer.music.play(loops=-1)
								rotateFunction(0)
				else:
					# The User does not have control over the cube
					pass
			else:
				if self.__cube.update():
					# The animation of scrambling is done
					self.isPlaying = True
		else:
			# Scramble
			while self.scrambleCounter < self.maxScramble:
				self.__cube.randomize()
				self.scrambleCounter += 1
			self.wasScrambled = True
			self.isPlaying = False

	def render(self, screen):
		self.__cubeRenderer.render(screen, self.__cube)
		self.__cube.cubeTimer.render(screen, 100, 0)
		for button in self.buttons:
			button.render(screen)
