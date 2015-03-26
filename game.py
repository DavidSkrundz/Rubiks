from button import TextButton, ImageButton
from cube import Cube
from runnable import Runnable
from cuberenderer import CubeRenderer
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

		self.reset()

	def reset(self):
		self.__cube = Cube()
		self.__cubeRenderer = CubeRenderer()
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

	def click(self, x, y, button, press):
		if press:
			for button in self.buttons:
				if x > button.rect[0] and x < button.rect[0] + button.rect[2]:
					if y > button.rect[1] and y < button.rect[1] + button.rect[3]:
						if self.__cube.update():
							button.activate()

	def tick(self, keypressEvent):
		# Handle the keypress event if it exists
# 		if self.__cube.isSolved():
# 			print("solved")
		if self.__cube.update():
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
# 				elif keyCode == pygame.K_r:
# 					self.__cube.B()
# 				elif keyCode == pygame.K_v:
# 					self.__cube.B_()
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
					self.__cube.UUU()
				elif keyCode == pygame.K_g:
					self.__cube.UUU_()
				elif keyCode == pygame.K_y:
					self.__cube.RRR()
				elif keyCode == pygame.K_n:
					self.__cube.RRR_()
		return True

	def render(self, screen):
		self.__cubeRenderer.render(screen, self.__cube, 350, 200)
		for button in self.buttons:
			button.render(screen)
