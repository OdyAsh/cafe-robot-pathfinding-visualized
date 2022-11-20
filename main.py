########################################################################
# Cafe Robot Scenario: Visualizing the Pathfinding Algorithm & Environment Scenarios
# Used tkinter
# Python 3.10.5
# Ashraf Haress 
# 20/11/2022
########################################################################
# Main Resource:
# @DariaSVasileva: Pathfinding_Algorithm_Visualizer_tkinter
# https://github.com/DariaSVasileva/Pathfinding_Algorithm_Visualizer_tkinter
# 
# Which is based on these resources:
# 
# @Tech With Tim: Python A* Path Finding Tutorial
# https://www.youtube.com/watch?v=JtiK0DOeI4A&ab_channel=TechWithTim
#
# @Daksh3K: Astar-Pathfinding-Algorithm-Visualization
# https://github.com/Daksh3K/Astar-Pathfinding-Algorithm-Visualization
#
# @nas-programmer: path-finding
# https://github.com/nas-programmer/path-finding
# https://www.youtube.com/watch?v=LF1h-8bEjP0&ab_channel=codeNULL
#
# @Davis MT: Python maze generator program
# https://github.com/tonypdavis/PythonMazeGenerator
# https://www.youtube.com/watch?v=Xthh4SEMA2o&ab_channel=DavisMT
#########################################################################

from tkinter import Tk, StringVar, Frame, Canvas, Button, messagebox, GROOVE, DISABLED, NORMAL, ttk, Scale, HORIZONTAL, W
import random
import time
from functools import partial

import globals
from Spot import Spot
from algorithms import Algorithms # import it here not at the top, to avoid circular dependency (as Algorithms class needs GUI to be defined in order for algorithms.py to be correctly parsed)

class GUI:
        
    def start():
        # accessing ui() as a class function instead of an instance (object) method.. 
        # example (using attributes) is here: https://stackoverflow.com/questions/4152850/is-it-possible-not-to-use-self-in-a-class
        # and here: https://stackoverflow.com/questions/136097/classmethod-vs-staticmethod-in-python
        GUI.ui() 
        # show instructions when the GUI appears
        GUI.instructions()
        # run loop 
        globals.root.mainloop()

    def ui():
        # frame layout - for user interface
        globals.UI_frame = Frame(globals.root, width=600, height=200, bg='black')
        globals.UI_frame.grid(row=0, column=0, padx=10, pady=5)
            
        # create canvas, "canvas" == "right area of application that contains the 'maze'"
        globals.canvas = Canvas(globals.root, width=globals.WIDTH, height=globals.WIDTH, bg='white')
        globals.canvas.grid(row=0, column=1, padx=10, pady=5) 

        # User interface area
        globals.bldMenu = ttk.Combobox(globals.UI_frame, textvariable=globals.selected_bld, 
                            values=['Random walls', 'Circular maze', 'Carved out maze'], font = globals.font)
        globals.bldMenu.grid(row=0, column=0, padx=5, pady=(10, 5))
        globals.bldMenu.current(0)
        globals.bldMenu.bind("<<ComboboxSelected>>", scale_action)
        globals.wallsScale = Scale(globals.UI_frame, from_=10, to=40, resolution=5, orient=HORIZONTAL, 
                        label='Wall density', font = globals.font, length=180)
        globals.wallsScale.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        Button(globals.UI_frame, text='Build maze', command=partial(build_maze, globals.grid), font = ("Helvetica", 14),
            bg='pale green').grid(row=2, column=0, padx=5, pady=(10, 20))

        globals.algMenu = ttk.Combobox(globals.UI_frame, textvariable=globals.selected_alg, 
                            values=['A-star Algorithm', 'Breadth-First Algorithm'], font = globals.font)
        globals.algMenu.grid(row=3, column=0, padx=5, pady=(20, 5), sticky=W)
        globals.algMenu.current(0)
        globals.speedScale = Scale(globals.UI_frame, from_=0.05, to=0.5, digits=2, resolution=0.05, 
                        orient=HORIZONTAL, label='Speed', font = globals.font, length=180)
        globals.speedScale.grid(row=4, column=0, padx=5, pady=(5, 5), sticky=W)
        Button(globals.UI_frame, text='Start Search', command=Algorithms.StartAlgorithm, font = ("Helvetica", 14),
            bg='light salmon').grid(row=5, column=0, padx=5, pady=(10, 10))

        Button(globals.UI_frame, text='Reset', command=GUI.Reset, font = ("Helvetica", 14),
            bg='white').grid(row=6, column=0, padx=5, pady=(20, 30))

        Button(globals.UI_frame, text='Instructions', command=GUI.instructions, font = ("Helvetica", 9),
            bg='white').grid(row=7, column=0, padx=5, pady=(10, 10))

        # Create grid
        globals.grid = GUI.make_grid(globals.WIDTH, globals.ROWS)

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

    def Reset():
        Spot.start_point = None
        Spot.end_point = None
        for row in globals.grid:
            for spot in row:
                spot.reset()
                spot.neighbors = []
                spot.g = float('inf') 
                spot.h = 0
                spot.f = float('inf')
                spot.parent = None
                spot.start = False
                spot.end = False
                spot.barrier = False
                spot.enable()
            



