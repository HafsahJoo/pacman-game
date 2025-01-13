from dataclasses import dataclass


@dataclass
class Position:
    """
    A class to store the basic information about each sprite's position.

    ---

    Attributes:
    ---
    xPos: int

    -
    X Position of sprite

    yPos: int

    -
    Y position of sprite

    angle: int

    -
    Angle of sprite, determining the face it is facing

    Methods:
    ---
    get_tuple() -> tuple

    -
    Return pacman's position as a tuple
    """

    xPos: int
    yPos: int
    angle: int

    def get_tuple(self) -> tuple:
        return self.xPos, self.yPos
