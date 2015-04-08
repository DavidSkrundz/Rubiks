from application import Application
from game import Game
from mainmenu import Menu
import pygame

app = Application()
app.initWindow(700, 700)
app.setWindowTitle("Rubik's Cube")

appIcon = pygame.image.load("assets/FreshCube.png").convert()
app.setAppIcon(appIcon)

app.setFrameRate(30)

N = 3
game = Game(app, N)
mainmenu = Menu(app)
app.registerRunnable(mainmenu)


app.run()
