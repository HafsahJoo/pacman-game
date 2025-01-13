import random
import sys

import pygame

sys.path.append(r"../PACMAN")
from pygame.locals import *

pygame.init()

window_width = 750
window_height = 875

window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

background = pygame.transform.scale(
    pygame.image.load(r"./assets/minigame/background-night.png"), (875, 1000)
)
base = pygame.transform.scale(
    pygame.image.load(r"./assets/minigame/base.png"), (850, 100)
)


# Load character images
character = {}
character["player"] = (
    pygame.transform.scale(
        pygame.image.load(r"./assets/minigame/spb1.png").convert_alpha(),
        (50, 50),
    ),
    pygame.transform.scale(
        pygame.image.load(r"./assets/minigame/spb2.png").convert_alpha(),
        (50, 50),
    ),
    pygame.transform.scale(
        pygame.image.load(r"./assets/minigame/spb3.png").convert_alpha(),
        (50, 50),
    ),
)
character["pipe"] = (
    pygame.transform.rotate(
        pygame.image.load(r"./assets/minigame/pipe-green.png").convert_alpha(),
        180,
    ),
    pygame.image.load(r"./assets/minigame/pipe-red.png").convert_alpha(),
)


class Pacman:
    def __init__(
        self,
        x: int,
        y: int,
        flap_acceleration: int,
        max_velocity: int,
        acceleration: float,
    ) -> None:
        """
        Represents the Pacman character.

        Parameters
        ----------

        x : int

        -
        The initial x-coordinate of the Pacman.

        y : int

        -
        The initial y-coordinate of the Pacman.

        flap_acceleration : int

        -
        The acceleration when the space bar is pressed.

        max_velocity : int

        -
        The maximum velocity of the Pacman.

        acceleration : float

        -
        The acceleration of the Pacman.

        """
        self.x = x
        self.y = y
        self.velocity = 0
        self.flap_acceleration = flap_acceleration
        self.max_velocity = max_velocity
        self.acceleration = acceleration
        self.flapped = False

    def flap(self) -> None:
        """Flaps the wings of the Pacman, moving it up."""
        self.velocity = self.flap_acceleration
        self.flapped = True

    def update(self) -> None:
        """Updates the position of the Pacman based on its velocity and acceleration."""
        if self.flapped:
            self.y += self.velocity
            self.flapped = False
        else:
            if self.velocity < self.max_velocity:
                self.velocity += self.acceleration
            self.y += self.velocity


class Pipe:
    def __init__(self, x, y, gap_size) -> None:
        """
        Represents a pipe obstacle.

        Parameters
        ----------

        x : int

        -
        The x-coordinate of the pipe.

        y : int

        -
        The y-coordinate of the pipe.

        gap_size : int

        -
        The size of the gap between the upper and lower pipes.

        """
        self.x = x
        self.y = y
        self.gap_size = gap_size
        self.image_upper = character["pipe"][0]
        self.image_lower = character["pipe"][1]
        self.passed = False

    def update(self, speed) -> None:
        """Updates the position of the pipe based on the speed."""
        self.x -= speed

    def collides_with(self, pacman) -> None:
        """
        Checks if the Pacman collides with the pipe.

        Parameters
        ----------

        pacman : Pacman

        -
        The Pacman object.

        Returns
        -------

        bool

        -
        True if collision occurs, False otherwise.

        """
        if (
            pacman.y < self.y
            and pacman.x + character["player"][0].get_width() > self.x
            and pacman.x < self.x + self.image_upper.get_width()
        ):
            return True

        if (
            pacman.y + character["player"][0].get_height() > self.y + self.gap_size
            and pacman.x + character["player"][0].get_width() > self.x
            and pacman.x < self.x + self.image_lower.get_width()
        ):
            return True

        return False

    @staticmethod
    def create_pipe() -> None:
        """Create a new pipe with random properties and return a new Pipe object."""
        pipe_gap_min = 150
        pipe_gap_max = 250
        pipe_gap = random.randint(pipe_gap_min, pipe_gap_max)
        pipe_x = window_width
        pipe_y = random.randint(200, 500)
        pipe = Pipe(pipe_x, pipe_y, pipe_gap)
        return pipe

    @staticmethod
    def draw_pipes(pipes) -> None:
        """Draw the pipes on the game window."""
        for pipe in pipes:
            window.blit(
                pipe.image_upper, (pipe.x, pipe.y - pipe.image_upper.get_height())
            )
            window.blit(pipe.image_lower, (pipe.x, pipe.y + pipe.gap_size))

    @staticmethod
    def move_pipes(pipes, speed: int) -> None:
        """Move the pipes towards the left based on the given speed."""
        for pipe in pipes:
            pipe.update(speed)


