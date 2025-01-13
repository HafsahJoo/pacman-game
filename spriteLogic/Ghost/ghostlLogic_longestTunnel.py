import random

from datatypes.GameCharacters.GhostMetadata import GhostMetaData, GhostState
from datatypes.GameCharacters.Position import Position
from inputHandling.event import EventDispatcher
from rendering.maze import Maze
from spriteLogic.Ghost.ghost import Ghost
from utils.MaximumUtils import max_index, second_max_index


class LongestTunnel_Ghost(Ghost):
    def __init__(
        self,
        Event: EventDispatcher,
        ghostChoice: list[str],
        frightenedChoice: list[str],
    ) -> None:
        self.spawnLocation = (325, 388)
        super().__init__(
            ghostMetaData=GhostMetaData(
                state=GhostState.SPAWNING,
                type="Clyde",
                CharacterChoice=ghostChoice,
                FrightenedChoice=frightenedChoice,
                spawnPosition=Position(self.spawnLocation[0], self.spawnLocation[1], 0),
                spawnTime=20,
            ),
            Event=Event,
        )

        # Subscribe the methods to different events
        self.pacmanPosition = (0, 0)

    def update_async(self) -> None:
        """Update the position of the ghost."""

        super().update_async()

        if self.ghost.state == GhostState.SPAWNING:
            self.get_out_of_cage()
            if not self.is_in_cage():
                self.ghost.state = GhostState.FREE
        elif self.ghost.state == GhostState.FREE:
            if self.rect.left > 745:
                self.rect.centerx = -self.rect.width + 5
                return
            elif self.rect.left < -self.rect.width + 5:
                self.rect.centerx = 745

            if self.is_cell_center():
                # Finds the longest tunnel
                self.find_tunnel(self.rect.centerx // 25, self.rect.centery // 25)
            else:
                # Continues motion
                self.continue_motion()
        elif self.ghost.state == GhostState.VULNERABLE:
            self.vulnerable_motion()
        elif self.ghost.state == GhostState.EATEN:
            self.eaten_motion()
        elif self.ghost.state == GhostState.RESPAWNING:
            self.go_into_cage()

    def find_tunnel(self, center_x: int, center_y: int) -> None:
        distances = [0, 0, 0, 0]
        while (
            center_y + distances[0] < 32
            and 6 < Maze[center_y + distances[0]][center_x] < 10
        ):
            distances[0] += 1
        while (
            center_x + distances[1] < 29
            and 6 < Maze[center_y][center_x + distances[1]] < 10
        ):
            distances[1] += 1
        while (
            center_y + distances[0] > 0
            and 6 < Maze[center_y - distances[2]][center_x] < 10
        ):
            distances[2] += 1
        while (
            center_x + distances[1] > 0
            and 6 < Maze[center_y][center_x - distances[3]] < 10
        ):
            distances[3] += 1
        if (
            distances[((self.angle + 90) // 90 + 1) % 4] > 1
            or distances[(self.angle + 90) // 90 - 1] > 1
        ):
            # This means we are in a corner and we can turn

            # Randomizes between the longest or the second-longest tunnel
            random_number = random.randint(1, 4)
            distances_indexed = [(i, v) for i, v in enumerate(distances)]
            if random_number == 1:
                direction_index = max_index(distances_indexed)
            else:
                direction_index = second_max_index(distances_indexed)
            self.angle = direction_index * 90 - 90
            self.continue_motion()
        else:
            self.continue_motion()
