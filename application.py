import pygame

class Application:
	"""
	The base application object that manages lifecycle of the program and the window
	"""
	def __init__(self):
		# Initialize pygame
		pygame.init()
		# A list of syncronous tasks to keep in the run loop
		# Must be a runnable
		self.runnables = []
		self.frameRate = 1 # Default value
		self.screen = None # Gets set when the window size gets set
		# Event queue for keypresses
		self.keypressEventQueue = []

	def initWindow(self, width, height):
		self.screen = pygame.display.set_mode([width, height])

	def setAppIcon(self, icon):
		pygame.display.set_icon(icon)

	def setWindowTitle(self, title):
		pygame.display.set_caption(title)

	def setFrameRate(self, frameRate):
		self.frameRate = frameRate

	def setCursor(self, cursorTextTuple, centerX, centerY):
		"""
		Sets the cursor to the image.
		Black: '.'
		White: 'X'
		XOR  : 'o'
		None : ' '

		Each line in the tuple should be as long as the lengh of the tuple.
		The width and height should be divisible by 8
		"""
		width = len(cursorTextTuple)
		height = len(cursorTextTuple[0])
		dataTuple, maskTuple = pygame.cursors.compile(cursorTextTuple, black='.', white='X', xor='o')
		pygame.mouse.set_cursor((width, height), (centerX, centerY), dataTuple, maskTuple)

	def registerRunnable(self, runnable):
		self.runnables.append(runnable)

	def run(self):
		"""
		This method runs the game loop and should be the last call in the python file.
		Runs as long as the process is running, then stops
		"""
		# Get a clock from pygame to timekeeping
		clock = pygame.time.Clock()
		clock.tick(self.frameRate) # Tick to callibrate

		# The loop where it all happens
		running = True
		while running:
			# Make sure we have something to run
			if len(self.runnables) == 0:
				break

			# Handle OS events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					# User has quit the program (quit program or closed window)
					running = False
					break
				# elif event.type == pygame.ACTIVEEVENT:
				# 	pass
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q and event.mod == 1024: # Command-Q
						running = False
					self.keypressEventQueue.append(event)
				# elif event.type == pygame.KEYUP:
				# 	pass
				# elif event.type == pygame.MOUSEMOTION:
				# 	pass
				# elif event.type == pygame.MOUSEBUTTONUP:
				# 	pass
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 4: # Scroll Down
						for runnable in self.runnables:
							runnable.scroll(2)
					elif event.button == 5: # Scroll Up
						for runnable in self.runnables:
							runnable.scroll(1)
					elif event.button == 1 or event.button == 3:
						for runnable in self.runnables:
							x, y = event.pos
							runnable.click(x, y, event.button, True)
				# elif event.type == pygame.JOYAXISMOTION:
				# 	pass
				# elif event.type == pygame.JOYBALLMOTION:
				# 	pass
				# elif event.type == pygame.JOYHATMOTION:
				# 	pass
				# elif event.type == pygame.JOYBUTTONUP:
				# 	pass
				# elif event.type == pygame.JOYBUTTONDOWN:
				# 	pass
				# elif event.type == pygame.VIDEORESIZE:
				# 	pass
				# elif event.type == pygame.VIDEOEXPOSE:
				# 	pass
				# elif event.type == pygame.USEREVENT:
				# 	pass

			# Get the current keypress event
			currentKeyPressEvent = None
			if self.keypressEventQueue:
				currentKeyPressEvent = self.keypressEventQueue.pop()
			# Tick
			runnableIndex = 0
			while runnableIndex < len(self.runnables):
				runnable = self.runnables[runnableIndex]
				if runnable.tick(currentKeyPressEvent) == False:
					self.runnables.remove(runnable)
				else:
					runnableIndex += 1

			# Render
			for runnable in self.runnables:
				self.screen.fill((0,0,0))
				runnable.render(self.screen)
			pygame.display.flip() # Draw what was drawn this frame to the screen

			# Finally tick() so we can limit the framerate
			clock.tick(self.frameRate)

		# After the application stops running, do some cleanup
		pygame.quit()
