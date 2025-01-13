import sqlite3

import pygame

pygame.init()

font_file = r"./assets/fonts/PacfontGood-yYye.ttf"
font_file1 = r"./assets/fonts/subway-ticker/SUBWT___.ttf"

# initialising the font sizes
font_size = 70
font_size1 = 20


def get_score(username) -> None:
    """
    Retrieve and display the scores from the database.

    Parameters
    ----------
    username : str

    -
    The username of the player.

    """
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT username, score FROM user ORDER BY score DESC
    """
    )
    rows = cursor.fetchall()

    # Create a font object for rendering the text
    font = pygame.font.Font(font_file1, font_size1)
    y_pos = 200
    i = 1
    for row in rows:
        if row[0] == username:
            text_surface = font.render(str(i), True, "Blue")
            window.blit(text_surface, (100, y_pos + 100))
            text_surface1 = font.render(row[0], True, "Blue")
            window.blit(text_surface1, (250, y_pos + 100))
            text_surface2 = font.render(str(row[1]), True, "Blue")
            window.blit(text_surface2, (600, y_pos + 100))
            y_pos += 30

        elif i <= 10:
            text_surface = font.render(str(i), True, "White")
            window.blit(text_surface, (100, y_pos + 100))
            text_surface1 = font.render(row[0], True, "White")
            window.blit(text_surface1, (250, y_pos + 100))
            text_surface2 = font.render(str(row[1]), True, "White")
            window.blit(text_surface2, (600, y_pos + 100))
            y_pos += 30
        i = i + 1

    connection.commit()
    connection.close()


class Button:
    def __init__(self, xpos: int, ypos: int, text: str) -> None:
        """
        Represents a button on the screen.

        Parameters
        ----------
        xpos : int
            The x-coordinate of the button's center.
        ypos : int
            The y-coordinate of the button's center.
        text : str
            The text to be displayed on the button.
        """
        self.xpos = xpos
        self.ypos = ypos
        self.text = text
        self.font = pygame.font.Font(font_file1, 40)
        self.text_surface = self.font.render(self.text, True, "red")
        self.rect = self.text_surface.get_rect(center=(self.xpos, self.ypos))

    def update(self) -> None:
        """Updates the button by drawing the text on the screen."""
        window.blit(self.text_surface, self.rect)

    def check_input(self, pos: tuple) -> None:
        """
        Checks if the button was clicked.

        Parameters
        ----------
        pos : tuple

        -
        The position of the mouse click.

        Returns
        -------
        bool

        -
        True if the button was clicked, False otherwise.

        """
        if self.rect.collidepoint(pos) and self.text == "Back":
            return True

    def animate_button(self, pos: tuple) -> None:
        """
        Animates the button by changing its color when hovering over it.

        Parameters
        ----------
        pos : tuple

        -
        The position of the mouse cursor.

        """
        if self.rect.collidepoint(pos):
            self.text_surface = self.font.render(self.text, True, "white")
        else:
            self.text_surface = self.font.render(self.text, True, "red")


button1 = Button(100, 750, "Back")

# Create a Pygame window
window = pygame.display.set_mode((750, 875))


def main(username: str) -> None:
    """
    Main function to display the leaderboard on the window.

    Parameters
    ----------
    username : str

    -
    The username of the player.

    """
    global u_name
    u_name = username
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and button1.check_input(
                pygame.mouse.get_pos()
            ):
                return

        # Clear the screen
        window.fill("black")
        font = pygame.font.Font(font_file, font_size)
        window.blit(font.render("leaderboard", True, "Red"), (110, 100))
        button1.update()
        button1.animate_button(pygame.mouse.get_pos())

        get_score(username)

        # Update the display
        pygame.display.flip()
    pygame.quit()
