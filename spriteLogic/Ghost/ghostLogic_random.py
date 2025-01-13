import threading
import time
from random import randint

from datatypes.GameCharacters import CharacterChoice
from datatypes.GameCharacters.GhostMetadata import GhostMetaData, GhostState
from datatypes.GameCharacters.Position import Position
from inputHandling.event import EventDispatcher
from spriteLogic.Ghost.ghost import Ghost


# TODO: Fix random movement and teleport to pacman if red is far
class RandomGhost(Ghost):
    """Create a Ghost class."""

    def __init__(
        self,
        Event: EventDispatcher,
        ghostChoice: list[str],
        frightenedChoice: list[str],
    ) -> None:
        self.spawnLocation = (425, 388)
        super().__init__(
            ghostMetaData=GhostMetaData(
                state=GhostState.SPAWNING,
                CharacterChoice=ghostChoice,
                FrightenedChoice=frightenedChoice,
                spawnPosition=Position(self.spawnLocation[0], self.spawnLocation[1], 0),
                spawnTime=14,
                type="Inky",
            ),
            Event=Event,
        )

        self.event.enroll("kill_process", self.end_thread)

        # Boolean that keeps the change_direction loop running
        self.__run_thread = True

        # Calls a function that finds a random direction on a thread
        threading.Thread(target=self.change_direction_thread).start()

    def end_thread(self):
        """Kills all thread"""
        self.__run_thread = False

    def update_async(self) -> None:
        """Update the position of the ghost."""

        super().update_async()

        if self.ghost.state == GhostState.SPAWNING:
            self.get_out_of_cage()
            if not self.is_in_cage():
                self.ghost.state = GhostState.FREE
        elif self.ghost.state == GhostState.FREE:
            if not self.continue_motion():
                self.continue_motion()
        elif self.ghost.state == GhostState.VULNERABLE:
            self.vulnerable_motion()
        elif self.ghost.state == GhostState.EATEN:
            self.eaten_motion()
        elif self.ghost.state == GhostState.RESPAWNING:
            self.go_into_cage()

    def continue_motion(self) -> bool:
        """Continue the ghost in its current direction."""

        if self.rect.left > 745:
            self.rect.centerx = -self.rect.width + 5
        elif self.rect.left < -self.rect.width + 5:
            self.rect.centerx = 745

        if self.angle == 90 and self.is_valid_move(
            Position(self.rect.left, self.rect.top - 2, self.angle)
        ):
            self.rect.top = self.rect.top - 2
        elif self.angle == -90 and self.is_valid_move(
            Position(self.rect.left, self.rect.top + 2, self.angle)
        ):
            self.rect.top = self.rect.top + 2
        elif self.angle == 0 and self.is_valid_move(
            Position(self.rect.left + 2, self.rect.top, self.angle)
        ):
            self.rect.left = self.rect.left + 2
        elif self.angle == 180 and self.is_valid_move(
            Position(self.rect.left - 2, self.rect.top, self.angle)
        ):
            self.rect.left = self.rect.left - 2
        else:
            self.change_direction()
            return False
        return True

    def change_direction_thread(self) -> None:
        """Change the direction of the movement of the ghost."""

        while self.__run_thread:
            new_positions = []
            if self.is_valid_move(
                Position(self.rect.left, self.rect.top - 2, self.angle)
            ):
                new_positions.append(90)
            if self.is_valid_move(
                Position(self.rect.left + 2, self.rect.top, self.angle)
            ):
                new_positions.append(0)
            if self.is_valid_move(
                Position(self.rect.left, self.rect.top + 2, self.angle)
            ):
                new_positions.append(-90)
            if self.is_valid_move(
                Position(self.rect.left - 2, self.rect.top, self.angle)
            ):
                new_positions.append(180)
            if self.ghost.state == GhostState.FREE:
                self.angle = self.change_direction()
                self.continue_motion()
            time.sleep(1)

    def change_direction(self) -> None:
        """Determine the new direction of the ghost."""

        new_positions = []

        if self.is_valid_move(Position(self.rect.left, self.rect.top - 2, self.angle)):
            new_positions.append(90)
        if self.is_valid_move(Position(self.rect.left + 2, self.rect.top, self.angle)):
            new_positions.append(0)
        if self.is_valid_move(Position(self.rect.left, self.rect.top + 2, self.angle)):
            new_positions.append(-90)
        if self.is_valid_move(Position(self.rect.left - 2, self.rect.top, self.angle)):
            new_positions.append(180)
        return new_positions[randint(0, len(new_positions) - 1)]
