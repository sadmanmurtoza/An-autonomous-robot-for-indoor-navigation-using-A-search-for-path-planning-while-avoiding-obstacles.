# Autonomous Indoor Navigation Robot Using A* Search

## Group 6 Project

This project is a Python-based simulation of an autonomous indoor navigation robot. The system represents an indoor environment as an occupancy grid and uses the A* search algorithm to calculate a safe shortest path from a selected starting position to a destination.

The project also includes a virtual robot that follows the calculated route, detects newly added obstacles, and supports dynamic replanning. A graphical user interface built with Tkinter allows the user to create maps, place obstacles, select start and destination cells, visualize the A* search, and control the robot.

## Team Members and Responsibilities

| Member | Project File | Responsibility |
|---|---|---|
| MD Asraful Hossain | `map_model.py` | Occupancy-grid map, grid creation, obstacle management, start/destination selection, and map save/load |
| Sadman | `astar.py` | A* path-planning algorithm, heuristic calculation, shortest-path search, path validation, explored-node tracking, performance measurement, and replanning |
| Fahima | `virtual_robot.py` | Virtual robot movement, travelled/remaining path management, pause/resume, stopping, dynamic-obstacle detection, and replanned-path handling |
| Sanjida Jaman | `gui_graphics.py` | Graphical user interface, grid visualization, controls, colors, robot graphics, warnings, performance display, and system testing |
| Whole Group | `main.py` | Creates the project components, connects the modules, and starts the complete application |

## Main Features

- Interactive occupancy-grid environment
- User-selectable start and destination positions
- Add and remove obstacles
- A* shortest-path calculation
- Manhattan-distance heuristic
- Visualization of explored cells and final route
- Animated virtual robot movement
- Pause, resume, stop, and reset controls
- Dynamic obstacle detection
- Automatic A* replanning when the route becomes blocked
- Path validation and safety checking
- Path length, explored-node count, and calculation-time display
- Save and load maps
- Built-in system testing
- Presentation-friendly graphical interface

## Project Structure

```text
project/
├── main.py
├── map_model.py
├── astar.py
├── virtual_robot.py
├── gui_graphics.py
├── test_integration.py
├── setup_and_run.bat
├── run_project.sh
└── README.md
```

### `main.py`
The entry point of the application. It creates the map, A* planner, virtual robot, and GUI objects and connects them together.

### `map_model.py`
Maintains the occupancy grid. A value of `0` represents a free cell and `1` represents an obstacle. It also handles start/destination selection and saving/loading maps.

### `astar.py`
Implements A* search. The planner uses Manhattan distance because movement is limited to up, down, left, and right. It returns the shortest available route along with explored nodes and performance information.

### `virtual_robot.py`
Represents the simulated robot. It follows the A* route one cell at a time, maintains its current and travelled positions, and detects when its next planned cell becomes blocked.

### `gui_graphics.py`
Provides the Tkinter graphical interface. It displays the map, obstacles, start and destination, explored cells, route, travelled cells, and robot. It also connects user actions to the other project modules.

### `test_integration.py`
Provides a non-GUI integration test for the main project modules.

## Requirements

- Python 3
- Tkinter

The project does not require an external graphics library. Tkinter is included with standard Python installations on many systems.

## How to Run

Make sure the following files are in the same project folder:

```text
main.py
map_model.py
astar.py
virtual_robot.py
gui_graphics.py
```

Open Command Prompt, PowerShell, or a terminal in that folder and run:

```bash
python main.py
```

On some Linux systems, use:

```bash
python3 main.py
```

Windows users can also run:

```text
setup_and_run.bat
```

Linux/macOS users can use:

```bash
./run_project.sh
```

## How to Use the Simulator

1. Start the application.
2. Select **Choose Start** and click a free grid cell.
3. Select **Choose Destination** and click another free cell.
4. Use **Add Obstacle** to create walls or blocked cells.
5. Click **Find A* Path** to calculate and visualize the shortest safe route.
6. Click **Run Robot** to start the virtual robot.
7. Use **Pause**, **Resume**, or **Stop** when required.
8. While the robot is moving, add an obstacle to its remaining route to demonstrate dynamic replanning.
9. The robot detects the blocked next cell, stops before entering it, and A* searches for a new safe route.
10. Use **Run System Tests** to test the integrated system.

## A* Path-Planning Process

The A* planner evaluates cells using:

```text
f(n) = g(n) + h(n)
```

where:

- `g(n)` is the actual movement cost from the starting cell to the current cell.
- `h(n)` is the estimated distance from the current cell to the destination.
- `f(n)` is the estimated total path cost.

Because the robot moves only horizontally and vertically, the project uses Manhattan distance as the heuristic.

## Dynamic Replanning

The project can respond to obstacles that appear after the robot has started moving. Before moving into the next planned cell, the robot checks whether that cell has become blocked. If it is blocked, the robot remains at its current safe position and the A* planner recalculates a route from the robot's current position to the destination.

If another valid route exists, the robot accepts the new route and continues. If no route exists, the robot stops safely.

## GUI Visualization

The interface uses different visual indicators for:

- Free cells
- Obstacles
- Start position
- Destination
- Explored cells
- Remaining A* path
- Travelled cells
- Current robot position

The interface also displays path length, number of explored nodes, and A* calculation time.

## Testing

To test the core modules without opening the GUI, run:

```bash
python test_integration.py
```

A successful test displays:

```text
ALL CORE INTEGRATION TESTS PASSED
```

The GUI also includes a **Run System Tests** button for integrated testing.

## Project Objective

The objective of this project is to demonstrate how an intelligent agent can navigate an indoor grid environment using informed search. A* provides efficient shortest-path planning, while dynamic replanning allows the simulated robot to respond safely when the environment changes.

## Technologies Used

- Python
- Tkinter
- A* Search Algorithm
- Priority Queue
- Manhattan Distance Heuristic
- Occupancy Grid Mapping
- Dynamic Path Replanning

## Conclusion

The Autonomous Indoor Navigation Robot combines environment representation, A* path planning, robot-state management, dynamic replanning, visualization, and testing in a modular Python application. Dividing the system into separate modules makes each team member's contribution clear while allowing all components to work together through `main.py`.
