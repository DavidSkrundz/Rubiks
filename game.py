from button import TextButton, ImageButton
from cube import Cube
from runnable import Runnable
from cubetimer import CubeTimer
from cuberenderer import CubeRenderer
import pygame
from pygame.mixer import Sound
from cubemoverenderer import CubeMoveRenderer

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

		self.buttons = []
		# Some buttons
# 		self.buttons.append(TextButton((0, 0, 100, 60), "Reset", self.reset))
# 		self.buttons.append(TextButton((0, 61, 100, 60), "Scramble", self.scramble))
# 		self.buttons.append(TextButton((0, 122, 100, 60), "Solve", self.solve))

# 		# Cube controls
# 		buttonX = 120
# 		buttonY = 50
# 		buttonSize = 28
# 		self.buttons.append(ImageButton((buttonX + 0*(buttonSize + 1), buttonY + 0*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/U.png").convert(), lambda : self.__cube.U()))
# 		self.buttons.append(ImageButton((buttonX + 2*(buttonSize + 1), buttonY + 0*(buttonSize + 1), buttonSize, buttonSize), pygame.image.load("assets/3x3/U_.png").convert(), lambda : self.__cube.U_()))

		self.__cube = None
# 		self.__cubeDoneUpdates = False
# 		self.__cubeTimer = CubeTimer()
		self.__cubeRenderer = CubeRenderer(350, 200)
#
# 		self.scrambleCounter = 26
# 		self.maxScramble = 26
# 		self.isPlaying = True
# 		self.wasScrambled = False
#
		self.reset()

	def reset(self):
		self.__cube = Cube(3)
		self.buttons = self.__cube.generateButtons(0, 0)
# 		self.playing = False
# 		self.__cubeTimer.reset()
# # 		self.__historyRenderer = CubeHistoryRenderer(0, 183, 24, 300)
#
# 		self.wasScrambled = False
# 		self.scrambleCounter = 26
#
# 		pygame.mixer.music.fadeout(1)
#
# 	def scramble(self):
# 		self.reset()
#
# 		self.scrambleCounter = 0
#
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
		self.__cubeRenderer.click(x, y, button, press)
		if press:
			for button in self.buttons:
				if x > button.rect[0] and x < button.rect[0] + button.rect[2]:
					if y > button.rect[1] and y < button.rect[1] + button.rect[3]:
						if self.__cube.update():
							button.activate()

	def tick(self, keypressEvent):
		return True
# 		if self.scrambleCounter == self.maxScramble:
# 			if self.__cube.update():
# 				self.__cubeDoneUpdates = True
# 				if self.__cube.isSolved() and self.playing:
# 					self.playing = False
# 					self.__cubeTimer.stop()
# 					# Play the VICTORY SOUND!!!
# 					winSound = Sound(file = "assets/audio/WIN.wav")
# 					winSound.play()
# 					pygame.mixer.music.fadeout(1)
# 		else:
# 			self.__cubeDoneUpdates = False
# 			if self.__cube.update():
# 				self.__cube.randomize()
# 				self.scrambleCounter += 1

# 				# Handle the keypress event if it exists
# 				if keypressEvent:
# 					keyCode = keypressEvent.key
# 					rotateFunction = None
# 					if keyCode == pygame.K_q:
# 						rotateFunction = self.__cube.U
# 					elif keyCode == pygame.K_e:
# 						rotateFunction = self.__cube.U_
# 					elif keyCode == pygame.K_c:
# 						rotateFunction = self.__cube.D
# 					elif keyCode == pygame.K_z:
# 						rotateFunction = self.__cube.D_
# 					elif keyCode == pygame.K_h:
# 						rotateFunction = self.__cube.F
# 					elif keyCode == pygame.K_s:
# 						rotateFunction = self.__cube.F_
# # 					elif keyCode == pygame.K_r:
# # 						rotateFunction = self.__cube.B
# # 					elif keyCode == pygame.K_v:
# # 						rotateFunction = self.__cube.B_
# 					elif keyCode == pygame.K_b:
# 						rotateFunction = self.__cube.L
# 					elif keyCode == pygame.K_t:
# 						rotateFunction = self.__cube.L_
# 					elif keyCode == pygame.K_u:
# 						rotateFunction = self.__cube.R
# 					elif keyCode == pygame.K_m:
# 						rotateFunction = self.__cube.R_
# 					elif keyCode == pygame.K_w:
# 						rotateFunction = self.__cube.C
# 					elif keyCode == pygame.K_x:
# 						rotateFunction = self.__cube.C_
# 					elif keyCode == pygame.K_d:
# 						rotateFunction = self.__cube.M
# 					elif keyCode == pygame.K_a:
# 						rotateFunction = self.__cube.M_
# 					elif keyCode == pygame.K_j:
# 						self.__cube.UUU()
# 					elif keyCode == pygame.K_g:
# 						self.__cube.UUU_()
# 					elif keyCode == pygame.K_y:
# 						self.__cube.RRR()
# 					elif keyCode == pygame.K_n:
# 						self.__cube.RRR_()

# 					if rotateFunction != None:
# 						self.__cubeDoneUpdates = False
# 						if not self.playing:
# 							self.playing = True
# 							self.__cubeTimer.reset()
# 							self.__cubeTimer.start()
# 							pygame.mixer.music.load("assets/audio/BGM.wav")
# 							pygame.mixer.music.play(loops=-1)
# 						rotateFunction()
# 			else:
# 				self.__cubeDoneUpdates = False

	def render(self, screen):
# 		CubeMoveRenderer.render(screen, 0, 0, 3, Cube.TurnUUU, 1)
# 		CubeMoveRenderer.render(screen, 0, 50, 3, Cube.TurnRRR_, [0,1])
# 		CubeMoveRenderer.render(screen, 50, 0, 3, Cube.Left, 0)
# 		CubeMoveRenderer.render(screen, 100, 0, 3, Cube.Front, 0)
# 		CubeMoveRenderer.render(screen, 50, 50, 4, Cube.Right_, [0, 1])
# 		CubeMoveRenderer.render(screen, 200, 200, 7, Cube.Center, [0, 1])

# 		self.__cubeTimer.render(screen, 100, 300)
		self.__cubeRenderer.render(screen, self.__cube)
		for button in self.buttons:
			button.render(screen)
