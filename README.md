# cafe-robot-pathfinding-visualized

This project visualizes different pathfinding algorithms. It's written in Python and uses the Tkinter library for the GUI.

## Usage

### [`main.py`](main.py)

This is the entry point of the application. It initializes the GUI and sets up the grid for the pathfinding visualization.

### [`algorithms.py`](algorithms.py)

This file contains the implementation of the pathfinding algorithms. It includes functions for A-star and Breadth-First algorithms, as well as functions for traversing and visualizing the path.

### [`Spot.py`](Spot.py)

This file defines the `Spot` class, which represents a spot on the grid. Each spot has attributes like its position, its neighbors, and whether it's a start, end, obstacle, or door spot.

### [`Presets.py`](Presets.py)

This file contains the `Presets` class, which is used to build and load presets for the grid.

### [`globals.py`](globals.py)

This file initializes global variables and functions used across the application.

## Phase 1
Details of phase 1 can be found in [phase 1's project document](https://nbviewer.org/github/OdyAsh/cafe-robot-pathfinding-visualized/blob/main/Project%20Scenario%20And%20Design/Phase%201/Ashraf%20196280%20-%20Caf%C3%A9%20Robot%20%28Assignment%201%29.pdf)

(Note: it is preferable to download the [.docx version](https://github.com/OdyAsh/cafe-robot-pathfinding-visualized/blob/main/Project%20Scenario%20And%20Design/Phase%201/Ashraf%20196280%20-%20Caf%C3%A9%20Robot%20(Assignment%201).docx) instead of viewing the pdf version, as the .docx version displays gifs properly.)

Example scenario:

![Scenario 1](./Project%20Scenario%20And%20Design/Phase%201/media%20assets/Scenario%201.gif)

Example of representing the environment (staff room) as a 2D grid:

![Grid representation](./Project%20Scenario%20And%20Design/Phase%201/media%20assets/gridRep.gif)

## Phase 2
Details of phase 2 can be found in [phase 2's project document](https://nbviewer.org/github/OdyAsh/cafe-robot-pathfinding-visualized/blob/main/Project%20Scenario%20And%20Design/Phase%202/Ashraf%20196280%20-%20Caf%C3%A9%20Robot%20%28Assignment%202%29.pdf)

(Note: it is preferable to download the [.docx version](https://github.com/OdyAsh/cafe-robot-pathfinding-visualized/blob/main/Project%20Scenario%20And%20Design/Phase%202/Ashraf%20196280%20-%20Caf%C3%A9%20Robot%20(Assignment%202).docx) instead of viewing the pdf version, as the .docx version displays gifs properly.)

Examples of the application running on different environments:

![Crooked smiley face](./Project%20Scenario%20And%20Design/Phase%202/media%20assets/Crooked%20smiley%20face%20(with%20random%20name).gif)

![Random walls with random staff names](./Project%20Scenario%20And%20Design/Phase%202/media%20assets/Random%20walls%20with%20random%20staff%20names.gif)

![Staff floor scenario](./Project%20Scenario%20And%20Design/Phase%202/media%20assets/staff%20floor%20scenario%20(faster).gif)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