def main() -> None:
    """Run the game"""
    pipes = []
    score = 0
    game_over = False
    game_started = False

    background_speed = 5
    xpos_base = 0

    # Pacman settings
    index = 0
    pacman_highest_velocity = 10
    acceleration = 0.5
    spacebar_accn = -7

    pacman = Pacman(150, 200, spacebar_accn, pacman_highest_velocity, acceleration)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if not game_started and event.type == KEYDOWN and event.key == K_SPACE:
                game_started = True
            if game_started and event.type == KEYDOWN and event.key == K_SPACE:
                pacman.flap()
            if game_over and event.type == KEYDOWN and event.key == K_SPACE:
                return

        if not game_started:
            window.blit(background, (0, 0))
            # Start screen
            font = pygame.font.Font(None, 72)
            text = font.render("Click SPACE to start", True, (255, 255, 255))
            text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
            text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
            window.blit(text, text_rect)
        elif not game_over:
            window.blit(background, (0, 0))
            # Check if a new pipe should be added
            if len(pipes) == 0 or pipes[-1].x < window_width - 300:
                pipes.append(Pipe.create_pipe())

            pacman.update()

            # Update and draw the pipes
            Pipe.draw_pipes(pipes)
            Pipe.move_pipes(pipes, background_speed)

            # Check collision with pipes and game over conditions
            for pipe in pipes:
                if (
                    pipe.collides_with(pacman)
                    or pacman.y < 0
                    or pacman.y + character["player"][0].get_height()
                    > window_height - base.get_height()
                ):
                    game_over = True

                if not pipe.passed and pipe.x + pipe.image_upper.get_width() < pacman.x:
                    pipe.passed = True
                    score += 1

            window.blit(character["player"][int(index)], (pacman.x, pacman.y))

            # Update the x position of the base
            xpos_base -= background_speed

            # Reset the x position of the base if it goes off the screen
            if xpos_base < -40:
                xpos_base = 0

            # Update the index for pacman animation
            index += 0.1
            if index > 2:
                index = 0

            window.blit(base, (xpos_base, window_height - base.get_height()))

            # Display the score
            font = pygame.font.Font(None, 36)
            text = font.render("Score: " + str(score), True, (255, 255, 255))
            window.blit(text, (10, 10))
        else:
            window.blit(background, (0, 0))
            font = pygame.font.Font(None, 60)
            game_over_text = font.render("Game Over", True, "Black")
            score_text = font.render(f"Score: {score}", True, "Black")
            menu_text = font.render("Press space to go to main menu", True, "Black")

            text_rect_game_over = game_over_text.get_rect(
                center=(window_width // 2, window_height // 2 - 50)
            )
            text_rect_score = score_text.get_rect(
                center=(window_width // 2, window_height // 2 + 50)
            )
            text_rect_menu = menu_text.get_rect(
                center=(window_width // 2, window_height // 2 + 150)
            )

            window.blit(game_over_text, text_rect_game_over)
            window.blit(score_text, text_rect_score)
            window.blit(menu_text, text_rect_menu)

        pygame.display.update()
        clock.tick(60)
