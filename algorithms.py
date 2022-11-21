from tkinter import messagebox
import time
from queue import PriorityQueue
from collections import deque

from Spot import Spot
import globals

class Algorithms:

    # define heuristic function - Manhatten distance
    def h(a, b):
        return abs(a.row - b.row) + abs(a.col - b.col)

    def reconstruct_path(spot, tickTime):
        current = spot
        while current.isStart == False:
            parent = current.parent
            parent.make_path()
            globals.root.update_idletasks()
            time.sleep(tickTime)
            current = parent

    # A-star algorithm
    def a_star(grid, tickTime):
        count = 0
        start = grid[Spot.start_point[1]][Spot.start_point[0]]
        end = grid[Spot.end_point[1]][Spot.end_point[0]]
        
        # create open_set
        open_set = PriorityQueue()
        
        # add start in open_set with f_score = 0 and count as one item
        open_set.put((0, count, start))

        # put g_score for start to 0    
        start.g = 0
        
        # calculate f_score for start using heuristic function
        start.f = Algorithms.h(start, end)
        
        # create a dict to keep track of spots in open_set, can't check PriorityQueue
        open_set_hash = {start}
        
        # if open_set is empty - all possible spots are considered, path doesn't exist
        while not open_set.empty():
            
            # popping the spot with lowest f_score from open_set
            # if score the same, then whatever was inserted first - PriorityQueue
            # popping [2] - spot itself
            current = open_set.get()[2]
            # syncronise with dict
            open_set_hash.remove(current)
            
            # found end?
            if current == end:
                Algorithms.reconstruct_path(end, tickTime)
                
                # draw end and start again
                end.make_end()
                start.make_start()
                
                # enable UI frame
                for child in globals.UI_frame.winfo_children():
                    child.configure(state='normal')
                return True
            
            # if not end - consider all neighbors of current spot to choose next step
            for neighbor in current.neighbors:
                
                # calculate g_score for every neighbor
                temp_g_score = current.g + 1
                
                # if new path through this neighbor better
                if temp_g_score < neighbor.g:
                    
                    # update g_score for this spot and keep track of new best path
                    neighbor.parent = current
                    neighbor.g = temp_g_score
                    neighbor.f = temp_g_score + Algorithms.h(neighbor, end)
                    
                    if neighbor not in open_set_hash:
                        
                        # count the step
                        count += 1
                        
                        # add neighbor in open_set for consideration
                        open_set.put((neighbor.f, count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()
            
            # draw updated grid with new open_set        
            globals.root.update_idletasks()
            time.sleep(tickTime)
            
            if current != start:
                current.make_closed()
                
        # didn't find path
        messagebox.showinfo("No Solution", "There was no solution" )

        return False

    # Breadth-First algorithm
    def breadth_first(grid, tickTime):
        
        start = grid[Spot.start_point[1]][Spot.start_point[0]]
        end = grid[Spot.end_point[1]][Spot.end_point[0]]
        
        open_set = deque()
        
        open_set.append(start)
        visited_hash = {start}
        
        while len(open_set) > 0:
            current = open_set.popleft()
            
            # found end?
            if current == end:
                Algorithms.reconstruct_path(end, tickTime)
                
                # draw end and start again
                end.make_end()
                start.make_start()
                return
            
            # if not end - consider all neighbors of current spot to choose next step
            for neighbor in current.neighbors:
                
                if neighbor not in visited_hash:
                    neighbor.parent = current
                    visited_hash.add(neighbor)
                    open_set.append(neighbor)
                    neighbor.make_open()
                    
            # draw updated grid with new open_set        
            globals.root.update_idletasks()
            time.sleep(tickTime)
            
            if current != start:
                current.make_closed()
                
        # didn't find path
        messagebox.showinfo("No Solution", "There was no solution")

        return False

    # start pathfinding
    def StartAlgorithm():

        if not globals.grid:
            messagebox.showinfo("No grid found", "Initialize grid")
            return

        if not Spot.start_point or not Spot.end_point: 
            messagebox.showinfo("No start/end", "Place starting and ending points")
            return
        
        # update neighbors based on current maze
        for row in globals.grid:
            for spot in row:
                spot.neighbors = []
                spot.g = float('inf') 
                spot.h = 0
                spot.f = float('inf')
                spot.parent = None
                spot.update_neighbors(globals.grid)
                if spot.clicked == False:
                    spot.reset()
                spot.disable() # disable buttons in the grid for running algorithm
        
        # disable UI frame for running algorithm
        for child in globals.UI_frame.winfo_children():
            child.configure(state='disable')
        
        # choose algorithm
        if globals.algMenu.get() == 'A-star Algorithm':
            Algorithms.a_star(globals.grid, globals.speedScale.get())
        elif globals.algMenu.get() == 'Breadth-First Algorithm':
            Algorithms.breadth_first(globals.grid, globals.speedScale.get())     
            
        # enable buttons in the grid
        for row in globals.grid:
            for spot in row:
                spot.enable()
        
        for child in globals.UI_frame.winfo_children():
            child.configure(state='normal') # enable frame
