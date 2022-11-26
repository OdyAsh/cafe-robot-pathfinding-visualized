from tkinter import Frame, Canvas, StringVar, Button, messagebox, ttk, Scale, HORIZONTAL, W
from functools import partial

import globals
from Spot import Spot
from Algorithms import Algorithms
from MazeGeneration import MazeGeneration

class Gui:

    def ui():
        # left_side_bar == Left column of application that contains buttons for the maze type, chosen algorithm, and instructions
        globals.left_side_bar = Frame(globals.root, width=600, height=200, bg='black')
        globals.left_side_bar.grid(row=0, column=0, padx=10, pady=5)
            
        # create grid_canvas, "grid_canvas" == Middle area of application that contains the "maze"
        globals.grid_canvas = Canvas(globals.root, width=globals.WIDTH, height=globals.WIDTH, bg='orange')
        globals.grid_canvas.grid(row=0, column=1, padx=10, pady=5) 

        # Create grid
        globals.grid = Gui.make_grid(globals.WIDTH, globals.ROWS)

        # UI elements for left_side_bar
        
        globals.bldMenu = ttk.Combobox(globals.left_side_bar, textvariable=globals.selected_bld, 
                            values=['Random walls', 'Circular maze', 'Carved out maze'], font = globals.font)
        globals.bldMenu.grid(row=0, column=0, padx=5, pady=(10, 5))
        globals.bldMenu.current(0)
        globals.bldMenu.bind("<<ComboboxSelected>>", MazeGeneration.scale_action)
        globals.wallsScale = Scale(globals.left_side_bar, from_=10, to=40, resolution=5, orient=HORIZONTAL, 
                        label='Obstacles density', font = globals.font, length=180)
        globals.wallsScale.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        Button(globals.left_side_bar, text='Build maze', command=partial(MazeGeneration.build_maze, globals.grid), font = ("Helvetica", 14),
            bg='pale green').grid(row=2, column=0, padx=5, pady=(10, 20))

        globals.algMenu = ttk.Combobox(globals.left_side_bar, textvariable=globals.selected_alg, 
                            values=['A-star Algorithm', 'Breadth-First Algorithm'], font = globals.font)
        globals.algMenu.grid(row=3, column=0, padx=5, pady=(20, 5), sticky=W)
        globals.algMenu.current(0)
        globals.speedScale = Scale(globals.left_side_bar, from_=0.05, to=0.5, digits=2, resolution=0.05, 
                        orient=HORIZONTAL, label='Speed', font = globals.font, length=180)
        globals.speedScale.grid(row=4, column=0, padx=5, pady=(5, 5), sticky=W)
        Button(globals.left_side_bar, text='Start Search', command=Algorithms.StartAlgorithm, font = ("Helvetica", 14),
            bg='light salmon').grid(row=5, column=0, padx=5, pady=(10, 10))

        Button(globals.left_side_bar, text='Reset', command=MazeGeneration.Reset, font = ("Helvetica", 14),
            bg='white').grid(row=6, column=0, padx=5, pady=(20, 30))

        Button(globals.left_side_bar, text='Instructions', command=Gui.instructions, font = ("Helvetica", 9),
            bg='white').grid(row=7, column=0, padx=5, pady=(10, 10))

        # spot_type_frame: right column that has options to change spot type to robot, obstactle, door, n-th staff member
        spot_type_frame = Frame(globals.root, width=600, height=200, bg='black')
        spot_type_frame.grid(row=0, column=2, padx=(0,10), pady=5)

        # UI elements for spot_type_frame
        spotTypeMenu = ttk.Combobox(spot_type_frame, textvariable=globals.selected_spot_type, 
                            values=['Robot (Green)', 'Obstacle (Black)', 'Door (Turqoise)', 'Staff Member (Red)'], font = globals.font)
        spotTypeMenu.grid(row=0, column=0, padx=10, pady=(10, 5))
        spotTypeMenu.current(0)

        Button(spot_type_frame, text='test', command=Gui.testPrint, font = ("Helvetica", 9),
            bg='white').grid(row=1, column=0, padx=10, pady=(10, 5))

    def instructions():
        messagebox.showinfo("Instructions", "1. Create a maze by clicking on the grid or choose\n"
                                            "    one of the functions from the drop-down menu\n"
                                            "\n"
                                            "    You can always edit generated mazes!\n"
                                            "\n"
                                            "2. Choose one of two algorithms to find the shortest path\n"
                                            "     and visualize the search with desired speed of animation\n"
                                            "\n"
                                            "3. Reset the grid if necessary")

    def make_grid(width, rows):
        grid = []
        gap = width // rows
        offset = 2
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(i, j, gap, offset, rows)
                grid[i].append(spot)
        return grid
  
    def testPrint():
        print(globals.selected_spot_type.get())