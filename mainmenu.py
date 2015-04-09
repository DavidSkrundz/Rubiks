from button import TextButton, ImageButton
from runnable import Runnable
import pygame
from pygame.event import Event
from cuberenderer import CubeRenderer
from cube import Cube
import game

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

class Menu(Runnable):
	def __init__(self, application):
		Runnable.__init__(self)

		self.RunningApplication = application
		self.RunningApplication.setCursor(handCursor, 5, 1)
		self.elements()

		self.cubeRenderer = CubeRenderer(700/2 - 50, 150)
		self.cube = Cube(1)

		self.size = None

		self.alive = True

	def elements(self):
		self.buttons = []
		self.buttons.append(TextButton((275,540,150,45), "Start Game", self.Start))
		self.buttons.append(TextButton((50, 440, 100, 60), "2x2x2", self.Size, 2))
		self.buttons.append(TextButton((150, 440, 100, 60), "3x3x3", self.Size, 3))
		self.buttons.append(TextButton((250, 440, 100, 60), "4x4x4", self.Size, 4))
		self.buttons.append(TextButton((350, 440, 100, 60), "5x5x5", self.Size, 5))
		self.buttons.append(TextButton((450, 440, 100, 60), "6x6x6", self.Size, 6))
		self.buttons.append(TextButton((550, 440, 100, 60), "7x7x7", self.Size, 7))

	def Start(self, args = None):
		if self.size:
			gameapp = game.Game(self.RunningApplication, self.size)
			self.RunningApplication.registerRunnable(gameapp)
			self.alive = False

	def click(self, x, y, button, press):
		if not press:
			self.RunningApplication.setCursor(handCursor, 5, 1)
			self.mouseMove(Event(4, {'pos': (x, y), 'buttons': (0, 0, 0), 'rel': (0, 0)}))
		if press:
			for button in self.buttons:
				if x > button.rect[0] and x < button.rect[0] + button.rect[2]:
					if y > button.rect[1] and y < button.rect[1] + button.rect[3]:
						button.activate()

	def mouseMove(self, event):
		# Check Mouse Cursor and whatnot
		self.RunningApplication.setCursor(handCursor, 5, 7)
		x = event.pos[0]
		y = event.pos[1]
		for button in self.buttons:
			if x > button.rect[0] and x < button.rect[0] + button.rect[2]:
				if y > button.rect[1] and y < button.rect[1] + button.rect[3]:
					self.RunningApplication.setCursor(handCursorClick, 5, 1)

	def tick(self, keypressEvent):
		self.cubeRenderer.slowlySpin(1)

		return self.alive

	def Size(self, args = None):
		self.size = args
		self.cube = Cube(self.size)

	def render(self, screen):
		for button in self.buttons:
			button.render(screen)

		if self.cube:
			self.cubeRenderer.render(screen, self.cube)
