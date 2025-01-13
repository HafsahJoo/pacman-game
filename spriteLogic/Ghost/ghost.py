import threading
from time import sleep

import pygame

from Algorithms.astar import make_grid, start_pathfinding
from datatypes.GameCharacters import CharacterChoice
from datatypes.GameCharacters.GhostMetadata import GhostMetaData, GhostState
from datatypes.GameCharacters.Position import Position
from inputHandling.event import EventDispatcher
from rendering.maze import Maze, mazeMask


class Ghost(pygame.sprite.Sprite):
    """
    A class to represent the basic features and functionalities of each ghosts.

    ---
    Attributes:
    ---
    ghost: GhostMetaData
    - A ghost class which contains data about the state, type and skins of the ghost.

    event: EventDispatcher
    - An event class to subscribe methods to certain events and emit events

    angle: int
    - Indicates the direction in which the ghost is moving

    stateIndex: int
    - Indicates the frame which is being displayed during the ghost's animation

    mazeMask: mazeMask
    - The mask for the maze

    mask: pygame.mask.Mask
    - The mask for the ghost

    image: pygame.image.load
    - The current image loaded for the ghost

    spawnLocation: tuple[int,int]
    - This is the spawn location of the ghost.

    rect: pygame.rect
    - This is the rectangle for the ghost image
    rect: pygame.rect()

    -
    This is the rectangle for the ghost image

    eaten: bool

    -
    This is to check if pacman has been eaten or not

    Methods:
    ---
    revert_state(*args) -> None:
    - Return the ghost to their normal state.

    frighten_state() -> None:
    - Responsible for the behavior of the ghosts during its frightened state

    spawn() -> None:
    - Responsible for spawning the ghosts.

    update() -> None:
    - Calls the animation method

    animation_state() -> None:
    - It animates pacman.
    """

    def __init__(self, ghostMetaData: GhostMetaData, Event: EventDispatcher) -> None:
        super().__init__()

        # Creating a class ghost
        self.ghost = ghostMetaData

        # Setting up an event handler
        self.event = Event
        self.event.enroll("Pacman_powerup", self.change_to_vulnerable_state)
        self.event.enroll("pacman_position", self.update_pacman_position)
        self.event.enroll("spawn_entities", self.spawn)

        # Loading the ghost sprites
        for index, frame in enumerate(self.ghost.CharacterChoice):
            self.ghost.CharacterChoice[index] = pygame.image.load(frame).convert_alpha()

        self.angle = 0
        self.stateIndex = 0

        self.mazeMask = mazeMask
        self.mask = pygame.mask.Mask((48, 48), fill=True)

        # Ghost's current frame
        self.image = self.ghost.CharacterChoice[self.stateIndex]

        # Getting ghost's position and its initial spawn location
        self.rect = self.image.get_rect()
        self.rect.center = self.ghost.spawnPosition.get_tuple()

        self.pacmanPosition = (0, 0)

        self.grid = make_grid(Maze)
        for row in self.grid:
            for spot in row:
                spot.update_neighbors(self.grid)
        self.current_thread = threading.Thread(target=self.__wait_spawn)

    def revert_state(self, duration: int) -> None:
        """
        Returns the ghost to its normal state.

        ---
        Parameters:
        ---
        duration: int
        - The amount of time the thread should sleep

        Returns:
        ---
        None
        """

        sleep(duration)
        self.place_center()
        if self.ghost.state == GhostState.VULNERABLE:
            self.ghost.state = GhostState.FREE

    def change_to_vulnerable_state(self) -> None:
        """
        Puts the ghosts into frightened state

        ---
        Parameters:
        ---
        None

        Returns:
        ---
        None
        """

        if self.ghost.state == GhostState.FREE:
            self.place_center()
            self.ghost.state = GhostState.VULNERABLE

            # TODO increase time remaining if pacman eats a ghost
            threading.Thread(target=self.revert_state, args=(10,)).start()

    def vulnerable_motion(self):
        if (
            abs(self.pacmanPosition[0] - self.rect.centerx) < 25
            and abs(self.pacmanPosition[1] - self.rect.centery) < 25
        ):
            self.ghost.state = GhostState.EATEN
            self.event.associate("pacman_eats_ghost")
            self.place_center()
        else:
            dx = 1 if (self.pacmanPosition[0] - self.rect.centerx) < 0 else -1
            dy = 1 if (self.pacmanPosition[1] - self.rect.centery) < 0 else -1
            if self.is_valid_move(
                Position(self.rect.left, self.rect.top + dy, self.angle)
            ):
                self.rect.centery += dy
            elif self.is_valid_move(
                Position(self.rect.left + dx, self.rect.top, self.angle)
            ):
                self.rect.centerx += dx

    def eaten_motion(self) -> None:
        """The path that each ghost in its eaten ghost follow."""

        start = self.grid[self.rect.centery // 25][self.rect.centerx // 25]
        end = self.grid[312 // 25][350 // 25]
        if (
            cellPath := start_pathfinding(start, end, self.grid)
        ) and self.is_cell_center():
            try:
                currentCell = cellPath[-1]
                nextCell = cellPath[-2]
            except IndexError:
                self.ghost.state = GhostState.RESPAWNING
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
        else:
            self.continue_motion()

    def go_into_cage(self):
        """Makes the ghost goes into the cage"""
        if self.rect.centery < self.ghost.spawnPosition.get_tuple()[1]:
            self.rect.centery += 1
        elif self.rect.centerx > self.ghost.spawnPosition.get_tuple()[0]:
            self.rect.centerx -= 1
        elif self.rect.centerx < self.ghost.spawnPosition.get_tuple()[0]:
            self.rect.centerx += 1
        else:
            self.ghost.state = GhostState.WAITING
            if not self.current_thread.is_alive():
                self.current_thread = threading.Thread(
                    target=self.__wait_spawn, args=(2,)
                )
                self.current_thread.start()

    def place_center(self) -> None:
        """Places the ghost at the center of a cell"""
        self.rect.center = (
            25 * (self.rect.centerx // 25) + 12,
            25 * (self.rect.centery // 25) + 12,
        )

    def check_collision(self) -> None:
        """Checks if pacman has collided with a ghost."""

        if (
            abs(self.rect.centerx - self.pacmanPosition[0]) < 27
            and abs(self.rect.centery - self.pacmanPosition[1]) < 27
            and self.ghost.state == GhostState.FREE
        ):
            self.event.associate("pacman_dies")

    def is_cell_center(self) -> bool:
        """
        Returns whether the ghost is in the center of a cell

        ---
        Parameters:
        ---
        None

        Returns:
        ---
        bool
        """
        return (
            abs(self.rect.centerx - 25 * (self.rect.centerx // 25) - 12.5) < 1
            and abs(self.rect.centery - 25 * (self.rect.centery // 25) - 12.5) < 1
        )

    def spawn(self) -> None:
        """
        Spawn the ghosts.

        ---
        Parameters:
        ---
        None

        Returns:
        ---
        None
        """

        self.ghost.state = GhostState.WAITING
        self.rect.center = self.ghost.spawnPosition.get_tuple()
        self.angle = 0
        if not self.current_thread.is_alive():
            self.current_thread = threading.Thread(
                target=self.__wait_spawn, args=(self.ghost.spawnTime,)
            )
            self.current_thread.start()

    def __wait_spawn(self, spawnTime) -> None:
        """
        It is called in a thread and waits until the time for the ghost to spawn.

        ---
        Parameters:
        ---
        spawnTime: int

        -
        The time that the ghost needs to wait in the cage

        Returns:
        ---
        None
        """
        sleep(spawnTime)
        self.ghost.state = GhostState.SPAWNING
        self.angle = 0

    def get_out_of_cage(self) -> None:
        """
        Makes the ghost move out of the cage.

        ---
        Parameters:
        ---
        None

        Returns:
        ---
        None
        """

        if self.rect.centerx > 375:
            self.rect.centerx -= 1
        elif self.rect.centerx < 375:
            self.rect.centerx += 1
        else:
            self.rect.centery -= 1

    def is_in_cage(self) -> bool:
        """
        Checks if the ghost is out of the cage

        ---
        Parameters:
        ---
        None

        Returns:
        ---
        bool
        """
        return self.rect.centery > 312

    def update(self) -> None:
        """
        Calls update_async method on a thread

        ---
        Parameters:
        ---
        None

        Returns:
        ---
        None
        """
        threading.Thread(target=self.update_async).start()

    def update_async(self):
        """
        Calls the methods that updates the ghost for every frame

        ---
        Parameters:
        ---
        None

        Returns:
        ---
        None
        """
        self.animation_state()
        self.check_collision()

    def continue_motion(self) -> None:
        """Continues the motion of the ghost in the direction it previously was going"""

        if self.angle == 0:
            self.rect.left += 2
        elif self.angle == 180:
            self.rect.left -= 2
        elif self.angle == -90:
            self.rect.top += 2
        elif self.angle == 90:
            self.rect.top -= 2

    def animation_state(self) -> None:
        """
        Responsible for changing the images and animating the ghosts.

        ---
        Parameters:
        ---
        None

        Returns:
        ---
        None
        """

        self.stateIndex += 0.1
        # Checks if the ghost is in its vulnerable state and loads the appropriate frame
        if self.ghost.state == GhostState.VULNERABLE:
            if self.stateIndex >= len(CharacterChoice.FrightenedGhostFrame):
                self.stateIndex = 0
            self.image = pygame.image.load(
                self.ghost.FrightenedChoice[int(self.stateIndex)]
            ).convert_alpha()
        elif (
            self.ghost.state == GhostState.EATEN
            or self.ghost.state == GhostState.RESPAWNING
        ):
            # Loads the eaten frames for the ghosts
            self.image = pygame.image.load(
                CharacterChoice.EatenGhostFrame[0]
            ).convert_alpha()
        else:
            if self.stateIndex >= len(self.ghost.CharacterChoice):
                self.stateIndex = 0
            self.image = self.ghost.CharacterChoice[int(self.stateIndex)]
            if self.angle == 180:
                self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(center=self.rect.center)

    def update_pacman_position(self, position: tuple[int, int]) -> None:
        """Update the position of pacman in the ghost object"""

        self.pacmanPosition = position

    def is_valid_move(self, nextPosition: Position) -> bool:
        """Check if the next move of Pacman is valid or not."""

        return not self.mazeMask.overlap(
            self.mask,
            (
                nextPosition.xPos - (48 - self.rect.width) // 2,
                nextPosition.yPos - (48 - self.rect.height) // 2,
            ),
        )


# Spear ghost finds direction where it will have the longest straight line.
# Siren head will find the shortest path and follow you
# Whip ghost will alternate between scatter and chase
# Portal ghost will move randomly in valid directions
