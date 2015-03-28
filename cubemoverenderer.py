import pygame
from pygame import Color
from cube import Cube
from math import pi

Black = Color(000, 000, 000, 1)
White = Color(255, 255, 255, 1)

class CubeMoveRenderer:
	VertivalMoves = [
						Cube.Left,
						Cube.Left_,

						Cube.Right,
						Cube.Right_,

						Cube.Center,
						Cube.Center_,

						Cube.TurnRRR,
						Cube.TurnRRR_
					]
	FrontMoves = [
					Cube.Front,
					Cube.Front_
				]

	def size(N):
		return 4 + 5*N + 4

	def render(screen, x, y, N, move, offSets):
		if move == Cube.TurnRRR:
			move = Cube.Right
			offSets = [i for i in range(N)]
		if move == Cube.TurnRRR_:
			move = Cube.Right_
			offSets = [i for i in range(N)]
		if move == Cube.TurnUUU:
			move = Cube.Top
			offSets = [i for i in range(N)]
		if move == Cube.TurnUUU_:
			move = Cube.Top_
			offSets = [i for i in range(N)]

		try:
			a = offSets[0]
		except:
			offSets = [offSets]

		# Draw the background and border
		pygame.draw.rect(screen, White, (x, y, CubeMoveRenderer.size(N), CubeMoveRenderer.size(N)), 0)
		pygame.draw.rect(screen, Black, (x, y, CubeMoveRenderer.size(N), CubeMoveRenderer.size(N)), 1)

		# Draw the lines
		for i in range(N):
			if move in CubeMoveRenderer.VertivalMoves:
				pygame.draw.line(screen, Black, (x + 4 + 2 + 5*i, y + CubeMoveRenderer.size(N) - 1 - 5), (x + 4 + 2 + 5*i, y + 5), 1)
			elif move in CubeMoveRenderer.FrontMoves:
				pygame.draw.circle(screen, Black, (x + int(CubeMoveRenderer.size(N) / 2) + 1, y + int(CubeMoveRenderer.size(N) / 2) + 1), int(CubeMoveRenderer.size(N) / 2) - 4 + 1, 1)
				pygame.draw.polygon(screen, White, [(x + int(CubeMoveRenderer.size(N) / 2), y + int(CubeMoveRenderer.size(N) / 2)), (x + 1, y + CubeMoveRenderer.size(N) - 3 - 1), (x + CubeMoveRenderer.size(N) - 1 - 1, y + CubeMoveRenderer.size(N) - 1 - 1)], 0)
			else:
				pygame.draw.line(screen, Black, (x + 5, y + 4 + 2 + 5*i), (x + CubeMoveRenderer.size(N) - 1 - 5, y + 4 + 2 + 5*i), 1)

		# Draw the arrows
		if move in CubeMoveRenderer.VertivalMoves:
			point1x = x + 4 + 2
			point2x = x + 4
			point3x = x + 4 + 4
			point1y = 4
			point2y = 8
			point3y = 8
			if move >= 0:
				point1y += y
				point2y += y
				point3y += y
			else:
				point1y = y + CubeMoveRenderer.size(N) - 1 - point1y
				point2y = y + CubeMoveRenderer.size(N) - 1 - point2y
				point3y = y + CubeMoveRenderer.size(N) - 1 - point3y
			if move == Cube.Center or move == Cube.Center_:
				newOffSets = []
				if N % 2 == 0:
					for i in offSets:
						newOffSets.append(int(N / 2) - 1 - i)
						newOffSets.append(int(N / 2) + 0 + i)
				else:
					for i in offSets:
						newOffSets.append(int(N / 2) - i)
						newOffSets.append(int(N / 2) + i)
				offSets = newOffSets
			for j in offSets:
				i = j
				if move == Cube.Right or move == Cube.Right_:
					i = N - i - 1
				pygame.draw.polygon(screen, Black, [(point1x + i*5, point1y), (point2x + i*5, point2y), (point3x + i*5, point3y)], 0)
		elif move in CubeMoveRenderer.FrontMoves:
			if move >= 0:
				point1 = (x + CubeMoveRenderer.size(N) - 1 - 4, y + CubeMoveRenderer.size(N) - 1 - 5)
				point2 = (x + CubeMoveRenderer.size(N) - 1 - 9, y + CubeMoveRenderer.size(N) - 1 - 3)
				point3 = (x + CubeMoveRenderer.size(N) - 1 - 7, y + CubeMoveRenderer.size(N) - 1 - 8)
				point4 = (x + CubeMoveRenderer.size(N) - 1 - 6, y + CubeMoveRenderer.size(N) - 1 - 6)
			else:
				point1 = (x + 4, y + CubeMoveRenderer.size(N) - 1 - 5)
				point2 = (x + 9, y + CubeMoveRenderer.size(N) - 1 - 3)
				point3 = (x + 7, y + CubeMoveRenderer.size(N) - 1 - 8)
				point4 = (x + 6, y + CubeMoveRenderer.size(N) - 1 - 6)
			pygame.draw.polygon(screen, Black, [point1, point2, point3, point4], 0)
		else:
			point1y = y + 4 + 2
			point2y = y + 4
			point3y = y + 4 + 4
			point1x = 4
			point2x = 8
			point3x = 8
			if move >= 0:
				point1x += x
				point2x += x
				point3x += x
			else:
				point1x = x + CubeMoveRenderer.size(N) - 1 - point1x
				point2x = x + CubeMoveRenderer.size(N) - 1 - point2x
				point3x = x + CubeMoveRenderer.size(N) - 1 - point3x
			if move == Cube.Middle or move == Cube.Middle_:
				newOffSets = []
				if N % 2 == 0:
					for i in offSets:
						newOffSets.append(int(N / 2) - 1 - i)
						newOffSets.append(int(N / 2) + 0 + i)
				else:
					for i in offSets:
						newOffSets.append(int(N / 2) - i)
						newOffSets.append(int(N / 2) + i)
				offSets = newOffSets
			for j in offSets:
				i = j
				if move == Cube.Bottom or move == Cube.Bottom_:
					i = N - i - 1
				pygame.draw.polygon(screen, Black, [(point1x, point1y + i*5), (point2x, point2y + i*5), (point3x, point3y + i*5)], 0)
