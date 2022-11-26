########################################################################
# Cafe Robot Scenario: Visualizing the Pathfinding Algorithm & Environment Scenarios
# Used tkinter
# Python 3.10.5
# Ashraf Haress 
# 20/11/2022
########################################################################
# Main Resource:
# @DariaSVasileva: Pathfinding_Algorithm_Visualizer_tkinter
# https://github.com/DariaSVasileva/Pathfinding_Algorithm_Visualizer_tkinter
# 
# Which is based on these resources:
# 
# @Tech With Tim: Python A* Path Finding Tutorial
# https://www.youtube.com/watch?v=JtiK0DOeI4A&ab_channel=TechWithTim
#
# @Daksh3K: Astar-Pathfinding-Algorithm-Visualization
# https://github.com/Daksh3K/Astar-Pathfinding-Algorithm-Visualization
#
# @nas-programmer: path-finding
# https://github.com/nas-programmer/path-finding
# https://www.youtube.com/watch?v=LF1h-8bEjP0&ab_channel=codeNULL
#
# @Davis MT: Python maze generator program
# https://github.com/tonypdavis/PythonMazeGenerator
# https://www.youtube.com/watch?v=Xthh4SEMA2o&ab_channel=DavisMT
#########################################################################

# To-Do:
# 1. make 4 buttons: Robot Loc, Obstacle Locs, Door Locs, Staff Locs
# 2. change "Spot" code to accommodate for change in 1.
    # 2.1 instead of relying on #clicks, make insertion of colors be based on combobox on the right
    # 2.2 change colors based on chosen combobox value
    # 2.3 make sure everything works (color of door does same job as empty cell)
    # 2.4 when choosing red in combobox (i.e., staff): 
        # 2.4.1 make list of pairs: 
            # 1st elem. is pair of (r,c) of clicked spot
            # 2nd elem. is click # since red value is chosen in combobox
        # 2.4.2 try to add numbers from 2nd elem. on GUI
        # 2.4.3 try to add text box below right combobox with this structure:
            # "#clickNum, StaffName"
            # possible failure scenario: make global list to check if name is actually
            # a staff member, if not, write in text box: this is not a staff member!
# 3. change reconstruct_path to accommodate for 2.

from tkinterReloader import run_with_reloader
import globals

if __name__ == "__main__":
    globals.init()
    run_with_reloader(globals.root, "<Control-R>", "<Control-r>")