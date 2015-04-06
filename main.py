from application import Application
from game import Game
import pygame

app = Application()
app.initWindow(700, 700)
app.setWindowTitle("Rubik's Cube")

appIcon = pygame.image.load("assets/FreshCube.png").convert()
app.setAppIcon(appIcon)

app.setFrameRate(30)

game = Game(app)
app.registerRunnable(game)

app.run()
