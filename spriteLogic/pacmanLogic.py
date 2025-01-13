#!/bin/python3
import pygame

from datatypes.GameCharacters import CharacterChoice
from datatypes.GameCharacters.PacmanMetadata import PacmanMetaData
from datatypes.GameCharacters.Position import Position
from inputHandling.event import EventDispatcher
from inputHandling.pacmanInputHandler import PacmanInputHandler
from rendering.maze import mazeMask

pygame.init()

pacmanPosition = 50, 50


class Pacman(pygame.sprite.Sprite):
    """
    A class to represent the features and functionalities of pacman.

    ---
    Attributes:
    ---
    pacman: PacmanMetaData
    - A pacman class which contains data about the state, type and skins of the ghost.

    event: EventDispatcher
    - An event class to subscribe methods to certain events and emit events

    angle: int
    - Indicates the direction in which pacman is moving

    stateIndex: int
    - Indicates the frame which is being displayed during pacman's animation

    mazeMask: mazeMask
    - The mask for the maze

    mask: pygame.mask.Mask
    - The mask for pacman

    image: pygame.image.load
    - The current image loaded for pacman

    spawnLocation: tuple[int,int]
    - This is the spawn location of the pacman.

    rect: pygame.rect
    - This is the rectangle for the pacman image

    Methods:
    ---
    spawn() -> None:
    - Spawn pacman at its spawn location

    set_position(*args) -> None:
    - Responsible for updating the location of pacman.

    change_lives(*args) -> None:
    - Responsible for updating the remaining lives of pacman

    pacman_input() -> None:
    - Dictates the movement of pacman according to player input

    change_position(*args) -> None:
    - Change the position of pacman according to player input

    update() -> None:
    - Calls the respective methods to animate and move pacman and also emits some events

    animation_state() -> None:
    - Animates pacman
    """

    def __init__(self, Event: EventDispatcher, pacmanChoice: list) -> None:
        super().__init__()

        # Creating an event class for pacman
        self.event = Event

        self.event.enroll("update_lives", self.change_lives)
        self.event.enroll("entities_spawn", self.set_position)
        self.event.enroll("spawn_entities", self.spawn)

        # Creating a class pacman Data Class
        self.pacman = PacmanMetaData(lives=3, CharacterChoice=pacmanChoice)

        # Loading the pacman sprites
        for index, frame in enumerate(self.pacman.CharacterChoice):
            self.pacman.CharacterChoice[index] = pygame.image.load(
                frame
            ).convert_alpha()

        self.angle = -1
        self.stateIndex = 0

        # Pacman's current frame
        self.image = self.pacman.CharacterChoice[self.stateIndex]

        # Spawn location of pacman
        self.spawnLocation = (113, 388)

        # Getting pacman's position and its initial spawn location
        self.rect = self.image.get_rect()
        self.rect.center = self.spawnLocation

        self.pacmanInputHandler = PacmanInputHandler(
            position=Position(self.rect.left, self.rect.top, self.angle),
            mazeMask=mazeMask,
            mask=pygame.mask.Mask((48, 48), fill=True),
        )

    def spawn(self) -> None:
        """
        Spawn pacman in its spawn location.

        ---
        Parameters:
        ---
        None

        Returns:
        ---
        None
        """

        self.angle = 0
        self.rect.center = self.spawnLocation

    def set_position(self, position: list) -> None:
        """Update the location of pacman after certain events."""

        self.rect.center = position[0].get_tuple()
        self.angle = position[0].angle

    def change_lives(self, lives: int) -> None:
        """Update the lives of pacman."""

        self.pacman.lives = lives

    def pacman_input(self) -> None:
        """Move pacman according to player input."""

        keys = pygame.key.get_pressed()

        self.pacmanInputHandler.handle_input(
            keys=keys,
            position=Position(self.rect.left, self.rect.top, self.angle),
            callback=self.change_position,
            pacmanWidth=self.rect.width,
            pacmanHeight=self.rect.height,
        )

    def change_position(self, position: Position) -> None:
        """Change the position of pacman."""

        self.rect.topleft = position.get_tuple()
        self.angle = position.angle

    def update(self) -> None:
        """Update the pacman animations."""

        self.pacman_input()
        self.animation_state()
        self.event.associate("pacman_position", self.rect.center)
        self.event.associate("get_lives", self.pacman.lives)

    def animation_state(self) -> None:
        """Responsible for changing pacman animation state."""

        self.stateIndex += 0.1
        # Change between pacman's frames
        if self.stateIndex >= len(self.pacman.CharacterChoice):
            self.stateIndex = 0
        self.image = self.pacman.CharacterChoice[int(self.stateIndex)]

        # Checks if pacman is going to the left
        if self.angle == 180:
            self.image = pygame.transform.flip(self.image, False, True)

        # Rotate pacman 90 degrees up or down
        self.image = pygame.transform.rotate(self.image, self.angle)

        # Updates the collision box of Pacman
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