def break_wall(current, new, grid):
    if current.row == new.row:
        if current.col > new.col:
            # wall to the left from current
            wall = grid[current.row][current.col - 1]
        else:
            # wall to the right
            wall = grid[current.row][current.col + 1]
    else:
        if current.row > new.row:
            # wall above
            wall = grid[current.row - 1][current.col]
        else:
            # wall below
            wall = grid[current.row + 1][current.col]
    # break wall
    wall.reset()
    wall.barrier = False


# Put random walls in the grid
def random_walls(grid):
    
    # if start and end spots are not indicated - put start and end randomly
    if not Spot.start_point:
        current = grid[random.randint(0, ROWS - 1)][random.randint(0, ROWS - 1)]
        if current.end == False:
            current.make_start()
    
    if not Spot.end_point:
        current = grid[random.randint(0, ROWS - 1)][random.randint(0, ROWS - 1)]
        if current.start == False:
            current.make_end()
            
    start = grid[Spot.start_point[1]][Spot.start_point[0]]
    end = grid[Spot.end_point[1]][Spot.end_point[0]]
    
    # put walls randomly
    for row in grid:
        for spot in row:
            if spot != start and spot != end:
                spot.reset()
                spot.barrier = False
                spot.clicked = False
                if random.randint(0, 100) < wallsScale.get():
                    spot.make_barrier()
    
    # draw updated grid       
    root.update_idletasks()

