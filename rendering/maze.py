#!/bin/python3
import math

import pygame

"""
Drawing the maze :
Which number indicates which shape:
0 : White horizontal line for ghost ONLY to pass through
1 : blue horizontal line
11 : blue horizontal line (thicker)
2 : blue vertical line
12 : blue vertical line (thicker)
3 : top right corner (blue)
13 : top right corner (blue and thicker)
4 : top left corner (blue)
14 : top left corner (blue and thicker)
5 : bottom left corner (blue)
15 : bottom left corner (blue and thicker)
6 : bottom right corner (blue)
16 : bottom right corner (blue and thicker)
7 : rectangle (black)
8 : white small dot for score
9 : Big white dot for power up
"""

pygame.init()

# Defining the size of the window
WIDTH = 750
HEIGHT = 875

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman 2.0")

# 33 rows
# 30 columns
Maze = [
    [14, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 13],
    [12, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 12],
    [12, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 12],
    [12, 2, 8, 4, 1, 1, 3, 8, 4, 1, 1, 1, 3, 8, 2, 2, 8, 4, 1, 1, 1, 3, 8, 4, 1, 1, 3, 8, 2, 12],
    [12, 2, 9, 2, 7, 7, 2, 8, 2, 7, 7, 7, 2, 8, 2, 2, 8, 2, 7, 7, 7, 2, 8, 2, 7, 7, 2, 9, 2, 12],
    [12, 2, 8, 5, 1, 1, 6, 8, 5, 1, 1, 1, 6, 8, 5, 6, 8, 5, 1, 1, 1, 6, 8, 5, 1, 1, 6, 8, 2, 12],
    [12, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 12],
    [12, 2, 8, 4, 1, 1, 3, 8, 4, 3, 8, 4, 1, 1, 1, 1, 1, 1, 3, 8, 4, 3, 8, 4, 1, 1, 3, 8, 2, 12],
    [12, 2, 8, 5, 1, 1, 6, 8, 2, 2, 8, 5, 1, 1, 3, 4, 1, 1, 6, 8, 2, 2, 8, 5, 1, 1, 6, 8, 2, 12],
    [12, 2, 8, 8, 8, 8, 8, 8, 2, 2, 8, 8, 8, 8, 2, 2, 8, 8, 8, 8, 2, 2, 8, 8, 8, 8, 8, 8, 2, 12],
    [12, 5, 1, 1, 1, 1, 3, 8, 2, 5, 1, 1, 3, 7, 2, 2, 7, 4, 1, 1, 6, 2, 8, 4, 1, 1, 1, 1, 6, 12],
    [12, 7, 7, 7, 7, 7, 2, 8, 2, 4, 1, 1, 6, 7, 5, 6, 7, 5, 1, 1, 3, 2, 8, 2, 7, 7, 7, 7, 7, 12],
    [12, 7, 7, 7, 7, 7, 2, 8, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2, 2, 8, 2, 7, 7, 7, 7, 7, 12],
    [16, 7, 7, 7, 7, 7, 2, 8, 2, 2, 7, 4, 1, 1, 0, 0, 1, 1, 3, 7, 2, 2, 8, 2, 7, 7, 7, 7, 7, 15],
    [1, 1, 1, 1, 1, 1, 6, 8, 5, 6, 7, 2, 7, 7, 7, 7, 7, 7, 2, 7, 5, 6, 8, 5, 1, 1, 1, 1, 1, 1],
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 2, 7, 7, 7, 7, 7, 7, 2, 7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7],
    [1, 1, 1, 1, 1, 1, 3, 8, 4, 3, 7, 2, 7, 7, 7, 7, 7, 7, 2, 7, 4, 3, 8, 4, 1, 1, 1, 1, 1, 1],
    [13, 7, 7, 7, 7, 7, 2, 8, 2, 2, 7, 5, 1, 1, 1, 1, 1, 1, 6, 7, 2, 2, 8, 2, 7, 7, 7, 7, 7, 14],
    [12, 7, 7, 7, 7, 7, 2, 8, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2, 2, 8, 2, 7, 7, 7, 7, 7, 12],
    [12, 7, 7, 7, 7, 7, 2, 8, 2, 2, 7, 4, 1, 1, 1, 1, 1, 1, 3, 7, 2, 2, 8, 2, 7, 7, 7, 7, 7, 12],
    [12, 4, 1, 1, 1, 1, 6, 8, 5, 6, 7, 5, 1, 1, 3, 4, 1, 1, 6, 7, 5, 6, 8, 5, 1, 1, 1, 1, 3, 12],
    [12, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 12],
    [12, 2, 8, 4, 1, 1, 3, 8, 4, 1, 1, 1, 3, 8, 2, 2, 8, 4, 1, 1, 1, 3, 8, 4, 1, 1, 3, 8, 2, 12],
    [12, 2, 8, 5, 1, 3, 2, 8, 5, 1, 1, 1, 6, 8, 5, 6, 8, 5, 1, 1, 1, 6, 8, 2, 4, 1, 6, 8, 2, 12],
    [12, 2, 9, 8, 8, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 2, 8, 8, 9, 2, 12],
    [12, 5, 1, 3, 8, 2, 2, 8, 4, 3, 8, 4, 1, 1, 1, 1, 1, 1, 3, 8, 4, 3, 8, 2, 2, 8, 4, 1, 6, 12],
    [12, 4, 1, 6, 8, 5, 6, 8, 2, 2, 8, 5, 1, 1, 3, 4, 1, 1, 6, 8, 2, 2, 8, 5, 6, 8, 5, 1, 3, 12],
    [12, 2, 8, 8, 8, 8, 8, 8, 2, 2, 8, 8, 8, 8, 2, 2, 8, 8, 8, 8, 2, 2, 8, 8, 8, 8, 8, 8, 2, 12],
    [12, 2, 8, 4, 1, 1, 1, 1, 6, 5, 1, 1, 3, 8, 2, 2, 8, 4, 1, 1, 6, 5, 1, 1, 1, 1, 3, 8, 2, 12],
    [12, 2, 8, 5, 1, 1, 1, 1, 1, 1, 1, 1, 6, 8, 5, 6, 8, 5, 1, 1, 1, 1, 1, 1, 1, 1, 6, 8, 2, 12],
    [12, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 12],
    [12, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 12],
    [15, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 16]
]

