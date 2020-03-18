from tkinter import font
from tkinter import ttk
from grid import init_grid
from constants import RED
import tkinter as tk
import pygame

class TK:
	def __init__(self):
		# Initialize starting window
		self.root = tk.Tk()
		self.root.configure(background='black')
		self.root.title("Path Finding Visualizer")
		self.center_window()
		self.root.geometry("500x400")

		# Fonts
		self.title_font = font.Font(family="Helvetica", size=32)
		self.font = font.Font(family="Helvetica", size=18)

		# Labels
		self.title = tk.Label(self.root, text = "Path Finding Visualizer",fg = "red", bg = "black", font = self.title_font)
		self.algorithm = tk.Label(self.root, text = "Path Finding Algorithm: ",fg = "white", bg = "black", font = self.font)
		self.size_label = tk.Label(self.root, text = "Grid Size:  ", fg = "white", bg = "black", font = self.font)
		self.tile_size_label = tk.Label(self.root, text = "Tile Size:  ", fg = "white", bg = "black", font = self.font)

		# Choices
		self.algos = ["Dijkstras", "A*", "DFS", "BFS"]
		self.sizes = ["10x10", "25x25", "40x40"]

		# Inputs
		self.selected_size = tk.StringVar()
		self.selected_algorithm = tk.StringVar()
		self.selected_tile_size = tk.StringVar()
		self.selected_size.set(self.sizes[0])
		self.selected_algorithm.set(self.algos[0])

		self.combo = ttk.Combobox(self.root, values = self.algos, textvariable = self.selected_algorithm)
		self.grid_size = ttk.Combobox(self.root, values = self.sizes, textvariable = self.selected_size)
		self.button = tk.Button(self.root, text = "Start", bg = "black", fg = "white", width = 20, command = self.set_vars)
		self.tile_size = tk.Entry(self.root, width = 10, textvariable = self.selected_tile_size)
		self.tile_size.insert(tk.END,"50")

		self.place_elements()

	def center_window(self):
		# Gets the requested values of the height and widht.
		windowWidth = self.root.winfo_reqwidth()
		windowHeight = self.root.winfo_reqheight()
		 
		# Gets both half the screen width/height and window width/height
		positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2) - 100
		positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2) - 150
		 
		# Positions the window in the center of the page.
		self.root.geometry("+{}+{}".format(positionRight, positionDown))

	def place_elements(self):
		# Places the graphical components in the window
		self.title.place(relx = 0.15, rely = 0.10)
		self.algorithm.place(relx = 0.10, rely = 0.35)
		self.tile_size_label.place(relx = 0.10, rely = 0.55)
		self.size_label.place(relx = 0.10, rely = 0.45)
		self.tile_size.place(relx = 0.30, rely = 0.55)
		self.grid_size.place(relx = 0.30, rely = 0.45)
		self.combo.place(relx = 0.50, rely = 0.35)
		self.button.place(relx = 0.30, rely = 0.75)
		
	def run(self):
		self.root.protocol("WM_DELETE_WINDOW", self.shutdown)
		self.selected_tile_size.trace("w", self.reset_background_color)
		self.root.mainloop()

	def reset_background_color(self, *args):
		if self.tile_size["background"] == "red":
			self.tile_size.configure({"background": "white"})	

	def set_vars(self):
		# Fetches the options the user selected
		algorithm = self.combo.get()
		rows, cols = (int(self.grid_size.get().split("x")[0]), int(self.grid_size.get().split("x")[1]))

		# Error handling for tile size input
		try:
			tile_size = int(self.tile_size.get())

			# Shutdowns the starting window and begins the main program
			self.shutdown()

			print("Starting Application...")
			print("Successfully Loaded!")

			init_grid(algorithm, rows, cols, tile_size)
		except ValueError:
			print("Please enter a number!")
			self.tile_size.configure({"background": "red"})	

	def shutdown(self):
		self.root.eval('::ttk::CancelRepeat')
		self.root.destroy()
