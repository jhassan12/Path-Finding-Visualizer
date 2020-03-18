import pygame
import threading
from constants import *
from thread import Thread
from pathfinding_algos import bfs, dfs, dijkstras, A_star

def init_grid(algorithm, rows, cols, tile_size):
	# Creates the start window and initializes the grid
	global window, WIDTH, HEIGHT, TILE_SIZE

	# Grid dimensions
	WIDTH = rows * tile_size
	HEIGHT = cols * tile_size
	DIMENSIONS = (WIDTH,HEIGHT)
	TILE_SIZE = tile_size

	# Initalizes Pygame
	pygame.init()

	# Creates the Window
	window = pygame.display.set_mode(DIMENSIONS)
	window.fill(BLACK)

	# Sets Caption
	pygame.display.set_caption("Path Finding Visualization")

	clock = pygame.time.Clock()
	
	grid = Grid(HEIGHT//TILE_SIZE,WIDTH//TILE_SIZE)
	grid.draw()

	placeObstacles = False
	isRunning = True
	thread = Thread()

	# Main loop
	while isRunning:
		# Handles events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				isRunning = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if not thread.isThreading:
					if event.button == 3:
						grid.handle(pygame.mouse.get_pos(), False)
					else:
						placeObstacles = True

			if event.type == pygame.MOUSEBUTTONUP:
				if placeObstacles:
					placeObstacles = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					grid.clear()

				if event.key == pygame.K_d:
					if not (grid.start and grid.finish):
						return

					start = grid.matrix[grid.start[0]][grid.start[1]]
					finish = grid.matrix[grid.finish[0]][grid.finish[1]]

					thread.turn_on()

					# Runs the pathfinding algortihm
					if algorithm == "Dijkstras":
						t1 = threading.Thread(target = dijkstras, args = (grid, start, finish, thread))
					elif algorithm == "A*":
						t1 = threading.Thread(target = A_star, args = (grid,thread))
					elif algorithm == "DFS":
						t1 = threading.Thread(target = dfs, args = (grid, thread))
					else:
						t1 = threading.Thread(target = bfs, args = (grid, thread))

					t1.start()
		
		if placeObstacles:
			grid.handle(pygame.mouse.get_pos(), True)

		clock.tick(FPS)

class Cell:
	def __init__(self,rect,c):
		self.rectangle = pygame.Rect(rect[0],rect[1],rect[2],rect[3])
		self.width = TILE_SIZE
		self.height = TILE_SIZE
		self.color = c
		self.parent = None
		self.X = 0
		self.Y = 0
		self.cost = 1
		self.g = float('inf')
		self.h = float('inf')
		self.f = float('inf')

	def draw(self):
		# Draws the cell onto the window
		pygame.draw.rect(window, self.color, (self.rectangle))
		pygame.display.update()

	def is_empty(self):
		return True if self.color == BLACK else False

	def is_start(self):
		return True if self.color == RED else False

	def is_finish(self):
		return True if self.color == GREEN else False

	def get_adjacent(self, grid, color = None):
		adjacent = []

		x = self.X
		y = self.Y

		g = grid.matrix

		# Does not include cells that represent walls and paths 
		exclude = {WALLS,PATH}

		if color:
			exclude.add(color)

		# Finds the adjacent cells that are empty
		if(x < len(g) - 1 and g[x+1][y].color not in exclude):
			adjacent.append(g[x+1][y])

		if(x < len(g) - 1 and y > 0 and g[x+1][y-1].color not in exclude):
			adjacent.append(g[x+1][y-1])

		if(y > 0 and g[x][y-1].color not in exclude):
			adjacent.append(g[x][y-1])

		if(x > 0 and y < len(g[0]) - 1 and g[x-1][y+1].color not in exclude):
			adjacent.append(g[x-1][y+1])

		if(x > 0 and g[x-1][y].color not in exclude):
			adjacent.append(g[x-1][y])

		if(x > 0 and y > 0 and g[x-1][y-1].color not in exclude):
			adjacent.append(g[x-1][y-1])

		if(y < len(g[0]) - 1 and g[x][y+1].color not in exclude):
			adjacent.append(g[x][y+1])

		if(x < len(g) - 1 and y < len(g[0]) - 1 and g[x+1][y+1].color not in exclude):
			adjacent.append(g[x+1][y+1])

		return adjacent

	def __str__(self):
		if (self.color == RED):
			return 'R'
		elif (self.color == GREEN):
			return 'G'
		elif (self.color == WALLS):
			return '-'
		else:
			return '.'

class Grid:
	def __init__(self,r,c):
		self.rows = r
		self.cols = c
		self.matrix = [[None for x in range(self.cols)] for y in range(self.rows)]
		self.start = None
		self.finish = None

	def fill_matrix(self):
		# Fills the grid with empty cells
		for r in range(len(self.matrix)):
			for c in range(len(self.matrix[0])):
				rect = pygame.Rect(r, c, TILE_SIZE, TILE_SIZE)
				cell = Cell(rect, BLACK)
				self.matrix[r][c] = cell
				cell.X = r
				cell.Y = c

	def draw(self):
		self.fill_matrix()

		# Draws the vertical grid lines
		for x in range(0,WIDTH,TILE_SIZE):
			pygame.draw.line(window, GRID, (x,0), (x,HEIGHT), 1)

		# Draws the horizontal grid lines
		for y in range(0,HEIGHT+1,TILE_SIZE):
			pygame.draw.line(window, GRID, (0,y), (WIDTH, y), 1)

		pygame.display.update()

	def remove(self, coords, pos):
		# Removes the cell at the specified location
		x, y = pos
		row, col = coords
		
		curr_cell = self.matrix[row][col]

		# Creates and draws empty cell in the place of the cell to be removed
		rect = pygame.Rect(x *  TILE_SIZE + 1, y * TILE_SIZE + 1,TILE_SIZE - 1, TILE_SIZE - 1)
		cell = Cell(rect,BLACK)
		cell.X, cell.Y = coords
		cell.draw()	

		if curr_cell.color == RED:
			self.start = None
		elif curr_cell.color == GREEN:
			self.finish = None

		self.matrix[row][col] = cell

		pygame.display.update()

	def place_cell(self, coords, pos, cell):
		# Places the cell in the grid
		x,y = pos
		row,col = coords

		cell.draw()

		self.matrix[row][col] = cell

		cell.X = row
		cell.Y = col

		if cell.color == RED:
			self.start = (row,col)
		elif cell.color == GREEN:
			self.finish = (row,col)

		pygame.display.update()

	def place_start(self, coords, pos):
		# Places the start cell
		x,y = pos
		rect = pygame.Rect(x *  TILE_SIZE + 1, y * TILE_SIZE + 1,TILE_SIZE - 1, TILE_SIZE - 1)
		cell = Cell(rect,RED)
		self.place_cell(coords, pos, cell)
		
	def place_finish(self, coords, pos):
		# Places the finish cell
		x,y = pos
		rect = pygame.Rect(x *  TILE_SIZE + 1, y * TILE_SIZE + 1,TILE_SIZE - 1, TILE_SIZE - 1)
		cell = Cell(rect,GREEN)
		self.place_cell(coords, pos, cell)

	def place_obstacle(self, coords, pos):
		# Places the obstacle cell
		x,y = pos
		rect = pygame.Rect(x * TILE_SIZE + 1, y * TILE_SIZE + 1, TILE_SIZE - 1, TILE_SIZE - 1)
		cell = Cell(rect,WALLS)
		self.place_cell(coords, pos, cell)

	def visit(self, c, color = None):
		# Visits the cell
		row = c.X
		col = c.Y

		if (self.matrix[row][col].color == RED) or (self.matrix[row][col].color == GREEN):
			return

		x = col
		y = row

		rect = pygame.Rect(x * TILE_SIZE + 1, y * TILE_SIZE + 1, TILE_SIZE - 1, TILE_SIZE - 1)

		# Marks the cell as visited with the color PATH
		if color:
			cell = Cell(rect, color)
		else:
			cell = Cell(rect, PATH)

		self.matrix[row][col] = cell
		cell.draw()

	def mark_path(self, c):
		# Marks the cell as part of the shortest path
		row = c.X
		col = c.Y

		if self.matrix[row][col].color == RED or self.matrix[row][col].color == GREEN:
			return

		x = col
		y = row

		# Marks the cell with the color FINAL_PATH
		rect = pygame.Rect(x * TILE_SIZE + 1, y * TILE_SIZE + 1, TILE_SIZE - 1, TILE_SIZE - 1)
		cell = Cell(rect,FINAL_PATH)
		cell.draw()

	def create_path(self, path):
		# Draws a line through the shortest path
		finish = self.matrix[self.finish[0]][self.finish[1]]

		prev = (finish.Y * TILE_SIZE + TILE_SIZE//2, finish.X * TILE_SIZE + TILE_SIZE//2)

		for cell in path:
			curr = (cell.Y * TILE_SIZE + TILE_SIZE//2, cell.X * TILE_SIZE + TILE_SIZE//2)
			pygame.draw.line(window, YELLOW, prev, curr, 3)

			prev = curr
		
		pygame.display.update()	


	def handle(self,pos, obstacle):
		# Processes the cell which the user clicked
		x,y = pos

		row = x//TILE_SIZE
		col = y//TILE_SIZE
	
		cell = self.matrix[col][row]

		coords = (col, row)
		pos = (row, col)

		leftVertical = row * TILE_SIZE
		topHorizontal = col * TILE_SIZE

		rect = pygame.Rect(leftVertical + 1, topHorizontal + 1, TILE_SIZE - 1, TILE_SIZE - 1)

		# Checks if the cell to be added is an obstacle
		if obstacle:
			# Does no further processing if the clicked cell is a start cell or a finish cell
			if cell.color == RED or cell.color == GREEN:
				return
			else:
				self.place_obstacle(coords, pos)
		else:
			# Draws the appropriate cell if the cell is empty otherwise removes the clicked cell
			if cell.is_empty():
				if not self.start:
					self.place_start(coords, pos)
				elif not self.finish:
					self.place_finish(coords, pos)
				else:
					self.remove(self.start, (self.start[1],self.start[0]))
					self.remove(self.finish, (self.finish[1], self.finish[0]))
					self.place_start(coords, pos)
			else:
				self.remove(coords,pos)

		# Updates the screen
		pygame.display.update()

	def clear(self):
		# Resets the grid
		window.fill(BLACK)
		self.draw()
		self.start = None
		self.finish = None
		self.fill_matrix()

	def clear_path(self):
		# Removes the cells that represent a path
		g = self.matrix

		for r in range(len(g)):
			for c in range(len(g[0])):
				cell = g[r][c]

				if cell.color == PATH:
					self.remove((r,c),(c,r))

	def __str__(self):
		result = ""

		for r in range(len(self.matrix)):
			for c in range(len(self.matrix[0])):
				cell = self.matrix[r][c]
				result += str(cell)
			result += '\n'

		return result
