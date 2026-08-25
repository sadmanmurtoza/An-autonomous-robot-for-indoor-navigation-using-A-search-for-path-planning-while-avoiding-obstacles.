# Group 6 - Autonomous Indoor Navigation Robot Using A* Search

The program uses only Python and Tkinter. No external graphics package is needed.

## Member files and responsibilities

| Member | File | Main work |
|---|---|---|
| Member 1 - MD Asraful Hossain | `member1_asraful_map.py` | Occupancy grid, new map, add/remove obstacles, start/goal, save/load map |
| Member 2 - Sadman | `member2_sadman_astar.py` | A* shortest path, explored nodes, validation, replanning, performance values |
| Member 3 - Fahima | `member3_fahima_robot.py` | Virtual robot, movement, travelled/remaining cells, pause/resume, dynamic obstacle safety |
| Member 4 - Sanjida Jaman| `member4_gui_graphics.py` | Window, buttons, colors, robot icon, warnings, performance panel, system tests |
| Whole group | `main.py` | Connects all four member modules and starts the project |

If Member 4 has a name, replace "Member 4" in this file and at the top of `member4_gui_graphics.py`.

## Easy explanation to memorize

- Member 1 creates the indoor map.
- Member 2 finds the shortest safe route with A*.
- Member 3 moves the virtual robot and reacts to a new obstacle.
- Member 4 displays everything and tests the complete system.
- `main.py` joins the four parts.

## New graphics

- Dark presentation-style control panel
- Blue buttons and live status card
- Colored performance dashboard
- Start and destination rings
- Small robot-face icon
- Yellow route dots
- X patterns on obstacle walls
- Clear colors for explored, travelled, and remaining cells

## Run on Windows

Double-click `setup_and_run.bat`, or open a terminal in the folder and run:

```bash
python main.py
```

## Demonstration

1. Click **Choose Start**, then click a free cell.
2. Click **Choose Destination**, then click another free cell.
3. Use **Add Obstacle** to create walls.
4. Click **Find A* Path** to display the shortest route.
5. Click **Run Robot** to move the robot.
6. Add an obstacle on the yellow route while the robot moves.
7. The robot stops before the obstacle and A* calculates a new route.
8. Click **Run System Tests** to show the automatic test results.
