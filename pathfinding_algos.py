import heapq
from collections import deque

def dfs(grid, thread):
	# Performs depth first search algorithm
	start = grid.matrix[grid.start[0]][grid.start[1]]
	finish = grid.matrix[grid.finish[0]][grid.finish[1]]
	stack = deque()
	stack.append(start)
	found = False

	while len(stack) > 0:
		# Grabs the cell from the top of the stack
		current = stack.pop()

		# Exits the loop if the finish cell has been found
		if current == finish:
			found = True
			break

		# Marks the current cell as visited and fetches its neighbors
		grid.visit(current)
		neighbors = current.get_adjacent(grid)
		for neighbor in neighbors:
			if neighbor not in stack:
				# Adds the neighbor to the stack
				neighbor.parent = current
				stack.append(neighbor)

	# Performs no more processing if the path has not been found
	if not found:
		print("Path Not Found!")
		thread.turn_off()
		return

	path = []
	current = finish.parent

	# Builds the path from start cell to finish cell
	while current and current != start:
		grid.mark_path(current)
		path.append(current)
		current = current.parent

	path.append(start)
	grid.create_path(path)

	thread.turn_off()
	
def bfs(grid, thread):
	# Performs breadth first search algorithm
	start = grid.matrix[grid.start[0]][grid.start[1]]
	finish = grid.matrix[grid.finish[0]][grid.finish[1]]
	queue = deque()
	queue.append(start)
	found = False

	while len(queue) > 0:
		# Grabs cell from front of queue
		current = queue.popleft()

		# Exits the loop if the finish cell has been found
		if current == finish:
			found = True
			break

		# Marks the current cell as visited and adds its neighbors to the queue.
		grid.visit(current)
		neighbors = current.get_adjacent(grid)
		for neighbor in neighbors:
			if neighbor not in queue:
				# Adds the neighbor to the queue
				neighbor.parent = current
				queue.append(neighbor)

	# Performs no more processing if the path has not been found
	if not found:
		print("Path Not Found!")
		thread.turn_off()
		return

	# Builds the path from start cell to finish cell
	path = []
	current = finish.parent
	while current and current != start:
		grid.mark_path(current)
		path.append(current)
		current = current.parent

	path.append(start)
	grid.create_path(path)

	thread.turn_off()

def dijkstras(grid, start, finish, thread):
	# Performs dijkstras algorithm
	costs = dict()
	visited = set()
	heap = []

	# Sets cost to get to every cell from the starting cell to infinity
	for r in range(len(grid.matrix)):
		for c in range(len(grid.matrix[0])):
			cell = grid.matrix[r][c]
			if cell.is_start():
				costs[cell] = 0
			else:
				costs[cell] = float('inf')

	# Creates an entry consisting of cost to get to current cell, coordinates on
	# the window, and the current cell object. Adds this entry to the min heap.
	entry = (costs[start], (start.X,start.Y), start)
	heapq.heappush(heap,entry)
	while len(heap) > 0 and finish not in visited:
		# Grabs the cell with the minimum cost
		cost,coords,cell = heapq.heappop(heap)
		if cell not in visited:
			# Visits the cell if it has not been visited
			grid.visit(cell)
			visited.add(cell)
			neighbors = cell.get_adjacent(grid)
			for neighbor in neighbors:
				if neighbor not in visited:
					# Calculates the cost to get to the neighbor cell
					total_cost = costs[cell] + neighbor.cost
					# Updates the cost of the neighbor cell if it is more than the totol cost
					if costs[neighbor] > total_cost:
						costs[neighbor] = total_cost
						neighbor.parent = cell
					entry = (costs[neighbor], (neighbor.X,neighbor.Y), neighbor)
					# Adds the entry associated with the neighbor to the min heap
					heapq.heappush(heap, entry)

	# Performs no more processing if the path has not been found
	if costs[finish] == float('inf'):
		print("Path Not Found!")
		thread.turn_off()
		return

	# Builds the shortest path from start cell to finish cell
	shortest_path = []
	current = finish.parent
	while current and current != start:
		grid.mark_path(current)
		shortest_path.append(current)
		current = current.parent
	shortest_path.append(start)
	grid.create_path(shortest_path)

	thread.turn_off()

def A_star(grid, thread):
	# Performs A* algorithm
	heap = []

	start = grid.matrix[grid.start[0]][grid.start[1]]
	finish = grid.matrix[grid.finish[0]][grid.finish[1]]

	start.g = 0
	start.h = abs(start.X - finish.X) + abs(start.Y - finish.Y)
	start.f = start.g + start.h


	# Creates an entry consisting of the f cost, coordinates of the cell on
	# the window, and the current cell object. Adds this entry to the min heap.
	entry = (start.f, (start.X,start.Y), start)
	heapq.heappush(heap, entry)

	found = False

	while len(heap) > 0:
		# Grabs the cell with the minimum cost
		f_cost,coords,current =  heapq.heappop(heap)

		# Exits the loop if the finish cell has been found
		if current == finish:
			found = True
			break

		# Visits the cell if it has not been visited
		if current != start:
			grid.visit(current)

		# Fetches the neighbors of the current cell
		neighbors = current.get_adjacent(grid)
		for neighbor in neighbors:	
			if neighbor.g > current.g + 1:
				# Calculates the g cost which represents the distance between the start cell and
				# the neighbor cell in in terms of tiles
				neighbor.g = current.g + 1
				# Calculates the h cost which is the Manhattan Distance between the neighbor cell and finish cell
				neighbor.h = abs(neighbor.X - finish.X) + abs(neighbor.Y - finish.Y)
				# Calculates the f cost which is the sum of the g cost and the h cost
				neighbor.f = neighbor.g + neighbor.h
				neighbor.parent = current

				if neighbor not in heap:
					# Adds the entry associated with the neighbor to the min heap
					heapq.heappush(heap, (neighbor.f,(neighbor.X,neighbor.Y),neighbor))
	
	# Performs no more processing if the path has not been found
	if not found:
		print("Path Not Found!")
		thread.turn_off()
		return
		
	# Builds the shortest path from start cell to finish cell
	shortest_path = []
	current = finish.parent
	while current and current != start:
		grid.mark_path(current)
		shortest_path.append(current)
		current = current.parent
	shortest_path.append(start)
	grid.create_path(shortest_path)

	thread.turn_off()
