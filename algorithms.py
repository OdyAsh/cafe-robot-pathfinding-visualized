from tkinter import messagebox
import time
from queue import PriorityQueue
from collections import deque

from Spot import Spot
import globals

class Algorithms:

    paths = []
    curPathOfWalking = 0
    # define heuristic function - Manhatten distance
    def h(a, b):
        return abs(a.row - b.row) + abs(a.col - b.col)

    def reconstruct_path(spot, tickTime):
        curPath = []
        current = spot
        current.make_path() # will make spot of current (which is staff location) dark orange
        curPath.append(current)
        while current.isStart == False:
            parent = current.parent
            parent.make_path()
            globals.root.update_idletasks()
            time.sleep(tickTime)
            current = parent
            curPath.append(current)
        Algorithms.paths.append(curPath[::-1]) # appending the reverse path (i.e., from start to end) to list of paths
        Algorithms.traverse_path(tickTime)
        Algorithms.curPathOfWalking += 1
    
    def traverse_path(tickTime):
        curPath = Algorithms.paths[Algorithms.curPathOfWalking]
        for i in range(1, len(curPath)):
            if curPath[i].isDoor:
                time.sleep(1)
                curPath[i].open_door() # simulates opening of door by turning color from turqoise to cornflower blue
                globals.root.update_idletasks()
                time.sleep(1) # open the door in one second
            curPath[i-1].traverse_a_step(isStartOfPath = (i == 1), isFirstPath = (Algorithms.curPathOfWalking == 0)) # marking the spot as finished with dark orange color if True (if the spot was a loc. of staff) or yellow if False (if it was the initial starting point)
            curPath[i].make_start()
            globals.root.update_idletasks()
            time.sleep(tickTime)

    # A-star algorithm
    def a_star(grid, tickTime, start, end):
        count = 0
        
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
            # synchronise with dict
            open_set_hash.remove(current)
            
            # found end?
            if current == end:
                Algorithms.reconstruct_path(end, tickTime)
                
                # enable UI frame
                for child in globals.left_side_bar.winfo_children():
                    child.configure(state='normal')
                return True
            
            # if not end - consider all neighbors of current spot to choose next step
            for neighbor in current.neighbors:
                
                # calculate g_score for every neighbor
                temp_g_score = current.g + 1
                
                # if new path through this neighbor is better
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
    def breadth_first(grid, tickTime, start, end):
        
        open_set = deque()
        
        open_set.append(start)
        visited_hash = {start}
        
        while len(open_set) > 0:
            current = open_set.popleft()
            
            # found end?
            if current == end:
                Algorithms.reconstruct_path(end, tickTime)
                
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

    def startAlgorithms():
        # validation checks
        if not globals.grid:
            messagebox.showinfo("No grid found", "Initialize grid")
            return
            
        if not Spot.start_point or len(Spot.end_points) == 0: 
            messagebox.showinfo("No start/end", "Place starting and ending points")
            return
        
        Spot.end_points[100] = (Spot.start_point[0], Spot.start_point[1]) # add one final end point; the robot's initial starting position (noting that "100" was put as upper limit, since there're unlikely more than 99 staff members who want to order coffee at the same time)
        # Running the algorithm for all staff members
        for key in sorted(Spot.end_points): # sorted() returns list of ordered keys (so values are not included)
            sRow, sCol = Spot.start_point[0], Spot.start_point[1]
            eRow, eCol = Spot.end_points[key][0], Spot.end_points[key][1]
            curStart = globals.grid[sRow][sCol]
            curEnd = globals.grid[eRow][eCol]
            curEnd.make_end(asObstacle=False)

            Algorithms.startAlgorithm(curStart, curEnd)
            time.sleep(0.5) # Gap between each algorithm run




    
    # start pathfinding
    def startAlgorithm(curStart, curEnd):

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
        
        # disable UI frame while running algorithm
        for child in globals.left_side_bar.winfo_children():
            child.configure(state='disable')
        
        # choose algorithm
        if globals.algMenu.get() == 'A-star Algorithm':
            Algorithms.a_star(globals.grid, globals.speedScale.get(), curStart, curEnd)
        elif globals.algMenu.get() == 'Breadth-First Algorithm':
            Algorithms.breadth_first(globals.grid, globals.speedScale.get(), curStart, curEnd)     
            
        # enable buttons in the grid
        for row in globals.grid:
            for spot in row:
                spot.enable()
        
        for child in globals.left_side_bar.winfo_children():
            child.configure(state='normal') # enable frame
