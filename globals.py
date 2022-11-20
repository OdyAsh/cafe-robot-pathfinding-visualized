from tkinter import Tk, StringVar
# this file contains the global GUI elements globally used by all the classes

# logic of the gloabal variables part is to avoid opening two windows parallely 
# (as from main import GUI line in Spot.py runs the class variables a second time)
# source: https://stackoverflow.com/questions/13034496/using-global-variables-between-files#:~:text=The%20problem%20is%20you%20defined%20myList%20from%20main.py%2C%20but%20subfile.py%20needs%20to%20use%20it.%20Here%20is%20a%20clean%20way%20to%20solve%20this%20problem%3A%20move%20all%20globals%20to%20a%20file%2C%20I%20call%20this%20file%20settings.py.%20This%20file%20is%20responsible%20for%20defining%20globals%20and%20initializing%20them%3A

def init(): 
    # initialize main window
    global root, font, selected_alg, selected_bld, WIDTH, ROWS, grid, UI_frame, canvas, bldMenu, wallsScale, algMenu, speedScale
    root = Tk()
    root.title('Pathfinding Algorithm Visualisation')
    root.maxsize(900, 900)
    root.config(bg='black')

    font = ("Helvetica", 11)

    # Variables
    selected_alg = StringVar()
    selected_bld = StringVar()
    WIDTH = 500
    ROWS = 25
    grid = []
    # Store variables as attributes
    UI_frame = None
    canvas = None
    bldMenu = None
    wallsScale = None
    algMenu = None
    speedScale = None