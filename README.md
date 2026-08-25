# GROUP 6 — AUTONOMOUS INDOOR NAVIGATION ROBOT USING A* SEARCH

An autonomous indoor navigation robot simulation developed using **Python, Tkinter, and A* Search**. The system creates a grid map, finds the shortest safe path, controls a virtual robot, and replans when a new obstacle appears.

**Course:** CSE 440 — Artificial Intelligence
**Group:** 06 | **Section:** 02
**Institution:** North South University
**Semester:** Summer 2026

---

## Group Members

| # | Name                   | File                      | Responsibility              |
| - | ---------------------- | ------------------------- | --------------------------- |
| 1 | **MD Asraful Hossain** | `member1_asraful_map.py`  | Map & obstacles             |
| 2 | **Sadman**             | `member2_sadman_astar.py` | A* pathfinding & replanning |
| 3 | **Fahima**             | `member3_fahima_robot.py` | Robot movement & safety     |
| 4 | **Sanjida Jaman**      | `member4_gui_graphics.py` | GUI & visualization         |

**Whole Group:** `main.py` — Integrates all modules and starts the system.

---
## Overview

* This project is an Autonomous Indoor Navigation Robot simulation designed to demonstrate how a robot can navigate an indoor environment while avoiding obstacles.

* The environment is represented using an occupancy grid, where each cell represents a location in the environment:

0 → Free cell
1 → Obstacle

* The user can select a start position and destination, create obstacles, and ask the system to calculate a safe route.

* The project uses A Search* to find the shortest safe path. During movement, if a new obstacle appears on the robot's planned route, the robot safely stops before the blocked cell and the system calculates a new route.

* The complete application is divided into four member modules and one integration file:

* Map → A* Path Planning → Robot → GUI
                 ↑
              main.py

* The four member files and their responsibilities are defined in the project documentation.

## Features

* Occupancy-grid map (`0 = free`, `1 = obstacle`)
* Start and destination selection
* Add/remove obstacles
* A* shortest-path search
* Explored-node and performance tracking
* Virtual robot movement
* Dynamic obstacle detection
* Automatic path replanning
* Interactive Tkinter GUI
* System testing

---

## Project Structure

```text
├── main.py
├── member1_asraful_map.py
├── member2_sadman_astar.py
├── member3_fahima_robot.py
├── member4_gui_graphics.py
├── README.md
└── setup_and_run.bat
```

---

## How to Run

### Requirements

* Python 3.x
* Tkinter
* No external graphics package required

### Run

```bash
python main.py
```

On Windows, you can also run:

```text
setup_and_run.bat
```

---

## Demo Workflow

```text
Map
 ↓
Set Start & Destination
 ↓
Add Obstacles
 ↓
Find A* Path
 ↓
Run Robot
 ↓
Obstacle Appears
 ↓
Robot Stops
 ↓
A* Replans
 ↓
Robot Reaches Destination
```

The documented demo follows this same workflow.

---

## Goal

**Map → Plan → Move → Detect → Replan → Reach**

A modular autonomous navigation system demonstrating **A* pathfinding, robot control, dynamic obstacle handling, and GUI visualization**.
