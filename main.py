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

from Gui import Gui
import globals

if __name__ == "__main__":
    globals.init()
    Gui.start()