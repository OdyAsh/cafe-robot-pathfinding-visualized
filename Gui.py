from tkinter import Frame, Canvas, Button, messagebox, ttk, Scale, HORIZONTAL, W, Label, Text
from functools import partial
import os

import globals
from Spot import Spot
from Algorithms import Algorithms
from Presets import Presets

class Gui:

    def ui():
        # left_frame == Left column of application that contains buttons for the preset type, chosen algorithm, and instructions
        globals.left_frame = Frame(globals.root, width=600, height=200, bg='black')
        globals.left_frame.grid(row=0, column=0, padx=10, pady=5)
            
        # create grid_canvas, "grid_canvas" == Middle area of application that contains the "preset"
        globals.grid_canvas = Canvas(globals.root, width=globals.WIDTH, height=globals.WIDTH, bg='orange')
        globals.grid_canvas.grid(row=0, column=1, padx=10, pady=5) 

        # Create grid
        globals.grid = Gui.make_grid(globals.WIDTH, globals.ROWS)

        # getting list of presets from pickle files available locally
        listOfPresets = ['Random walls']
        if os.path.exists(globals.dir):
            for filename in os.listdir(globals.dir): # iterate over files in "presets" directory
                if filename.endswith('.pickle'):
                    listOfPresets.append(filename.split('.pickle')[0])
        
        # UI elements for left_frame
        globals.bldMenu = ttk.Combobox(globals.left_frame, textvariable=globals.selected_bld, 
                            values=listOfPresets, font = globals.font)
        globals.bldMenu.grid(row=0, column=0, padx=5, pady=(10, 5))
        globals.bldMenu.current(0)
        globals.bldMenu.bind("<<ComboboxSelected>>", Presets.scale_action)

        globals.wallsScale = Scale(globals.left_frame, from_=10, to=40, resolution=5, orient=HORIZONTAL, 
                        label='Obstacles density', font = globals.font, length=180)
        globals.wallsScale.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        Button(globals.left_frame, text='Save preset', command=Presets.save_preset, font = ("Helvetica", 10),
            bg='white').grid(row=2, column=0, padx=5, pady=(10, 20))
        Button(globals.left_frame, text='Build preset', command=partial(Presets.build_preset, globals.grid), font = ("Helvetica", 14),
            bg='pale green').grid(row=3, column=0, padx=5, pady=(10, 20))

        globals.algMenu = ttk.Combobox(globals.left_frame, textvariable=globals.selected_alg, 
                            values=['A-star Algorithm', 'Breadth-First Algorithm'], font = globals.font)
        globals.algMenu.grid(row=4, column=0, padx=5, pady=(20, 5), sticky=W)
        globals.algMenu.current(0)
        globals.speedScale = Scale(globals.left_frame, from_=0.05, to=0.5, digits=2, resolution=0.05, 
                        orient=HORIZONTAL, label='Speed', font = globals.font, length=180)
        globals.speedScale.grid(row=5, column=0, padx=5, pady=(5, 5), sticky=W)
        Button(globals.left_frame, text='Start Search', command=Algorithms.threadifyStartAlgorithms, font = ("Helvetica", 14),
            bg='light salmon').grid(row=6, column=0, padx=5, pady=(10, 10))

        Button(globals.left_frame, text='Reset', command=Presets.Reset, font = ("Helvetica", 14),
            bg='white').grid(row=7, column=0, padx=5, pady=(20, 30))

        Button(globals.left_frame, text='Instructions', command=Gui.instructions, font = ("Helvetica", 9),
            bg='white').grid(row=8, column=0, padx=5, pady=(10, 10))

        # right_frame: right column that has options to change spot type to robot, obstactle, door, n-th staff member, and allows for entry of staff members' names who ordered coffee
        right_frame = Frame(globals.root, width=600, height=200, bg='black')
        right_frame.grid(row=0, column=2, padx=(0,10), pady=5)

        # UI elements for right_frame
        spotTypeMenu = ttk.Combobox(right_frame, textvariable=globals.selected_spot_type, 
                            values=['Robot (Green)', 'Obstacle (Black)', 'Door (Turqoise)', 'Staff Member (Red)'], font = globals.font)
        spotTypeMenu.grid(row=0, column=0, padx=10, pady=(10, 5))
        spotTypeMenu.current(0)

        Label(right_frame, text="Staff's Orders").grid(row=1, column=0, padx=10, pady=(30, 5))
        globals.txtBox = Text(right_frame, height=15, width=28, bg='light cyan', font=("Helvetica", 8)) # text box for storing info about each staff member who ordered coffee
        globals.txtBox.grid(row=2, column=0, padx=10, pady=(0, 5))
        globals.txtBox.focus() # focuses mouse cursor in this text box when user opens the application

    def instructions():
        messagebox.showinfo("Instructions", "1. Create a preset by clicking on the grid or choose\n"
                                            "    one of the functions from the drop-down menu\n"
                                            "\n"
                                            "    You can always edit generated presets!\n"
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
  