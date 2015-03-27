from button import TextButton, ImageButton
from cube import Cube
from runnable import Runnable
from cubetimer import CubeTimer
from cuberenderer import CubeRenderer
import pygame
from pygame.mixer import Sound

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
		self.buttons.append(TextButton((0, 0, 100, 60), "Reset", self.reset))
# 		self.buttons.append(TextButton((0, 61, 100, 60), "Scramble", self.scramble))
# 		self.buttons.append(TextButton((0, 122, 100, 60), "Solve", self.solve))

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
		self.__cubeTimer = CubeTimer()
		self.__cubeRenderer = CubeRenderer(350, 200)

		self.reset()

	def reset(self):
		self.__cube = Cube()
		self.playing = False
		self.__cubeTimer.reset()
# 		self.__historyRenderer = CubeHistoryRenderer(0, 183, 24, 300)

		pygame.mixer.music.fadeout(1)

	def scroll(self, up):
		"""
		1 for Up
		"""
# 		mouseX, mouseY = pygame.mouse.get_pos()
# 		if mouseX > self.__historyRenderer.x and mouseY > self.__historyRenderer.y and mouseX < self.__historyRenderer.x + self.__historyRenderer.surfaceWidth and mouseY < self.__historyRenderer.y + self.__historyRenderer.height:
# 			if up == 1:
# 				self.__historyRenderer.surfaceY = min(self.__historyRenderer.surfaceY + 10, self.__historyRenderer.surfaceHeight - self.__historyRenderer.height)
# 			else:
# 				self.__historyRenderer.surfaceY = max(self.__historyRenderer.surfaceY - 10, 0)

	def mouseMove(self, event):
		# Check Mouse Cursor and whatnot
		if self.__cubeRenderer.mouseOver(event.pos[0], event.pos[1]):
			self.RunningApplication.setCursor(handCursorClick, 5, 1)
		else:
			self.RunningApplication.setCursor(handCursor, 5, 1)
		self.__cubeRenderer.mouseMove(event.pos[0], event.pos[1], event.rel[0], event.rel[1])

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
		if self.__cube.update():
			if self.__cube.isSolved() and self.playing:
				self.playing = False
				self.__cubeTimer.stop()
				# Play the VICTORY SOUND!!!
				winSound = Sound(file = "assets/audio/WIN.wav")
				winSound.play()
				pygame.mixer.music.fadeout(1)

			# Handle the keypress event if it exists
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
# 				elif keyCode == pygame.K_r:
# 					rotateFunction = self.__cube.B
# 				elif keyCode == pygame.K_v:
# 					rotateFunction = self.__cube.B_
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
					self.__cube.UUU()
				elif keyCode == pygame.K_g:
					self.__cube.UUU_()
				elif keyCode == pygame.K_y:
					self.__cube.RRR()
				elif keyCode == pygame.K_n:
					self.__cube.RRR_()

				if rotateFunction != None:
					if self.__cube.isSolved() and not self.playing:
						self.playing = True
						self.__cubeTimer.reset()
						self.__cubeTimer.start()
						pygame.mixer.music.load("assets/audio/BGM.wav")
						pygame.mixer.music.play(loops=-1)
					rotateFunction()
		return True

	def render(self, screen):
		self.__cubeTimer.render(screen, 100, 300)
		self.__cubeRenderer.render(screen, self.__cube)
		for button in self.buttons:
			button.render(screen)
