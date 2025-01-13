import threading
from time import sleep

import pygame

from datatypes.GameCharacters.Position import Position


class PacmanInputHandler:
    """
    A class that manages the input from the keyboard and moves Pacman

    ---

    Attributes:
    ----------

    nextPosition : Position

    -
    Pacman next position

    mask : pygame. mask

    -
    Mask for Pacman

    mazeMask : pygame. mask

    -
    Maze's mask

    Methods:
    -------
    handle_input() -> None:

    -
    Uses the list of pressed keys and moves Pacman

    is_valid_move() -> bool:

    -
    Uses Maze's mask and Pacman's mask to determine if the next moves would cause a collision

    continue_motion() -> None:

    -
    Moves pacman in the same direction if no key is pressed
    """

    def __init__(self, position: Position, mazeMask: pygame.mask, mask: pygame.mask):
        # Creating an object for pacman's movement data
        self.nextPosition = position

        # Mask for pacman
        self.mask = mask

        # Mask for the maze
        self.mazeMask = mazeMask

        self.input_direction = None

    def handle_input(
        self, keys, position: Position, pacmanWidth: int, pacmanHeight: int, callback
    ) -> None:
        """
        Uses the list of pressed keys and moves Pacman

        ---

        Parameters
        ----------
        keys : ScancodeWrapper
            A dictionary for all the keys and if they are pressed
        position : Position
            The current position of Pacman
        pacmanWidth : int
            Width of pacman
        pacmanHeight : int
            Height of pacman
        callback() -> None:
            Function that is called to change the position of pacman
        """

        # Teleports pacman if out of bounds
        if position.xPos > 745:
            self.nextPosition.xPos = -pacmanWidth + 5
            callback(self.nextPosition)
            return
        elif position.xPos < -pacmanWidth + 5:
            self.nextPosition.xPos = 745
            callback(self.nextPosition)
            return

        if keys[pygame.K_UP]:
            self.input_direction = "up"
            threading.Thread(target=self.revert_input_state).start()
        elif keys[pygame.K_DOWN]:
            self.input_direction = "down"
            threading.Thread(target=self.revert_input_state).start()
        elif keys[pygame.K_RIGHT]:
            self.input_direction = "right"
            threading.Thread(target=self.revert_input_state).start()
        elif keys[pygame.K_LEFT]:
            self.input_direction = "left"
            threading.Thread(target=self.revert_input_state).start()

        # Check the arrow keys for movement and changes the x coordinates, the y coordinates
        # and the angle of pacman respectively
        if self.input_direction == "up":
            self.nextPosition.xPos = position.xPos
            self.nextPosition.yPos = position.yPos - 2
            self.nextPosition.angle = 90
            if self.is_valid_move(pacmanWidth, pacmanHeight):
                callback(self.nextPosition)
            else:
                self.continue_motion(position)
                if self.is_valid_move(pacmanWidth, pacmanHeight):
                    callback(self.nextPosition)
        elif self.input_direction == "down":
            self.nextPosition.xPos = position.xPos
            self.nextPosition.yPos = position.yPos + 2
            self.nextPosition.angle = -90
            if self.is_valid_move(pacmanWidth, pacmanHeight):
                callback(self.nextPosition)
            else:
                self.continue_motion(position)
                if self.is_valid_move(pacmanWidth, pacmanHeight):
                    callback(self.nextPosition)
        elif self.input_direction == "right":
            self.nextPosition.xPos = position.xPos + 2
            self.nextPosition.yPos = position.yPos
            self.nextPosition.angle = 0
            if self.is_valid_move(pacmanWidth, pacmanHeight):
                callback(self.nextPosition)
            else:
                self.continue_motion(position)
                if self.is_valid_move(pacmanWidth, pacmanHeight):
                    callback(self.nextPosition)
        elif self.input_direction == "left":
            self.nextPosition.xPos = position.xPos - 2
            self.nextPosition.yPos = position.yPos
            self.nextPosition.angle = 180
            if self.is_valid_move(pacmanWidth, pacmanHeight):
                callback(self.nextPosition)
            else:
                self.continue_motion(position)
                if self.is_valid_move(pacmanWidth, pacmanHeight):
                    callback(self.nextPosition)
        else:
            # No arrow key is being pressed, continue moving in the current direction
            self.continue_motion(position)
            if self.is_valid_move(pacmanWidth, pacmanHeight):
                callback(self.nextPosition)

    def revert_input_state(self):
        """A buffer for pacman's movement"""
        sleep(0.9)
        self.input_direction = None

    def is_valid_move(self, pacmanWidth: int, pacmanHeight: int) -> bool:
        """
        Uses Maze's mask and Pacman's mask to determine if the next moves would cause a collision

        ---

        Parameters
        ----------
        pacmanWidth : int
            Width of pacman
        pacmanHeight : int
            Height of pacman
        """

        return not self.mazeMask.overlap(
            self.mask,
            (
                self.nextPosition.xPos - (48 - pacmanWidth) // 2,
                self.nextPosition.yPos - (48 - pacmanHeight) // 2,
            ),
        )

    def continue_motion(self, position: Position) -> None:
        """
        Moves pacman in the same direction if no key is pressed

        ---

        Parameters
        ----------
        position: Position
            The current position of pacman
        """

        if position.angle == 90:
            self.nextPosition.xPos = position.xPos
            self.nextPosition.yPos = position.yPos - 2
            self.nextPosition.angle = 90
        elif position.angle == -90:
            self.nextPosition.xPos = position.xPos
            self.nextPosition.yPos = position.yPos + 2
            self.nextPosition.angle = -90
        elif position.angle == 0:
            self.nextPosition.xPos = position.xPos + 2
            self.nextPosition.yPos = position.yPos
            self.nextPosition.angle = 0
        elif position.angle == 180:
            self.nextPosition.xPos = position.xPos - 2
            self.nextPosition.yPos = position.yPos
            self.nextPosition.angle = 180