def circ_maze(grid, rows):

    # Reset all
    Reset()

    # breake into rings
    rings = []
    for n in range(rows // 2 + 1):
        set1 = set()
        set2 = set()
        for row in grid:    
            for spot in row:
                if spot.row in range(n, rows - n) and spot.col in range(n, rows - n):
                    set1.add(spot)
                if spot.row in range(n + 1, rows - n - 1) and spot.col in range(n + 1, rows - n - 1):
                    set2.add(spot)
        ring = list(set1 - set2)
        if len(ring) > 0:
            rings.append(ring)
    
    # put start in the outer ring and end in the inner ring and remove them from rings
    random.choice(rings[0]).make_start()
    for spot in rings[0]:
        if spot.start == True:
            rings[0].remove(spot)
    
    random.choice(rings[-1]).make_end()
    for spot in rings[-1]:
        if spot.end == True:
            rings[-1].remove(spot)

    # make odd rings into walls
    for ring in rings[1::2]:
        
        # remove connor spots from rings    
        if len(ring) > 0:
            min_row = min([spot.row for spot in ring])
            max_row = max([spot.row for spot in ring])
            tmp = []
            for spot in ring:
                if (spot.row, spot.col) in [(min_row, min_row), (min_row, max_row),
                                            (max_row, min_row), (max_row, max_row)]:
                    tmp.append(spot)
            for item in tmp:
                ring.remove(item)
        
        for spot in ring:
            spot.make_barrier()
        
        if len(ring) == 0:
            rings.remove(ring)
    
    # make oppenings in ring walls
    for ring in rings[1::2]:
        for item in random.sample(ring, 2):
            item.reset()
            item.barrier = False
    
    # update neighbors based on current maze
    for row in grid:
        for spot in row:
            spot.neighbors = []
            spot.update_neighbors(grid)
    
    # add single walls between ring walls
    for ring in rings[2::2]:
        # make random spots into a wall
        tmp = []
        for spot in ring:
            if len(spot.neighbors) < 3:
                tmp.append(spot)
        if len(tmp) > 0:
            single_wall = random.choice(tmp)
            single_wall.make_barrier()        
    
    # draw updated grid       
    root.update_idletasks()
    
def carve_out(grid, rows, tickTime):

    # Reset all
    Reset()
    
    to_visit = []
    for row in grid[::2]:
        for spot in row[::2]:
            to_visit.append(spot)
        
    for row in grid:
        for spot in row:
            if spot in to_visit:
                spot.make_to_visit()
            else:
                spot.make_barrier()
    
    to_visit[0].make_start()
    to_visit[-1].make_end()
    start = grid[Spot.start_point[1]][Spot.start_point[0]]
    end = grid[Spot.end_point[1]][Spot.end_point[0]]
    
    # draw updated grid with new open_set        
    root.update_idletasks()
    time.sleep(tickTime)
    
    visited = []
    open_set = []
    current = start
    open_set.append(current)
    visited.append(current)
    
    while len(open_set) > 0:
        moves = []
        
        # right neighbor
        if current.col + 2 < rows:
            neighbor = grid[current.row][current.col + 2]
            if neighbor not in visited and neighbor in to_visit:
                moves.append(neighbor)

        # left neighbor
        if current.col - 2 >= 0:
            neighbor = grid[current.row][current.col - 2]
            if neighbor not in visited and neighbor in to_visit:
                moves.append(neighbor)
            
        # down neighbor
        if current.row + 2 < rows:
            neighbor = grid[current.row + 2][current.col]
            if neighbor not in visited and neighbor in to_visit:
                moves.append(neighbor)
            
        # up neighbor
        if current.row - 2 >= 0:
            neighbor = grid[current.row - 2][current.col]
            if neighbor not in visited and neighbor in to_visit:
                moves.append(neighbor)

        if len(moves) > 0:
            new = random.choice(moves)
            break_wall(current, new, grid)
            if new != end:
                new.reset()
            current = new
            visited.append(current)
            open_set.append(current)
        else:
            current = open_set.pop()
            if current != start and current != end:
                current.make_backtracking()
                # draw updated grid with new open_set        
                root.update_idletasks()
                time.sleep(tickTime)
                current.reset()
            
        # draw updated grid with new open_set        
        root.update_idletasks()
        time.sleep(tickTime)
        
    # draw updated grid with new open_set        
    root.update_idletasks()
    time.sleep(tickTime)
    
# start pathfinding
def build_maze(grid):
    if not grid: 
        messagebox.showinfo("No grid", "Please initialize grid" )
        return

    for row in grid:
        for spot in row:
            spot.disable() # disable buttons in the grid for running algorithm
    
    # disable UI frame for running algorithm
    for child in UI_frame.winfo_children():
        child.configure(state='disable')
    
    # choose algorithm
    if bldMenu.get() == 'Random walls':
        random_walls(grid)
    elif bldMenu.get() == 'Circular maze':
        circ_maze(grid, ROWS) 
    elif bldMenu.get() == 'Carved out maze':
        carve_out(grid, ROWS, speedScale.get())
        
    # enable buttons in the grid
    for row in grid:
        for spot in row:
            spot.enable()
    
    for child in UI_frame.winfo_children():
        child.configure(state='normal') # enable frame

def scale_action(event):
    if bldMenu.get() == 'Random walls':
        wallsScale.configure(state='normal')
    else:
        wallsScale.configure(state='disable')
        


if __name__ == "__main__":
    globals.init()
    GUI.start()