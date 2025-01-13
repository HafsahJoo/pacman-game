import sys

import numpy
import pygame

sys.path.append(r"../PACMAN")
from inputHandling.event import EventDispatcher
from rendering.maze import Maze, cellHeight, cellWidth


class MazeLogic:
    """
    A class that contains all the methods to update the maze's functions

    ---

    Attributes:
    ---
    event: EventDispatcher

    -
    An event class to emit events and subscribe functions to events

    score: int

    -
    Score of pacman

    dots: int

    -
    Number of small white dots pacman has eaten

    pacmanPosition: tuple[int, int]

    -
    Position of pacman

    lives: int

    -
    Number of lives remaining for pacman

    font: pygame.font.Font

    -
    Font used for displaying scores.

    Methods:
    ---
    eats_dots(*args) -> None:

    -
    Updates the score of pacman .

    get_lives(*args) -> None:

    -
    Get the lives of pacman.

    spawn() -> None:

    -
    Spawn the entities at their original positon.

    display_score(*args) -> None:

    -
    Display the score of pacman.

    pacman_dies() -> None:

    -
    Remove a life from pacman and updates the game accordingly.

    update(*args) -> None:

    -
    Update the maze functions and processes by calling the respective methods.
    """

    def __init__(self, Event: EventDispatcher) -> None:
        # Setting up the listeners for each event
        self.event = Event
        self.event.enroll("pacman_position", self.eats_dots)
        self.event.enroll("pacman_dies", self.pacman_dies)
        self.event.enroll("get_lives", self.get_lives)
        self.event.enroll("score_update", self.display_score)
        self.event.enroll("pacman_eats_ghost", self.update_score)

        # Keeps track of the score and the number of dots pacman has eaten
        self.score = 0
        self.dots = 0

        # Hold's the position of pacman
        self.pacmanPosition = 0, 0

        # Count the number of remaining lives for pacman
        self.lives = 3

        # The font used to display the score counter
        self.font = pygame.font.Font(r"./assets/fonts/subway-ticker/SUBWT___.ttf", 32)

    def update_score(self) -> None:
        """Updates score when pacman eats a ghost"""

        pygame.mixer.music.load("./assets/sound/pacman_eatghost.wav")
        pygame.mixer.music.play()
        self.score += 500

    def eats_dots(self, pacmanPosition: tuple[int, int]) -> None:
        """
        Updates the score of pacman and emits events such as level completed or  pacman has powered up.

        ---
        Parameters:
        ---
        pacmanPosition: tuple[int, int]

        -
        It gives the current position of pacman

        Returns:
        ---
        None
        """

        # Checks the cell pacman is in
        nextCell = (
            numpy.clip(pacmanPosition[0] // cellWidth, 0, 28),
            numpy.clip(pacmanPosition[1] // cellHeight, 0, 31),
        )

        # Checks if pacman eats a white small dot
        if Maze[nextCell[1]][nextCell[0]] == 8:
            if self.dots == 241:
                self.score += 10
                # play sound
                pygame.mixer.music.load("./assets/sound/pacman_extrapac.wav")
                pygame.mixer.music.play()
                self.event.associate("level_completed")
            else:
                self.score += 10
                self.dots += 1
                # play sound
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load("./assets/sound/pacman_chomp.wav")
                    pygame.mixer.music.play()

            Maze[nextCell[1]][nextCell[0]] = 7

        # Checks if pacman eats a power up dot
        elif Maze[nextCell[1]][nextCell[0]] == 9:
            self.score += 50
            self.event.associate("Pacman_powerup")
            Maze[nextCell[1]][nextCell[0]] = 7

        # Stores the position of pacman
        self.pacmanPosition = pacmanPosition

    def get_lives(self, lives: int) -> None:
        """
        Get the current remaining lives of pacman.

        ---
        Parameters:
        ---
        lives: int

        -
        Contains the remaining lives of pacman.

        Returns:
        ---
        None
        """

        self.lives = lives

    def spawn(self) -> None:
        """
        Emits an event to indicate that the sprites should be spawned in the maze.

        ---
        Parameters:
        ---
        None

        Returns:
        ---
        None
        """

        # Spawn event to place entities at their spawn location
        self.event.associate("spawn_entities")

    def display_score(self) -> None:
        """
        Emits an event to update the score of pacman

        ---
        Parameters:
        ---
        None

        Returns:
        ---
        None
        """

        self.event.associate("display_score", self.score)

    def pacman_dies(self) -> None:
        """
        Remove a life from pacman and checks if the game is over.

        ---

        Parameters:
        ---
        None

        Returns:
        ---
        None
        """

        # Remove a life from pacman
        self.lives -= 1
        pygame.mixer.music.load("./assets/sound/pacman_death.wav")
        pygame.mixer.music.play()
        if self.lives != 0:
            self.spawn()
            # Update event to change the lives of pacman
            self.event.associate("update_lives", self.lives)
        else:
            self.event.associate("game_over")

    def update(self, screen: pygame.Surface) -> None:
        """
        Call the respective methods to update and display the score and remaining lives of pacman.

        ---
        Parameters:
        ---
        screen: pygame.Surface

        -
        This is the main screen that is being drawn

        Returns:
        ---
        None
        """

        # Display pacman's score
        self.display_score()

        for i in range(0, self.lives):
            screen.blit(
                pygame.image.load(r"./assets/sprite/pacman_lives_icon.png"),
                (700 - (i * 40), 831),
            )
