import tkinter as tk

from map_model import GridMap
from astar import AStarPlanner
from virtual_robot import VirtualRobot
from gui_graphics import RobotGUI


def main():
    root = tk.Tk()

    grid_map = GridMap()
    planner = AStarPlanner()
    robot = VirtualRobot()

    RobotGUI(root, grid_map, planner, robot)

    root.mainloop()


if __name__ == "__main__":
    main()
