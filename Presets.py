import random
import pickle
import os
from tkinter import END

import globals
from Spot import Spot
from Algorithms import Algorithms

class Presets:

    # Build preset based on chosen option
    def build_preset(grid):
        chosenPreset = globals.bldMenu.get()
        if chosenPreset == 'Invalid member scenario':
            Presets.inv_mem()
        elif chosenPreset == 'No solution scenario':
            Presets.no_sol()
        elif chosenPreset == "A+ scenario":
            Presets.a_plus()
        if chosenPreset == 'Random walls':
            Presets.random_walls(grid)
        else:
            Presets.load_preset(chosenPreset)

    def load_preset(fileName):
        with open(os.path.join(globals.dir, fileName + '.pickle'), 'rb') as f:
            loadedGridData, txtinTxtBox = pickle.load(f)
            for i in range(len(loadedGridData)):
                for j in range(len(loadedGridData[i])):
                    globals.grid[i][j].importData(loadedGridData[i][j])
            globals.txtBox.delete('1.0', END)
            globals.txtBox.insert('1.0', txtinTxtBox)
            globals.txtBox.delete("end-1c", END) # delete the \n that appears for some reason when loading the pickle file
            globals.updateGui()
            
        
    def save_preset():
        fullFileName = os.path.join(globals.dir, globals.bldMenu.get() + '.pickle')
        os.makedirs(os.path.dirname(fullFileName), exist_ok=True) # makes the "presets" directory if it was not present previously
        gridData = []
        for row in globals.grid:
            tmpRow = []
            for spot in row:
                tmpRow.append(spot.exportData())
            gridData.append(tmpRow)
        with open(fullFileName, 'wb') as f:
            pickle.dump((gridData, globals.txtBox.get('1.0', END)), f)

    def scale_action(event):
        if globals.bldMenu.get() == 'Random walls':
            globals.wallsScale.grid() # shows wall density scale
        else:
            globals.wallsScale.grid_remove() # hides wall density scale
        globals.updateGui()
    
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
        globals.updateGui()

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


