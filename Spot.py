from tkinter import Button, messagebox, GROOVE, DISABLED, NORMAL
import globals

# define class - spot
class Spot():
    
    start_point = None
    end_point = None
    
    __slots__ = ['button','row', 'col', 'width', 'neighbors', 'g', 'h', 'f',  
                 'parent', 'isStart', 'isEnd', 'obstacle', 'clicked', 'total_rows']
    
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
        self.obstacle = False
        self.clicked = False
        self.total_rows = total_rows
    
    def make_start(self):
        self.button.config(bg = "lime green")
        self.isStart = True
        self.clicked = True
        Spot.start_point = (self.col, self.row)
        
    def make_end(self):
        self.button.config(bg = "Red")
        self.isEnd = True
        self.clicked = True
        Spot.end_point = (self.col, self.row)
        
    def make_obstacle(self):
        self.button.config(bg = "black")
        self.obstacle = True
        self.clicked = True
        
    def reset(self):
        self.button.config(bg = "white")
        self.clicked = False
        
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
        if self.clicked == False:
            if not Spot.start_point:   
                self.make_start()
            elif not Spot.end_point:
                self.make_end()
            else :
                self.make_obstacle()
        else:
            self.reset()
            if self.isStart == True:   
                self.isStart = False
                Spot.start_point = None
            elif self.isEnd == True:
                self.isEnd = False
                Spot.end_point = None
            else :
                self.obstacle = False
    
    def update_neighbors(self, grid):
        self.neighbors = []

        # check neighbors a row down - if spot not outside grid and not obstacle
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].obstacle:
            self.neighbors.append(grid[self.row + 1][self.col]) # add spot to the neighbors

        # check neighbors a row up - if spot not outside grid and not obstacle
        if self.row > 0 and not grid[self.row - 1][self.col].obstacle:
            self.neighbors.append(grid[self.row - 1][self.col]) # add spot to the neighbors

        # check neighbors a col right - if spot not outside grid and not obstacle
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].obstacle:
            self.neighbors.append(grid[self.row][self.col + 1]) # add spot to the neighbors

        # check neighbors a col left - if spot not outside grid and not obstacle
        if self.col > 0 and not grid[self.row][self.col - 1].obstacle:
            self.neighbors.append(grid[self.row][self.col - 1]) # add spot to the neighbors
