#!/bin/python3
import sys

import pygame

sys.path.append(r"../PACMAN")
from rendering import credentials

pygame.init()

# Window width and height
window_width: int = 750
window_height: int = 875
window = pygame.display.set_mode((window_width, window_height))

font_file: str = "./assets/fonts/Pacman2.ttf"
font_file1: str = "./assets/fonts/PacfontGood-yYye.ttf"

image1 = pygame.transform.scale(
    pygame.image.load("./assets/sprite/pixelpac.png"), (50, 50)
)
image2 = pygame.transform.scale(
    pygame.image.load("./assets/sprite/bg.png"), (800, 1000)
)

font_size: int = 150
font = pygame.font.Font(font_file, font_size)


def title(text: str) -> None:
    """
    Show the main title.

    Parameters
    ----------
    text : str

    -
    The text to be displayed as the main title.

    Returns
    -------
    None
    """
    font = pygame.font.Font(font_file1, 105)

    # Render text using the loaded font
    text_surface = font.render(text, True, (220, 220, 0))
    window.blit(text_surface, (83, 55))


def subtitle(text: str) -> None:
    """
    Show the subtitle.

    Parameters
    ----------
    text : str

    -The text to be displayed as the subtitle.

    Returns
    -------
    None
    """
    font = pygame.font.Font(font_file1, 22)

    # Render text using the loaded font
    text_surface = font.render(text, True, (255, 255, 255))
    window.blit(text_surface, (37, 200))


class Button:
    """
    A class to represent a button.

    ...

    Attributes
    ----------
    xpos : int

    -
    x-coordinate position of the button

    ypos : int

    -
    y-coordinate position of the button

    text : str

    -
    text displayed on the button

    color : tuple

    -
    color of the button when not hovered over

    toggle_color : tuple

    -
    color of the button when hovered over

    Methods
    -------

    animate_button(pos: tuple) -> bool

    -
    Changes the button color when hovering over it.

    update()

    -
    Draws the button on the screen.

    checkinput(pos: tuple) -> None

    -
    Checks if the button is clicked.
    """

    def __init__(self, xpos: int, ypos: int, text: str, color, toggle_color):
        self.xpos = xpos
        self.ypos = ypos
        self.font = pygame.font.Font(font_file1, 90)
        self.color = color
        self.toggle_color = toggle_color
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect(center=(self.xpos, self.ypos))

    def animate_button(self, pos: tuple) -> bool:
        """
        Changes the button color when hovering over it.

        Parameters
        ----------
        pos : tuple

        -
        position of the mouse cursor

        Returns
        -------
        bool

        -
        True if the button is being hovered over, False otherwise
        """
        if self.rect.collidepoint(pos):
            window.blit(image1, (160, 405))
            self.text_surface = self.font.render(self.text, True, self.toggle_color)
            self.rect.center = self.xpos - 3, self.ypos - 7
            return True
        else:
            self.text_surface = self.font.render(self.text, True, self.color)
            self.rect.center = self.xpos, self.ypos

    def update(self) -> None:
        """
        Draws the button on the screen.
        """
        window.blit(self.text_surface, self.rect)

    def checkinput(self, pos: tuple) -> None:
        """
        Checks if the button is clicked.

        Parameters
        ----------
        pos : tuple

        -
        position of the mouse cursor
        """
        if self.rect.collidepoint(pos):
            credentials.main()
            exit()


button0 = Button(355, 440, "play", "blue", (220, 220, 0))
button1 = Button(360, 445, "play", (220, 220, 0), "blue")

# list from A-Z for animation of pacman using characters
character = [chr(65 + j % 26) for j in range(26)]


def main() -> None:
    """
    The main function that runs the game loop.
    """
    running = True
    i = 0
    j = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                button0.checkinput(pygame.mouse.get_pos())

        window.fill("black")

        window.blit(image2, (0, 0))

        # Update and animate the buttons
        button0.update()
        button0.animate_button(pygame.mouse.get_pos())
        button1.update()
        button1.animate_button(pygame.mouse.get_pos())

        # Render and display text surfaces to animate pacman
        text_surface = font.render(character[int(i)], True, "white")
        window.blit(text_surface, (300, 600))
        text_surface1 = font.render(character[int(i)].lower(), True, "yellow")
        window.blit(text_surface1, (100, 600))
        text_surface2 = font.render(str(int(j)), True, "yellow")
        window.blit(text_surface2, (500, 600))

        title("P91-MAN")

        subtitle("A CHOMPING ADVENTURE LIKE NEVER BEFORE!")

        i += 0.08
        j += 0.08

        if i > 25:
            i = 0

        if j > 9:
            j = 0

        pygame.draw.rect(window, (220, 220, 0), (0, 0, 750, 875), 6)
        pygame.draw.rect(window, (220, 220, 0), (10, 10, 730, 855), 6)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
