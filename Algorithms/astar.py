from queue import PriorityQueue

import pygame

from Algorithms.pathFinding.Spot import Spot
from Algorithms.pathFinding.SpotState import SpotState

pygame.init()


def start_pathfinding(start, end, grid):
    """
    Find the shortest path from the start to the end.

        Parameters:
            start (Spot): The start of the path
            end (Spot): The end of the path
            grid (list[list[Spot]]): The grid to find the path in

        Returns:
            None
    """

    # Initialises the count to determine which Spot to take first
    count = 0

    # This uses heap sort to find the spot with the least f score
    openSet = PriorityQueue()

    # Adding the first item to the PriorityQueue
    openSet.put((0, count, start))

    # Tracks the visited Spot and its previous Spot
    # It is a dictionary with the key being the current Spot and the
    # value being the previous Spot
    came_from = {}

    # Initialises the g score of all the Spots in the grid
    gScore = {spot: float("inf") for row in grid for spot in row}
    gScore[start] = 0

    # Initialises the h score of all the Spots in the grid
    fScore = {spot: float("inf") for row in grid for spot in row}
    fScore[start] = h(start.get_pos(), end.get_pos())

    # This is used to determine the contents of the PriorityQueue as it is not readable
    openSet_hash = {start}

    # This keeps running until there is no more Spot to visit
    while not openSet.empty():
        # Event to close the pygame program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Gets and removes the Spot with the lowest f score from the PriorityQueue
        current = openSet.get()[2]
        openSet_hash.remove(current)

        # We have reached the end
        if current == end:
            return get_path(came_from, end)

        # Checks all the neighbor of the current Spot
        for neighbor in current.neighbors:
            # G score will always be one larger than the current
            tempgScore = gScore[current] + 1

            # Checks if we have found a shorter path to the neighbor Spot
            if tempgScore < gScore[neighbor]:
                came_from[neighbor] = current
                gScore[neighbor] = tempgScore
                fScore[neighbor] = tempgScore + h(neighbor.get_pos(), end.get_pos())

                # Checks if we have stores this in our path
                if neighbor not in openSet_hash:
                    count += 1
                    openSet.put((fScore[neighbor], count, neighbor))
                    openSet_hash.add(neighbor)
                    neighbor.make_open()
        # Makes the Spot closed if we have visited it
        if current != start:
            current.make_closed()
    return None


def h(p1: tuple[int, int], p2: tuple[int, int]):
    """
    Returns the Manhattan walk between the positions p1 and p2

            Parameters:
                    p1 (tuple[int, int]): The start position
                    p2 (tuple[int, int]): The end position

            Returns:
                    distance (str): The Manhattan distance between p1 and p2
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p1[1])


def get_path(came_from: dict[Spot], current: Spot) -> list[tuple[int, int]]:
    """
    Finds the list of positions of each Spot in the 'came from' dictionary

            Parameters:
                    came_from (dict[Spot]): A dictionary with the key being the current Spot and the
                        value being the previous Spot
                    current (Spot): The Spot being traced back from

            Returns:
                    positions (list[tuple[int,int]]): The list of positions of each Spot for the path
    """
    positions = []
    while current in came_from:
        current = came_from[current]
        positions.append(current.get_pos())
    return positions


def make_grid(maze: list[list[int]]) -> list[list[Spot]]:
    """
    Returns the Manhattan walk between the positions p1 and p2

            Parameters:
                    maze (list[list[int]]): The maze encoded just like in maze.py

            Returns:
                    grid (list[list[Spot]]): The grid with each item being a spot
    """
    grid = []
    for y, i in enumerate(maze):
        grid.append([])
        for x, j in enumerate(i):
            if 7 > maze[y][x] >= 0:
                spot = Spot(y, x, len(maze), len(maze[x]), SpotState.BARRIER)
            else:
                spot = Spot(y, x, len(maze), len(maze[x]), SpotState.OPEN)
            grid[y].append(spot)
    return grid
