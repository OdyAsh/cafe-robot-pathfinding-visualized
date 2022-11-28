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






































    def circ_maze(grid, rows):

        # Reset all
        MazeGeneration.Reset()

        # break into rings
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

        start = grid[Spot.start_point[0]][Spot.start_point[1]]
        for key in sorted(Spot.end_points):
            end = grid[Spot.end_points[key][0]][Spot.end_points[key][1]]
            break
        
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