from tkinter import Button, GROOVE, DISABLED, NORMAL
import globals

# define class - spot
class Spot():
    
    start_point = None
    end_points = {}
    staffId = 1

    def exportData(self):
        dicWithoutButton = self.__dict__.copy()
        btn = dicWithoutButton.pop('button')
        btnConfigs = {'bg': btn['bg'], 'fg': btn['fg'], 'text': btn['text']}
        classData = Spot.start_point, Spot.end_points, Spot.staffId
        return (dicWithoutButton, btnConfigs, classData)

    def importData(self, pklContent):
        pklContent[0]['button'] = self.button
        self.__dict__ = pklContent[0]
        self.button.config(**pklContent[1])
        Spot.start_point, Spot.end_points, Spot.staffId = pklContent[2]

    # this is used for efficiency, but because we possibly want to export spots (to a preset), we need __dict__, which won't be created if we create __slots__
    #__slots__ = ['button','row', 'col', 'width', 'neighbors', 'g', 'h', 'f',  
    #             'parent', 'isStart', 'isEnd', 'isObstacle', 'isDoor', 'isPath', 'clicked', 'total_rows']
    
    def __init__(self, row, col, width, offset, total_rows):
        
        self.button = Button(globals.grid_canvas,
         command = self.click,
         bg='white', bd=2, relief=GROOVE
        )
        
        self.row = row
        self.col = col
        self.width = width
        
        self.button.place(x=row * width + offset, y=col * width + offset, 
                          width=width, height=width)

        self.neighbors = []
        self.g = float('inf') 
        self.h = 0
        self.f = float('inf')
        self.parent = None
        self.isStart = False
        self.isEnd = False
        self.isObstacle = False
        self.isDoor = False
        self.isPath = False
        self.clicked = False
        self.total_rows = total_rows
    
    def make_start(self):
        self.button.config(bg = "lime green")
        self.isStart = True
        self.isEnd = self.isObstacle = False # don't change self.isDoor, bec. if the spot was actually a door, then we want its colour to re-appear (using traverse_a_step()) after the robot passes by it
        self.clicked = True
        Spot.start_point = (self.row, self.col)
        
    def make_end(self, asObstacle = True, userClicked = False):
        if (len(Spot.end_points) == 0 or not asObstacle):
            self.button.config(bg = globals.rgbtohex(255,0,0))
            self.isEnd = True
            self.isObstacle = False
        else:
            self.button.config(bg = globals.rgbtohex(max(100, abs(255-Spot.staffId*14)),0,0))
            self.isEnd = False
            self.isObstacle = True
        self.isStart = self.isDoor = False
        self.clicked = True

        if userClicked:
            Spot.end_points[Spot.staffId] = (self.row, self.col)
            Spot.staffId += 1

        if Spot.end_points.get(100) and self.row == Spot.end_points[100][0] and self.col == Spot.end_points[100][1]: # overriding previously set colors if the spot is the initial starting point of the robot
            self.button.config(bg = globals.rgbtohex(0,128,0)) # dark green
            return

        # add staff's id to the corresponding spot's button
        for key, rc in Spot.end_points.items():
            if self.row == rc[0] and self.col == rc[1]:
                self.button.config(text=f'{key}', fg='white')

              

    def traverse_a_step(self, isStartOfPath, isFirstPath):
        if self.isDoor: # if spot was a door, then leave it as a closed door after robot walks by it
            self.make_door()
            return
        self.isEnd = self.isStart = False
        if isStartOfPath: # set spot attributes based on if robot was at the initial location or staff location
            self.isObstacle = (not isFirstPath)
            self.button.config(bg = globals.rgbtohex(0,128,0) if isFirstPath else globals.rgbtohex(150,0,0)) # Dark Red if the spot that the robot was in is related to a staff member, dark green if this was initial location of the robot
        else: # otherwise, deals with spot as a walkable path
            self.isObstacle = False
            self.button.config(bg = "gold" if self.button['bg'] != globals.rgbtohex(0,128,0) else globals.rgbtohex(0,128,0)) # gold if the location that the robot left was any location other than its starting location
            
            
        
    def make_obstacle(self):
        self.button.config(bg = "black")
        self.isObstacle = True
        self.isStart = self.isEnd = self.isDoor = False
        self.clicked = True

    def make_door(self):
        self.button.config(bg = globals.rgbtohex(64, 224, 208)) # Turqoise Colour
        self.isDoor = True
        self.isStart = self.isEnd = self.isObstacle = False
        self.clicked = True
        
    def reset(self):
        self.button.config(bg = "white", text='', fg='black')
        self.clicked = self.parent = self.isObstacle = self.isDoor = self.isPath = False
        if self.isStart:   
            self.isStart = False
            Spot.start_point = None
        if self.isEnd:
            self.isEnd = False
            for key, rowCol in Spot.end_points.items():
                if self.row == rowCol[0] and self.col == rowCol[1]:
                    Spot.end_points.pop(key)
        
    def make_path(self):
        self.isPath = True
        if self.isDoor or self.button['bg'] == globals.rgbtohex(0,128,0): # don't change the color if the spot is a door or the initial starting point of the robot
            return 
        if self.isEnd:
            self.button.config(bg = globals.rgbtohex(150,0,0)) # dark red
            self.isEnd = False
        else: # otherwise, turn the current spot's color to gold, indicating that the robot will eventually traverse it
            self.button.config(bg = "gold")
        
    def make_to_visit(self):
        self.button.config(bg = "pink")

    def make_backtracking(self):
        self.button.config(bg = "SteelBlue1")
        
    def make_open(self):
        if not (self.isPath or self.isDoor) : # color the spot if it is not traversed by the robot and spot is not a door
            self.button.config(bg = "cornflower blue")
    
    def open_door(self):
        self.button.config(bg = "white")

    def close_door(self):
        self.button.config(bg = globals.rgbtohex(64, 224, 208)) # Turqoise Colour

    def make_closed(self):
        if not (self.isPath or self.isDoor): # color the spot if it is not traversed by the robot and spot is not a door
            self.button.config(bg = "LightSkyBlue2")
        
    def disable(self):
        self.button.config(state=DISABLED)
    
    def enable(self):
        self.button.config(state=NORMAL)
    
    def click(self):
        if self.clicked: # spot was already clicked, so reset it to original state
            hexString = self.button['bg']
            if hexString[0] != "#": # then it is a color like "lime green" or any other name, so it is not an end point and we should just reset it
                self.reset()
            r,g,b = globals.hextorgb(hexString)
            if g == 0 and b == 0: # then it is a shade of red, so it is an end point
                removedId = -1
                for id, rowCol in Spot.end_points.items():
                    if self.row == rowCol[0] and self.col == rowCol[1]:
                        removedId = id
                        break
                if removedId == -1:
                    self.reset()
                    return
                ids = list(Spot.end_points.keys())
                for curId in ids:
                    curPoint = globals.grid[Spot.end_points[curId][0]][Spot.end_points[curId][1]]
                    idToBeChanged = int(curPoint.button['text'])
                    if idToBeChanged <= removedId:
                        continue
                    if idToBeChanged == 2: # then we should make its "isEnd" variable to True, since this will now have id "1" and is therefore the next end in the algorithm
                        curPoint.make_end(asObstacle=False)
                    curPoint.button.config(text=f'{idToBeChanged-1}', fg='white')
                    Spot.end_points[idToBeChanged-1] = Spot.end_points[idToBeChanged]
                    Spot.end_points.pop(idToBeChanged)
                    Spot.staffId -= 1
            self.reset()
            return
        if globals.isSpotType('Robot') and not Spot.start_point:   
            self.make_start()
        elif globals.isSpotType('Staff'):
            self.make_end(userClicked = True)
        elif globals.isSpotType('Obstacle'):
            self.make_obstacle()
        elif globals.isSpotType('Door'):
            self.make_door()
            
    
    def update_neighbors(self, grid):
        self.neighbors = []

        # check neighbors a row down - if spot not outside grid and not obstacle
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].isObstacle:
            self.neighbors.append(grid[self.row + 1][self.col]) # add spot to the neighbors

        # check neighbors a row up - if spot not outside grid and not obstacle
        if self.row > 0 and not grid[self.row - 1][self.col].isObstacle:
            self.neighbors.append(grid[self.row - 1][self.col]) # add spot to the neighbors

        # check neighbors a col right - if spot not outside grid and not obstacle
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].isObstacle:
            self.neighbors.append(grid[self.row][self.col + 1]) # add spot to the neighbors

        # check neighbors a col left - if spot not outside grid and not obstacle
        if self.col > 0 and not grid[self.row][self.col - 1].isObstacle:
            self.neighbors.append(grid[self.row][self.col - 1]) # add spot to the neighbors
