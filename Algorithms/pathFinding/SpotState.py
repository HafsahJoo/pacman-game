from enum import Enum


class SpotState(Enum):
    """
    Enum class for each Spot's state in the A* algorithm
    """

    OPEN = 1
    CLOSE = 2
    BARRIER = 3
    START = 4
    END = 5
