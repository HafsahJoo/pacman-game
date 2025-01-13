from dataclasses import dataclass


@dataclass
class PacmanMetaData:
    """
    A class to store the lives and the frames of pacman.

    ---

    Attributes
    ---
    lives: int

    -
    Pacman's lives

    CharacterChoice: list

    -
    Pacman's frames
    """

    lives: int
    CharacterChoice: list = None
