from tkinter import Button, messagebox, GROOVE, DISABLED, NORMAL
import globals

# define class - spot
class Spot():
    
    start_point = None
    end_points = {}
    staffId = 1

    __slots__ = ['button','row', 'col', 'width', 'neighbors', 'g', 'h', 'f',  
                 'parent', 'isStart', 'isEnd', 'isObstacle', 'isDoor', 'clicked', 'total_rows']
    
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
        self.clicked = False
        self.total_rows = total_rows
    
    def make_start(self):
        self.button.config(bg = "lime green")
        self.isStart = True
        self.clicked = True
        Spot.start_point = (self.col, self.row)
        
    def make_end(self):
        self.button.config(bg = globals.rgbtohex(max(100, abs(255-Spot.staffId*14)),0,0))
        self.isEnd = True
        self.clicked = True
        Spot.end_points[Spot.staffId] = (self.col, self.row)
        Spot.staffId += 1
        
    def make_obstacle(self):
        self.button.config(bg = "black")
        self.isObstacle = True
        self.clicked = True

    def make_door(self):
        self.button.config(bg = globals.rgbtohex(64, 224, 208)) # Turqoise Colour
        self.isDoor = True
        self.clicked = True
        
    def reset(self):
        self.button.config(bg = "white")
        self.clicked = False
        if self.isStart:   
            self.isStart = False
            Spot.start_point = None
        elif self.isEnd:
            self.isEnd = False
            for key, valuePair in Spot.end_points:
                if self.row == valuePair[0] and self.col == valuePair[1]:
                    Spot.end_points.pop(key)
        elif self.isObstacle:
            self.isObstacle = False
        elif self.isDoor:
            self.isDoor = False
        
    def make_path(self):
        self.button.config(bg = "gold")
        
    def make_to_visit(self):
        self.button.config(bg = "pink")

    def make_backtracking(self):
        self.button.config(bg = "SteelBlue1")
        
    def make_open(self):
        self.button.config(bg = "cornflower blue")
        
    def make_closed(self):
        self.button.config(bg = "LightSkyBlue2")
        
    def disable(self):
        self.button.config(state=DISABLED)
    
    def enable(self):
        self.button.config(state=NORMAL)
    
    def click(self):
        if self.clicked: # spot was already clicked, so reset it to original state
            self.reset()
            return
        if globals.isSpotType('Robot') and not Spot.start_point:   
            self.make_start()
        elif globals.isSpotType('Staff'):
            self.make_end()
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
