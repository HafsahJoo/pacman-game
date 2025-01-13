import numpy

from Algorithms.astar import start_pathfinding
from datatypes.GameCharacters.GhostMetadata import GhostMetaData, GhostState
from datatypes.GameCharacters.Position import Position
from inputHandling.event import EventDispatcher
from spriteLogic.Ghost.ghost import Ghost


class PathFinding_Ghost(Ghost):
    def __init__(
        self,
        Event: EventDispatcher,
        ghostChoice: list[str],
        frightenedChoice: list[str],
    ) -> None:
        self.spawnLocation = (462, 462)
        super().__init__(
            ghostMetaData=GhostMetaData(
                state=GhostState.FREE,
                CharacterChoice=ghostChoice,
                FrightenedChoice=frightenedChoice,
                spawnPosition=Position(self.spawnLocation[0], self.spawnLocation[1], 0),
                spawnTime=0,
                type="Blinky",
            ),
            Event=Event,
        )

        # Spots for ghost(start) and pacman(end)
        self.start = self.grid[(462 // 25)][475 // 25]
        self.end = self.grid[462 // 25][375 // 25]

        if cellPath := start_pathfinding(self.start, self.end, self.grid):
            currentCell = cellPath[-1]
            nextCell = cellPath[-2]
            if currentCell[0] < nextCell[0]:
                self.angle = 0
            elif currentCell[0] > nextCell[0]:
                self.angle = 180
            elif currentCell[1] < nextCell[1]:
                self.angle = -90
            elif currentCell[1] > nextCell[1]:
                self.angle = 90

    def spawn(self) -> None:
        """Spawn Blinky."""

        self.rect.center = self.spawnLocation

    def update_async(self) -> None:
        """Update the position of the ghost."""

        super().update_async()

        if self.ghost.state == GhostState.FREE:
            self.start = self.grid[(self.rect.centery // 25)][self.rect.centerx // 25]
            if self.is_cell_center():
                self.find_path()
            else:
                self.continue_motion()
        elif self.ghost.state == GhostState.SPAWNING:
            self.ghost.state = GhostState.FREE
        elif self.ghost.state == GhostState.VULNERABLE:
            self.vulnerable_motion()
        elif self.ghost.state == GhostState.EATEN:
            self.eaten_motion()
        elif self.ghost.state == GhostState.RESPAWNING:
            self.go_into_cage()

    def find_path(self) -> None:
        """Find path to follow pacman."""
        if cellPath := start_pathfinding(self.start, self.end, self.grid):
            try:
                currentCell = cellPath[-1]
                nextCell = cellPath[-2]
            except IndexError:
                pass
            else:
                if currentCell[0] < nextCell[0]:
                    self.rect.left += 2
                    self.angle = 0
                elif currentCell[0] > nextCell[0]:
                    self.rect.left -= 2
                    self.angle = 180
                elif currentCell[1] < nextCell[1]:
                    self.rect.top += 2
                    self.angle = -90
                elif currentCell[1] > nextCell[1]:
                    self.rect.top -= 2
                    self.angle = 90

    def update_pacman_position(self, position: tuple[int, int]) -> None:
        """Update the position of pacman in the ghost object"""

        super().update_pacman_position(position)

        self.grid[self.pacmanPosition[1] // 25][
            numpy.clip(self.pacmanPosition[0] // 25, 0, 29)
        ].make_open()
        end = self.grid[position[1] // 25][numpy.clip(position[0] // 25, 0, 29)]
        end.make_end()
        self.end = end
