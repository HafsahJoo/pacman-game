import random
import sys
import threading
import time

import numpy

sys.path.append(r"../PACMAN")
from Algorithms.astar import make_grid, start_pathfinding
from datatypes.GameCharacters import CharacterChoice
from datatypes.GameCharacters.GhostMetadata import GhostMetaData, GhostState
from datatypes.GameCharacters.Position import Position
from inputHandling.event import EventDispatcher
from rendering.maze import Maze
from spriteLogic.Ghost.ghost import Ghost


class Scatter_Ghost(Ghost):
    def __init__(
        self,
        Event: EventDispatcher,
        ghostChoice: list[str],
        frightenedChoice: list[str],
    ) -> None:
        self.spawnLocation = (370, 388)
        super().__init__(
            ghostMetaData=GhostMetaData(
                state=GhostState.WAITING,
                CharacterChoice=ghostChoice,
                FrightenedChoice=frightenedChoice,
                spawnPosition=Position(self.spawnLocation[0], self.spawnLocation[1], 0),
                spawnTime=8,
                type="Pinky",
            ),
            Event=Event,
        )

        self.event.enroll("kill_process", self.end_thread)

        # Boolean that keeps the change_direction loop running
        self.__run_thread = True

        # State that decides whether ghost need to scatter or not
        # It is the randomized evey 5 seconds through a thread
        self.scatterState = False
        threading.Thread(target=self.change_state).start()

        # Create grid for pathfinding
        self.grid = make_grid(Maze)
        for row in self.grid:
            for spot in row:
                spot.update_neighbors(self.grid)

        # Spots for ghost(start) and pacman(end)
        self.start = self.grid[(self.spawnLocation[1] // 25)][
            self.spawnLocation[0] // 25
        ]
        self.end = self.grid[462 // 25][375 // 25]

        self.corner_pos = (2, 2)

        # Defines an initial path for the ghost
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

    def end_thread(self):
        """Kill the threads"""
        self.__run_thread = False

    def update_async(self) -> None:
        """Update the position of the ghost."""

        super().update_async()

        # Checks if ghost is spawning
        if self.ghost.state == GhostState.SPAWNING:
            self.get_out_of_cage()
            if not self.is_in_cage():
                # Sets the state of the ghost to free
                self.ghost.state = GhostState.FREE
        elif self.ghost.state == GhostState.FREE:
            self.start = self.grid[(self.rect.centery // 25)][self.rect.centerx // 25]
            if self.is_cell_center():
                # Alternate between running away and finding path
                if self.scatterState:
                    self.run_away()
                else:
                    self.find_path()
            else:
                self.continue_motion()
        elif self.ghost.state == GhostState.VULNERABLE:
            self.vulnerable_motion()
        elif self.ghost.state == GhostState.EATEN:
            self.eaten_motion()
        elif self.ghost.state == GhostState.RESPAWNING:
            self.go_into_cage()

    def find_path(self) -> None:
        """Find the path that leads to pacman."""
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

    def run_away(self) -> None:
        """Tries to run away from pacman"""

        if cellPath := start_pathfinding(
            self.start,
            self.find_furthest_corner(),
            self.grid,
        ):
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

    def find_furthest_corner(self) -> None:
        """Finds the further corne away from pacman."""

        if self.rect.centery // 25 < 4:
            self.corner_pos = (self.corner_pos[0], 30)
        elif self.rect.centery // 25 > 28:
            self.corner_pos = (self.corner_pos[0], 2)
        if self.rect.centerx // 25 < 4:
            self.corner_pos = (26, self.corner_pos[1])
        elif self.rect.centerx // 25 > 28:
            self.corner_pos = (2, self.corner_pos[1])

        return self.grid[self.corner_pos[1]][self.corner_pos[0]]

    def update_pacman_position(self, position: tuple[int, int]) -> None:
        """Update the position of pacman in the ghost object"""

        super().update_pacman_position(position)

        self.grid[self.pacmanPosition[1] // 25][
            numpy.clip(self.pacmanPosition[0] // 25, 0, 29)
        ].make_open()
        end = self.grid[position[1] // 25][numpy.clip(position[0] // 25, 0, 29)]
        end.make_end()
        self.end = end

    def change_state(self) -> None:
        """Change the path logic of the ghost"""

        while self.__run_thread:
            time.sleep(15)
            self.scatterState = bool(random.getrandbits(1))
