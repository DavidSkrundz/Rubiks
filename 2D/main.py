from application import Application
from game import Game
import pygame

handCursor = (
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

app = Application()
app.initWindow(600, 483)
app.setWindowTitle("Rubik's Cube")

appIcon = pygame.image.load("../assets/FreshCube.png").convert()
app.setAppIcon(appIcon)

app.setFrameRate(30)
app.setCursor(handCursor, 5, 1)

game = Game()
app.registerRunnable(game)

app.run()
