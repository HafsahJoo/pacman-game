from dataclasses import dataclass
from enum import Enum

from datatypes.GameCharacters.Position import Position


class GhostState(Enum):
    """
    An enum class for the ghost's different states.

    ---
    """

    WAITING = 1
    SPAWNING = 2
    FREE = 3
    VULNERABLE = 4
    EATEN = 5
    RESPAWNING = 6


@dataclass
class GhostMetaData:
    """
    A class to store the metadata of the ghost

    ---
    Attributes:
    ---
    state: GhostState

    - The state of the ghost. I.e: Free, Spawning, Vulnerable...

    type: str

    - Type of ghost

    spawnPosition: Position

    - Position where ghost should spawn

    spawnTime: int

    - Seconds until ghost goes out of cage

    CharacterChoice: list

    - Skins of ghosts

    FrightenedChoice: list

    - Frightened skins of ghosts
    """

    # The state of the ghost. I.e: Free, Spawning, Vulnerable...
    state: GhostState
    # Type of ghost
    type: str
    # Position where ghost should spawn
    spawnPosition: Position
    # Seconds until ghost goes out of cage
    spawnTime: int
    # Skins of ghosts
    CharacterChoice: list = None
    # Frightened skins of ghosts
    FrightenedChoice: list = None
