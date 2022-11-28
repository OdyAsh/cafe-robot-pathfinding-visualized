########################################################################
# Cafe Robot Scenario: Visualizing the Pathfinding Algorithm & Environment Scenarios
# Used tkinter
# Python 3.10.5
# Ashraf Haress 
# 20/11/2022 (The code in the rest of the files was reviewed by the TAs on 27/11/2022)
########################################################################

import globals
from Gui import Gui
if __name__ == "__main__":
    globals.init()
    # accessing ui() as a class function instead of an instance (object) method.. 
    # example (using attributes) is here: https://stackoverflow.com/questions/4152850/is-it-possible-not-to-use-self-in-a-class
    # and here: https://stackoverflow.com/questions/136097/classmethod-vs-staticmethod-in-python
    Gui.ui() 
    # show instructions when the Gui appears
    # Gui.instructions() # un-comment this if you want instructions to appear everytime you start up the application
    # run loop 
    globals.root.mainloop()