# Defining the cell HEIGHT and cell WIDTH
cellHeight = HEIGHT // 35
cellWidth = WIDTH // 30

mazeMask = pygame.mask.Mask((WIDTH, HEIGHT))


def create_mask() -> None:
    """Creating mask for maze."""

    # Creating a mask for the maze
    for row in range(len(Maze)):
        for col in range(len(Maze[row])):
            # 0 : white horizontal line
            if Maze[row][col] == 0:
                for x in range(0, cellWidth):
                    mazeMask.set_at((col * cellWidth + x, (row + 0.5) * cellHeight))

            # 1 : blue horizontal line
            if Maze[row][col] == 1:
                for x in range(0, cellWidth):
                    mazeMask.set_at((col * cellWidth + x, (row + 0.5) * cellHeight))

            # 2 : blue vertical line
            elif Maze[row][col] == 2:
                for y in range(0, cellHeight):
                    mazeMask.set_at(((col + 0.5) * cellWidth, row * cellHeight + y))

            # 3 : top right corner (blue)
            elif Maze[row][col] == 3:
                for x in range(cellWidth // 2 + 1):
                    mazeMask.set_at((col * cellWidth + x, (row + 0.5) * cellHeight))

                for y in range(cellHeight // 2 + 1):
                    mazeMask.set_at(
                        ((col + 0.5) * cellWidth, (row + 1) * cellHeight - y)
                    )

            # 4 : top left corner (blue)
            elif Maze[row][col] == 4:
                for x in range(cellWidth // 2 + 2):
                    mazeMask.set_at(
                        ((col + 1) * cellWidth - x, (row + 0.5) * cellHeight)
                    )

                for y in range(cellHeight // 2 + 1):
                    mazeMask.set_at(
                        ((col + 0.5) * cellWidth, (row + 1) * cellHeight - y)
                    )

            # 5 : bottom left corner (blue)
            elif Maze[row][col] == 5:
                for x in range(cellWidth // 2 + 2):
                    mazeMask.set_at(
                        ((col + 1) * cellWidth - x, (row + 0.5) * cellHeight)
                    )

                for y in range(cellHeight // 2):
                    mazeMask.set_at(((col + 0.5) * cellWidth, row * cellHeight + y))

            # 6 : bottom right corner (blue)
            elif Maze[row][col] == 6:
                for x in range(cellWidth // 2 + 1):
                    mazeMask.set_at((col * cellWidth + x, (row + 0.5) * cellHeight))

                for y in range(cellHeight // 2):
                    mazeMask.set_at(((col + 0.5) * cellWidth, row * cellHeight + y))


def draw_maze(step: int, maze_color, dot_color) -> None:
    """Drawing the maze."""

    currentStep = 0

    # Looping through the maze and drawing each element
    for row in range(len(Maze) // 2 + 1, len(Maze)):
        for col in range(len(Maze[row])):
            # Drawing debugging grids
            if currentStep > step:
                continue
            currentStep += 1

            # Debugging grid lines

            # pygame.draw.line(
            #     window,
            #     "red",
            #     (col * cellWidth, row * cellHeight),
            #     (col * cellWidth + cellWidth, row * cellHeight),
            #     1,
            # )
            # pygame.draw.line(
            #     window,
            #     "red",
            #     (col * cellWidth, row * cellHeight),
            #     (col * cellWidth, row * cellHeight + cellHeight),
            #     1,
            # )
            # pygame.draw.line(
            #     window,
            #     "red",
            #     (col * cellWidth + 1, row * cellHeight),
            #     (col * cellWidth, row * cellHeight + cellHeight),
            #     1,
            # )
            # pygame.draw.line(
            #     window,
            #     "red",
            #     (col * cellWidth, row * cellHeight + 1),
            #     (col * cellWidth + 1, row * cellHeight),
            #     1,
            # )

            # 0 : Drawing white horizontal lines
            if Maze[row][col] == 0:
                pygame.draw.line(
                    window,
                    dot_color,
                    (col * cellWidth, row * cellHeight + (0.5 * cellHeight)),
                    (
                        col * cellWidth + cellWidth,
                        row * cellHeight + (0.5 * cellHeight),
                    ),
                    1,
                )

            # 1 : blue horizontal line
            elif Maze[row][col] == 1:
                pygame.draw.line(
                    window,
                    maze_color,
                    (col * cellWidth, row * cellHeight + (0.5 * cellHeight)),
                    (
                        col * cellWidth + cellWidth,
                        row * cellHeight + (0.5 * cellHeight),
                    ),
                    1,
                )

            # 11 : Blue horizontal line (thicker)
            elif Maze[row][col] == 11:
                pygame.draw.line(
                    window,
                    maze_color,
                    (col * cellWidth, row * cellHeight + (0.5 * cellHeight)),
                    (
                        col * cellWidth + cellWidth,
                        row * cellHeight + (0.5 * cellHeight),
                    ),
                    4,
                )

            # 2 : blue vertical line
            elif Maze[row][col] == 2:
                pygame.draw.line(
                    window,
                    maze_color,
                    (col * cellWidth + (0.5 * cellWidth), row * cellHeight),
                    (
                        col * cellWidth + (0.5 * cellWidth),
                        row * cellHeight + cellHeight,
                    ),
                    1,
                )

            # 12 : Blue vertical line (thicker)
            elif Maze[row][col] == 12:
                pygame.draw.line(
                    window,
                    maze_color,
                    (col * cellWidth + (0.5 * cellWidth), row * cellHeight),
                    (
                        col * cellWidth + (0.5 * cellWidth),
                        row * cellHeight + cellHeight,
                    ),
                    5,
                )

            # 3 : top right corner (blue)
            elif Maze[row][col] == 3:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth - (cellWidth * 0.4)) - 2,
                        (row * cellHeight + (0.5 * cellHeight)),
                        cellWidth,
                        cellHeight,
                    ],
                    0,
                    math.pi / 2,
                    1,
                )

            # 13 : top right corner (blue and thicker)
            elif Maze[row][col] == 13:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth - (cellWidth * 0.5)) + 2,
                        (row * cellHeight + (0.5 * cellHeight)),
                        cellWidth,
                        cellHeight,
                    ],
                    0,
                    math.pi / 2,
                    5,
                )

            # 4 : top left corner (blue)
            elif Maze[row][col] == 4:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth + (cellWidth * 0.5)),
                        (row * cellHeight + (0.5 * cellHeight)),
                        cellWidth,
                        cellHeight,
                    ],
                    math.pi / 2,
                    math.pi,
                    1,
                )

            # 14 : top left corner (blue and thicker)
            elif Maze[row][col] == 14:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth + (cellWidth * 0.5)) - 1,
                        (row * cellHeight + (0.5 * cellHeight)),
                        cellWidth,
                        cellHeight,
                    ],
                    math.pi / 2,
                    math.pi,
                    5,
                )

            # 5 : bottom left corner (blue)
            elif Maze[row][col] == 5:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth + (cellWidth * 0.5)),
                        (row * cellHeight - (0.4 * cellHeight)) - 3,
                        cellWidth,
                        cellHeight,
                    ],
                    math.pi,
                    3 * math.pi / 2,
                    1,
                )

            # 15 : bottom left corner (blue and thicker)
            elif Maze[row][col] == 15:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth + (cellWidth * 0.5)),
                        (row * cellHeight - (0.4 * cellHeight)),
                        cellWidth,
                        cellHeight,
                    ],
                    math.pi,
                    3 * math.pi / 2,
                    5,
                )

            # 6 : bottom right corner (blue)
            elif Maze[row][col] == 6:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth - (cellWidth * 0.4)) - 2,
                        (row * cellHeight - (0.4 * cellHeight)) - 2,
                        cellWidth,
                        cellHeight,
                    ],
                    3 * math.pi / 2,
                    2 * math.pi,
                    1,
                )

            # 16 : bottom right corner (blue and thicker)
            elif Maze[row][col] == 16:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth - (cellWidth * 0.4)),
                        (row * cellHeight - (0.4 * cellHeight)),
                        cellWidth,
                        cellHeight,
                    ],
                    3 * math.pi / 2,
                    2 * math.pi,
                    5,
                )

            # 8 : Drawing white small dots
            elif Maze[row][col] == 8:
                pygame.draw.circle(
                    window,
                    dot_color,
                    (
                        col * cellWidth + (0.5 * cellWidth),
                        row * cellHeight + (0.5 * cellHeight),
                    ),
                    4,
                )

            # 9 : Drawing power ups dots
            elif Maze[row][col] == 9:
                pygame.draw.circle(
                    window,
                    dot_color,
                    (
                        col * cellWidth + (0.5 * cellWidth),
                        row * cellHeight + (0.5 * cellHeight),
                    ),
                    10,
                )

    currentStep = 0

    for row in range(len(Maze) // 2, -1, -1):
        for col in range(len(Maze[row])):
            # Drawing debugging grids
            if currentStep > step:
                continue
            currentStep += 1

            # Debugging grid lines

            # pygame.draw.line(
            #     window,
            #     "red",
            #     (col * cellWidth, row * cellHeight),
            #     (col * cellWidth + cellWidth, row * cellHeight),
            #     1,
            # )
            # pygame.draw.line(
            #     window,
            #     "red",
            #     (col * cellWidth, row * cellHeight),
            #     (col * cellWidth, row * cellHeight + cellHeight),
            #     1,
            # )
            # pygame.draw.line(
            #     window,
            #     "red",
            #     (col * cellWidth + 1, row * cellHeight),
            #     (col * cellWidth, row * cellHeight + cellHeight),
            #     1,
            # )
            # pygame.draw.line(
            #     window,
            #     "red",
            #     (col * cellWidth, row * cellHeight + 1),
            #     (col * cellWidth + 1, row * cellHeight),
            #     1,
            # )

            # 0 : Drawing white horizontal lines
            if Maze[row][col] == 0:
                pygame.draw.line(
                    window,
                    dot_color,
                    (col * cellWidth, row * cellHeight + (0.5 * cellHeight)),
                    (
                        col * cellWidth + cellWidth,
                        row * cellHeight + (0.5 * cellHeight),
                    ),
                    1,
                )

            # 1 : blue horizontal line
            elif Maze[row][col] == 1:
                pygame.draw.line(
                    window,
                    maze_color,
                    (col * cellWidth, row * cellHeight + (0.5 * cellHeight)),
                    (
                        col * cellWidth + cellWidth,
                        row * cellHeight + (0.5 * cellHeight),
                    ),
                    1,
                )

            # 11 : Blue horizontal line (thicker)
            elif Maze[row][col] == 11:
                pygame.draw.line(
                    window,
                    maze_color,
                    (col * cellWidth, row * cellHeight + (0.5 * cellHeight)),
                    (
                        col * cellWidth + cellWidth,
                        row * cellHeight + (0.5 * cellHeight),
                    ),
                    4,
                )

            # 2 : blue vertical line
            elif Maze[row][col] == 2:
                pygame.draw.line(
                    window,
                    maze_color,
                    (col * cellWidth + (0.5 * cellWidth), row * cellHeight),
                    (
                        col * cellWidth + (0.5 * cellWidth),
                        row * cellHeight + cellHeight,
                    ),
                    1,
                )

            # 12 : Blue vertical line (thicker)
            elif Maze[row][col] == 12:
                pygame.draw.line(
                    window,
                    maze_color,
                    (col * cellWidth + (0.5 * cellWidth), row * cellHeight),
                    (
                        col * cellWidth + (0.5 * cellWidth),
                        row * cellHeight + cellHeight,
                    ),
                    5,
                )

            # 3 : top right corner (blue)
            elif Maze[row][col] == 3:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth - (cellWidth * 0.4)) - 2,
                        (row * cellHeight + (0.5 * cellHeight)),
                        cellWidth,
                        cellHeight,
                    ],
                    0,
                    math.pi / 2,
                    1,
                )

            # 13 : top right corner (blue and thicker)
            elif Maze[row][col] == 13:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth - (cellWidth * 0.5)) + 2,
                        (row * cellHeight + (0.5 * cellHeight)),
                        cellWidth,
                        cellHeight,
                    ],
                    0,
                    math.pi / 2,
                    5,
                )

            # 4 : top left corner (blue)
            elif Maze[row][col] == 4:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth + (cellWidth * 0.5)),
                        (row * cellHeight + (0.5 * cellHeight)),
                        cellWidth,
                        cellHeight,
                    ],
                    math.pi / 2,
                    math.pi,
                    1,
                )

            # 14 : top left corner (blue and thicker)
            elif Maze[row][col] == 14:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth + (cellWidth * 0.5)),
                        (row * cellHeight + (0.5 * cellHeight)),
                        cellWidth,
                        cellHeight,
                    ],
                    math.pi / 2,
                    math.pi,
                    5,
                )

            # 5 : bottom left corner (blue)
            elif Maze[row][col] == 5:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth + (cellWidth * 0.5)),
                        (row * cellHeight - (0.4 * cellHeight)) - 3,
                        cellWidth,
                        cellHeight,
                    ],
                    math.pi,
                    3 * math.pi / 2,
                    1,
                )

            # 15 : bottom left corner (blue and thicker)
            elif Maze[row][col] == 15:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth + (cellWidth * 0.5)) - 1,
                        (row * cellHeight - (0.4 * cellHeight)),
                        cellWidth,
                        cellHeight,
                    ],
                    math.pi,
                    3 * math.pi / 2,
                    5,
                )

            # 6 : bottom right corner (blue)
            elif Maze[row][col] == 6:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth - (cellWidth * 0.4)) - 2,
                        (row * cellHeight - (0.4 * cellHeight)) - 2,
                        cellWidth,
                        cellHeight,
                    ],
                    3 * math.pi / 2,
                    2 * math.pi,
                    1,
                )

            # 16 : bottom right corner (blue and thicker)
            elif Maze[row][col] == 16:
                pygame.draw.arc(
                    window,
                    maze_color,
                    [
                        (col * cellWidth - (cellWidth * 0.4)),
                        (row * cellHeight - (0.4 * cellHeight)),
                        cellWidth,
                        cellHeight,
                    ],
                    3 * math.pi / 2,
                    2 * math.pi,
                    5,
                )

            # 8 : Drawing white small dots
            elif Maze[row][col] == 8:
                pygame.draw.circle(
                    window,
                    dot_color,
                    (
                        col * cellWidth + (0.5 * cellWidth),
                        row * cellHeight + (0.5 * cellHeight),
                    ),
                    4,
                )

            # 9 : Drawing power ups dots
            elif Maze[row][col] == 9:
                pygame.draw.circle(
                    window,
                    dot_color,
                    (
                        col * cellWidth + (0.5 * cellWidth),
                        row * cellHeight + (0.5 * cellHeight),
                    ),
                    10,
                )
