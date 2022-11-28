from tkinter import messagebox
import time
from queue import PriorityQueue
from collections import deque
from threading import Thread

from Spot import Spot
from tkinter import END
import globals
import random

class Algorithms:

    paths = []
    curPathOfWalking = 0
    # define heuristic function - Manhatten distance
    def h(a, b):
        return abs(a.row - b.row) + abs(a.col - b.col)

    def reconstruct_path(spot):
        curPath = []
        current = spot
        current.make_path() # will make spot of current (which is staff location) Dark Red
        curPath.append(current)
        while current.isStart == False:
            parent = current.parent
            parent.make_path()
            globals.root.update_idletasks()
            time.sleep(globals.getTickTime())
            current = parent
            curPath.append(current)
        Algorithms.paths.append(curPath[::-1]) # appending the reverse path (i.e., from start to end) to list of paths
    
    def traverse_path():
        curPath = Algorithms.paths[Algorithms.curPathOfWalking]
        for i in range(1, len(curPath)):
            if curPath[i].isDoor:
                time.sleep(1)
                curPath[i].open_door() # simulates opening of door by turning color from turqoise to cornflower blue
                globals.root.update_idletasks()
                time.sleep(1) # open the door in one second
            curPath[i-1].traverse_a_step(isStartOfPath = (i == 1), isFirstPath = (Algorithms.curPathOfWalking == 0)) # marking the spot as finished with dark red if True (if the spot was a loc. of staff) or dark green if False (if it was the initial starting point)
            curPath[i].button.config(bg = "lime green") # simulate robot moving to current spot
            globals.root.update_idletasks()
            time.sleep(globals.getTickTime())
        curPath[-1].make_start() # make the last spot in the current path the starting position for the next path

    # A-star algorithm
    def a_star(grid, start, end):
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
                Algorithms.reconstruct_path(end)
                Algorithms.traverse_path()
                Algorithms.curPathOfWalking += 1

                # enable UI frame
                for child in globals.left_frame.winfo_children():
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
            time.sleep(globals.getTickTime())
            
            if current != start:
                current.make_closed()
                
        # didn't find path
        messagebox.showinfo("No Solution", "There was no solution" )

        return False

    # Breadth-First algorithm
    def breadth_first(grid, start, end):
        
        open_set = deque()
        
        open_set.append(start)
        visited_hash = {start}
        
        while len(open_set) > 0:
            current = open_set.popleft()
            
            # found end?
            if current == end:
                Algorithms.reconstruct_path(end)
                Algorithms.traverse_path()
                Algorithms.curPathOfWalking += 1
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
            time.sleep(globals.getTickTime())
            
            if current != start:
                current.make_closed()
                
        # didn't find path
        messagebox.showinfo("No Solution", "There was no solution")

        return False


    def threadifyStartAlgorithms(): # make StartAlgorithms() in a separate thread; to prevent GUI from freezing
        th = Thread(target=Algorithms.startAlgorithms)
        try:
            th.start()
        except:
            th.join()
            th.start()

    def startAlgorithms():
        # validation checks
        if not globals.grid:
            messagebox.showinfo("No grid found", "Initialize grid")
            return
            
        if not Spot.start_point or len(Spot.end_points) == 0: 
            messagebox.showinfo("No start/end", "Place starting and ending points")
            return

        Spot.end_points[100] = (Spot.start_point[0], Spot.start_point[1]) # add one final end point; the robot's initial starting position (noting that "100" was put as upper limit, since there're unlikely more than 99 staff members who want to order coffee at the same time)
        
        strictMode = True
        # '1.0': 1st line in text box, 0th character, end: last character in textbox (\n), '-1c': ommit the last character (which is \n)
        if globals.txtBox.get("1.0", "end-1c") == "": # if text box is empty, then the robot becomes in "non-strict" mode; meaning that it will give out coffee to anyone who orders anonymously
            strictMode = False
            for key in sorted(Spot.end_points):
                if key == 100: # this is the flag value set to indicate that the robot will return to its initial position
                    break
                globals.txtBox.insert(END, f"{key}. {random.choice(globals.storedStaffNames)}\n")
        else:
            globals.txtBox.insert(END, '\n') # add a new line at the end, as the user probably didn't type "enter"
        globals.txtBox.insert(END, 'Return to initial position')

        
        # Running the algorithm for all staff members
        curLine = 1 # current line in staff's text box
        for key in sorted(Spot.end_points): # sorted() returns list of ordered keys (so values are not included)
            if strictMode and key != 100:
                valid = globals.validateName(globals.txtBox.get(f"{curLine}.3", f"{curLine}.end")) # check the tkinter docs to understand indexing: https://tkdocs.com/tutorial/text.html#:~:text=Here%20are%20a%20few%20additional%20examples%20of%20indices%20and%20how%20to%20interpret%20them%3A
                if not valid:
                    messagebox.showerror('Invalid Request', 'A non-staff member cannot order coffee!!\nTerminating...')
                    time.sleep(3)
                    globals.root.destroy() 
            
            sRow, sCol = Spot.start_point[0], Spot.start_point[1]
            eRow, eCol = Spot.end_points[key][0], Spot.end_points[key][1]
            curStart = globals.grid[sRow][sCol]
            curEnd = globals.grid[eRow][eCol]
            curEnd.make_end(asObstacle=False)

            if curLine > 1:
                globals.txtBox.delete(f"{curLine-1}.0", f"{curLine-1}.3") # delete arrow of previous line
            globals.txtBox.insert(f"{curLine}.0", "-> ") # insert arrow at start of current line

            Algorithms.startAlgorithm(curStart, curEnd)

            time.sleep(0.5) # Gap between each algorithm run
            curLine += 1

        # After finishing the algorithms, change blue spots (spots that were checked by the algorithm) to white
        for row in globals.grid:
            for spot in row:
                if not spot.clicked:
                    spot.button.config(bg = 'white')
        globals.root.update_idletasks()
        time.sleep(0.1)
        
        # Finally, draw the entire path walked by the robot
        for path in Algorithms.paths:
            for spot in path:
                if spot.button['bg'] == 'white':
                    spot.button.config(bg = 'gold')
                globals.root.update_idletasks()
                time.sleep(globals.getTickTime())
        
        time.sleep(0.2)
        Algorithms.paths[0][0].button.config(text=':]', fg='black') # Algorithms' Finale
        globals.root.update_idletasks()

    
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
        
        # choose algorithm
        if globals.algMenu.get() == 'A-star Algorithm':
            Algorithms.a_star(globals.grid, curStart, curEnd)
        elif globals.algMenu.get() == 'Breadth-First Algorithm':
            Algorithms.breadth_first(globals.grid, curStart, curEnd)     
            
        # enable buttons in the grid
        for row in globals.grid:
            for spot in row:
                spot.enable()
        
        for child in globals.left_frame.winfo_children():
            child.configure(state='normal') # enable frame
