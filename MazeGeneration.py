import random
import time
from tkinter import messagebox, END

import globals
from Spot import Spot
from Algorithms import Algorithms

class MazeGeneration:

    # Build maze based on chosen option
    def build_maze(grid):

        if globals.bldMenu.get() == 'Staff floor scenario':
            MazeGeneration.staff_floor()
        elif globals.bldMenu.get() == 'Invalid member scenario':
            MazeGeneration.inv_mem()
        elif globals.bldMenu.get() == 'No solution scenario':
            MazeGeneration.no_sol()
        elif globals.bldMenu.get() == "A+ scenario":
            MazeGeneration.a_plus()
        elif globals.bldMenu.get() == 'Random walls':
            MazeGeneration.random_walls(grid)

    def staff_floor():
        pass

    def inv_mem():
        pass

    def no_sol():
        pass
        
    def a_plus():
        pass

        

    def scale_action(event):
        if globals.bldMenu.get() == 'Random walls':
            globals.wallsScale.grid() # shows wall density scale
        else:
            globals.wallsScale.grid_remove() # hides wall density scale
    
    # Put random walls in the grid
    def random_walls(grid):
        
        # if start and end spots are not indicated - put start and end randomly
        if not Spot.start_point:
            current = grid[random.randint(0, globals.ROWS - 1)][random.randint(0, globals.ROWS - 1)]
            current.make_start()
        
        if len(Spot.end_points) == 0:
            current = grid[random.randint(0, globals.ROWS - 1)][random.randint(0, globals.ROWS - 1)]
            current.make_end(userClicked = True)
        
        # put walls randomly
        for row in grid:
            for spot in row:
                if spot.button['bg'] not in ['white', 'black']: # don't change any spots that are assigned with any value except obstacles (e.g., robot, staff, door)
                    continue
                spot.reset()
                spot.isObstacle = False
                spot.clicked = False
                if random.randint(0, 100) < globals.wallsScale.get():
                    spot.make_obstacle()
                
        # draw updated grid       
        globals.root.update_idletasks()

    def Reset():
        Spot.start_point = None
        Spot.end_points = {}
        Spot.staffId = 1
        Algorithms.paths = []
        Algorithms.curPathOfWalking = 0
        globals.txtBox.delete("1.0", END)        
        for row in globals.grid:
            for spot in row:
                spot.reset()
                spot.neighbors = []
                spot.g = float('inf') 
                spot.h = 0
                spot.f = float('inf')
                spot.enable()


