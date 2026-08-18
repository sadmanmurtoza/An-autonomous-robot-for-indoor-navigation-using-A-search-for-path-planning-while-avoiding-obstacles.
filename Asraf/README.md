# Autonomous Robot for Indoor Navigation Using A* Search

This project follows the supplied CSE440 work plan. It is a **software-only** indoor-navigation simulator. The map is a 2D occupancy grid where **0 = free** and **1 = obstacle**. The user can create/load maps, place/remove obstacles, choose a start and destination, run A*, see explored cells/path/robot movement, and add a dynamic obstacle while the robot is moving.

## Easiest way to run on Windows

1. Extract the project ZIP.
2. Open the extracted folder.
3. Double-click **`setup_and_run.bat`**.
4. If Python is already installed, the program starts immediately.
5. If Python is missing and `winget` is available, the script tries to install official Python 3.12 automatically.
6. No extra `pip install` libraries are needed.

## Manual run

Open Command Prompt/PowerShell inside the project folder and run:

```text
python main.py
```

If Windows uses the Python launcher instead:

```text
py main.py
```

## How to use the simulator

1. Click **Choose Start**, then click a free white cell.
2. Click **Choose Destination**, then click another free cell.
3. Click **Add Obstacle**, then click cells to build walls.
4. Click **Find A* Path** to show the calculated safe route.
5. Click **Run Robot** to watch the virtual robot move.
6. While the robot moves, keep **Add Obstacle** selected and click a cell in its future route. The map updates immediately. If the new obstacle blocks the route, A* calculates a new route from the robot's current location.
7. Use **Pause / Continue / Stop** to control movement.
8. Use **Save Map** and **Load Map** for JSON map files.
9. Use **New Map / Grid Size** to test small or large grids.
10. Use **Reset Simulation** to remove path/travel history without deleting the map.

## Color guide

- White = free cell
- Black = obstacle
- Green = start
- Red = destination
- Light blue = cells explored by A*
- Yellow = calculated path / remaining route
- Orange = travelled cells
- Purple = virtual robot

## Files

- `main.py` - graphical interface, visualization, robot simulation, live obstacle updates, controls.
- `astar.py` - A* path-planning algorithm.
- `map_model.py` - occupancy grid, obstacle management, map save/load.
- `test_project.py` - small automatic test for the map and A* code.
- `setup_and_run.bat` - Windows setup + run launcher.
- `run_project.sh` - Linux/macOS launcher.
- `requirements.txt` - confirms that no external pip libraries are needed.

## Automatic test

Run:

```text
python test_project.py
```

A correct result prints `All automatic tests passed.`

## How this matches the 7-week plan

- **Week 1:** project structure, software workflow, GUI/map modules.
- **Week 2:** 2D occupancy grid; 0 free / 1 blocked; create/load; add/remove obstacles.
- **Week 3:** visual states; start, destination, obstacles, explored cells, path, robot; A* integration.
- **Week 4:** robot movement; travelled cells and remaining route are visible and refreshed after each movement.
- **Week 5:** dynamic obstacle placement; immediate live map update; A* replanning when the route is blocked.
- **Week 6:** GUI controls for maps, start/goal, obstacles, run/pause/stop, clearing, and reset.
- **Week 7:** automatic logic test plus code organization and comments. You can use small/large grids and different obstacle patterns for final screenshots/testing.
