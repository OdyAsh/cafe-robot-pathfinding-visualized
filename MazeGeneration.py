import random
import time
from tkinter import messagebox

import globals
from Spot import Spot

class MazeGeneration:
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
        wall.isObstacle = False

    # Put random walls in the grid
    def random_walls(grid):
        
        # if start and end spots are not indicated - put start and end randomly
        if not Spot.start_point:
            current = grid[random.randint(0, globals.ROWS - 1)][random.randint(0, globals.ROWS - 1)]
            if current.isEnd == False:
                current.make_start()
        
        if not Spot.end_point:
            current = grid[random.randint(0, globals.ROWS - 1)][random.randint(0, globals.ROWS - 1)]
            if current.isStart == False:
                current.make_end()
                
        start = grid[Spot.start_point[1]][Spot.start_point[0]]
        end = grid[Spot.end_point[1]][Spot.end_point[0]]
        
        # put walls randomly
        for row in grid:
            for spot in row:
                if spot != start and spot != end:
                    spot.reset()
                    spot.isObstacle = False
                    spot.clicked = False
                    if random.randint(0, 100) < globals.wallsScale.get():
                        spot.make_obstacle()
        
        # draw updated grid       
        globals.root.update_idletasks()

    def circ_maze(grid, rows):

        # Reset all
        MazeGeneration.Reset()

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
            if spot.isStart == True:
                rings[0].remove(spot)
        
        random.choice(rings[-1]).make_end()
        for spot in rings[-1]:
            if spot.isEnd == True:
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
                spot.make_obstacle()
            
            if len(ring) == 0:
                rings.remove(ring)
        
        # make oppenings in ring walls
        for ring in rings[1::2]:
            for item in random.sample(ring, 2):
                item.reset()
                item.isObstacle = False
        
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
                single_wall.make_obstacle()        
        
        # draw updated grid       
        globals.root.update_idletasks()
        
    def carve_out(grid, rows, tickTime):

        # Reset all
        MazeGeneration.Reset()
        
        to_visit = []
        for row in grid[::2]:
            for spot in row[::2]:
                to_visit.append(spot)
            
        for row in grid:
            for spot in row:
                if spot in to_visit:
                    spot.make_to_visit()
                else:
                    spot.make_obstacle()
        
        to_visit[0].make_start()
        to_visit[-1].make_end()
        start = grid[Spot.start_point[1]][Spot.start_point[0]]
        end = grid[Spot.end_point[1]][Spot.end_point[0]]
        
        # draw updated grid with new open_set        
        globals.root.update_idletasks()
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
                MazeGeneration.break_wall(current, new, grid)
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
                    globals.root.update_idletasks()
                    time.sleep(tickTime)
                    current.reset()
                
            # draw updated grid with new open_set        
            globals.root.update_idletasks()
            time.sleep(tickTime)
            
        # draw updated grid with new open_set        
        globals.root.update_idletasks()
        time.sleep(tickTime)
        
    # Build maze based on chosen option
    def build_maze(grid):
        if not grid: 
            messagebox.showinfo("No grid", "Please initialize grid" )
            return

        for row in grid:
            for spot in row:
                spot.disable() # disable buttons in the grid for running algorithm
        
        # disable UI frame for running algorithm
        for child in globals.left_side_bar.winfo_children():
            child.configure(state='disable')
        
        # choose algorithm
        if globals.bldMenu.get() == 'Random walls':
            MazeGeneration.random_walls(grid)
        elif globals.bldMenu.get() == 'Circular maze':
            MazeGeneration.circ_maze(grid, globals.ROWS) 
        elif globals.bldMenu.get() == 'Carved out maze':
            MazeGeneration.carve_out(grid, globals.ROWS, globals.speedScale.get())
            
        # enable buttons in the grid
        for row in grid:
            for spot in row:
                spot.enable()
        
        for child in globals.left_side_bar.winfo_children():
            child.configure(state='normal') # enable frame

    def scale_action(event):
        if globals.bldMenu.get() == 'Random walls':
            globals.wallsScale.configure(state='normal')
        else:
            globals.wallsScale.configure(state='disable')

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
                spot.isStart = False
                spot.isEnd = False
                spot.isObstacle = False
                spot.enable()