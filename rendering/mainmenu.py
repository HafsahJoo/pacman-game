#!/bin/python3
import sqlite3
import sys
import webbrowser

import pygame

from rendering import customise, leaderboard, minigame

sys.path.append(r"../PACMAN")
from datatypes.GameCharacters import CharacterChoice
from inputHandling.event import EventDispatcher
from rendering.maze import HEIGHT, WIDTH, create_mask, draw_maze
from spriteLogic.Ghost.ghostlLogic_longestTunnel import LongestTunnel_Ghost
from spriteLogic.Ghost.ghostLogic_pathfinding import PathFinding_Ghost
from spriteLogic.Ghost.ghostLogic_random import RandomGhost
from spriteLogic.Ghost.ghostLogic_scatter import Scatter_Ghost
from spriteLogic.mazeLogic import MazeLogic
from spriteLogic.pacmanLogic import Pacman

pygame.init()

# Connect to the SQLite database
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

window_width = 750
window_height = 875
window = pygame.display.set_mode((window_width, window_height))

font_file = r"./assets/fonts/PacfontGood-yYye.ttf"
font_file1 = r"./assets/fonts/Gameplay.ttf"

image1 = pygame.image.load(r"./assets/sprite/menughost1.png")
image2 = pygame.image.load(r"./assets/sprite/menughost2.png")
image3 = pygame.image.load(r"./assets/sprite/menughost3.png")
image4 = pygame.image.load(r"./assets/sprite/menughost4.png")
image5 = pygame.image.load(r"./assets/sprite/menughost5.png")
image6 = pygame.image.load(r"./assets/sprite/pacfont1.png")

font_size = 80
font_size1 = 36

choice = [
    {
        "pacman": CharacterChoice.ClassicPacmanFrames,
        "Ghost1": CharacterChoice.ClassicGhostFrame1,
        "Ghost2": CharacterChoice.ClassicGhostFrame2,
        "Ghost3": CharacterChoice.ClassicGhostFrame3,
        "Ghost4": CharacterChoice.ClassicGhostFrame4,
        "Frightened": CharacterChoice.FrightenedGhostFrame,
    },
    "Blue",
    "White",
]


class Button:
    def __init__(self, xpos: int, ypos: int, text: str, font_file: str):
        """
        Represents a button on the screen.

        Parameters
        ----------
        xpos : int

        -
        The x-coordinate of the button's center.

        ypos : int

        -
        The y-coordinate of the button's center.

        text : str

        -
        The text to be displayed on the button.

        font_file : str

        -
        The file path of the font used for the button text.

        """
        self.xpos = xpos
        self.ypos = ypos
        self.text = text
        self.fontfile = font_file
        self.font = pygame.font.Font(self.fontfile, font_size1)
        self.text_surface = self.font.render(self.text, True, (220, 220, 0))
        self.rect = self.text_surface.get_rect(center=(self.xpos, self.ypos))

    def set_color(self) -> None:
        """Draws the text on the screen with a specific color."""
        self.text_surface = self.font.render(self.text, True, "Blue")
        self.rect = self.text_surface.get_rect(center=(self.xpos, self.ypos))
        window.blit(self.text_surface, self.rect)

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

        global choice
        if self.rect.collidepoint(pos) and self.text == "Login":
            return True

        if self.rect.collidepoint(pos) and self.text == "Sign Up":
            return True

        if self.rect.collidepoint(pos) and self.text == "Leaderboard":
            leaderboard.main(u_name)

        if self.rect.collidepoint(pos) and self.text == "Learn More":
            webbrowser.open("https://pacman.fandom.com/wiki/Pac-Man")

        if self.rect.collidepoint(pos) and self.text == "Quit Game":
            return True

        if self.rect.collidepoint(pos) and self.text == "Back":
            return True

        if self.rect.collidepoint(pos) and self.text == "Customize":
            global choice
            choice = customise.main(u_name)

        if self.rect.collidepoint(pos) and self.text == "Mini Game":
            minigame.main()

        if self.rect.collidepoint(pos) and self.text == "Play Game":
            game(u_name, choice)

    def animate_button(self, pos):
        """
        Animates the button by changing its color when hovering over it.

        Parameters
        ----------

        pos : tuple

        -
        The position of the mouse cursor.

        Returns
        -------

        bool

        -
        True if the mouse is hovering over the button, False otherwise.

        """
        if self.rect.collidepoint(pos):
            self.text_surface = self.font.render(self.text, True, "white")
            self.rect.center = self.xpos - 3, self.ypos - 7
            return True
        else:
            self.text_surface = self.font.render(self.text, True, (220, 220, 0))
            self.rect.center = self.xpos, self.ypos


# Instances of Button class representing different buttons
buttonA = Button(368, 260, "Play Game", font_file1)
buttonB = Button(368, 360, "Customize", font_file1)
buttonC = Button(368, 460, "Leaderboard", font_file1)
buttonD = Button(368, 560, "Learn More", font_file1)
buttonE = Button(368, 760, "Quit Game", font_file1)
buttonF = Button(368, 660, "Mini Game", font_file1)
button0 = Button(375, 265, "Play Game", font_file1)
button1 = Button(375, 365, "Customize", font_file1)
button2 = Button(375, 465, "Leaderboard", font_file1)
button3 = Button(375, 565, "Learn More", font_file1)
button4 = Button(375, 765, "Quit Game", font_file1)
button5 = Button(375, 665, "Mini Game", font_file1)


def game(username, theme: list) -> None:
    """Main game function."""

    # Creating an event handler for pacman
    sys.path.append(r"../PACMAN")
    event = EventDispatcher()

    pygame.mixer.music.load("./assets/sound/pacman_beginning.wav")
    pygame.mixer.music.play()

    gameOver = False
    levelCompleted = False
    score = 0

    font = pygame.font.Font(r"./assets/fonts/subway-ticker/SUBWT___.ttf", 32)

    def display_game_over(screen: pygame.Surface) -> None:
        """Display a game over screen"""
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 72)
        # Display game over text and final score
        game_over_text = font.render("Game Over. You died!", True, "Yellow")
        score_text = font.render(f"Your final score is {score}", True, "Yellow")
        font = pygame.font.Font(None, 20)
        menu_text = font.render("Press space to exit game", True, "Red")

        text_rect_game_over = game_over_text.get_rect(center=(375, 400))
        text_rect_score = score_text.get_rect(center=(375, 550))
        text_rect_menu = menu_text.get_rect(center=(375, 800))

        # Place the texts on the screen
        screen.blit(game_over_text, text_rect_game_over)
        screen.blit(score_text, text_rect_score)
        screen.blit(menu_text, text_rect_menu)

        # Retrieve the current score of the user from the database

        cursor.execute("SELECT score FROM user WHERE username = ?", (username,))
        row = cursor.fetchone()

        high_score = row[0]

        # Compare the current score with the new score
        if score > high_score:
            # Update the score in the database
            cursor.execute(
                "UPDATE user SET score = ? WHERE username = ?", (score, username)
            )
            connection.commit()

        connection.close()

    def display_level_completed(screen: pygame.Surface) -> None:
        """Display a winning screen"""
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        screen.fill((0, 0, 0))
        window.blit(
            pygame.transform.scale(
                pygame.image.load("./assets/sprite/bgimage.png"), (1000, 1200)
            ),
            (-125, -300),
        )
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("You saved MS pacman!", True, "Cyan")
        score_text = font.render(f"Your final score is {score}", True, "Cyan")
        font = pygame.font.Font(None, 20)
        menu_text = font.render("Press space to exit game", True, "Red")

        text_rect_game_over = game_over_text.get_rect(center=(375, 200))
        text_rect_score = score_text.get_rect(center=(375, 300))
        text_rect_menu = menu_text.get_rect(center=(375, 800))

        screen.blit(game_over_text, text_rect_game_over)
        screen.blit(score_text, text_rect_score)
        screen.blit(menu_text, text_rect_menu)

        cursor.execute("SELECT score FROM user WHERE username = ?", (username,))
        row = cursor.fetchone()

        high_score = row[0]

        # Compare the current score with the new score
        if score > high_score:
            # Update the score in the database
            cursor.execute(
                "UPDATE user SET score = ? WHERE username = ?", (score, username)
            )
            connection.commit()

        connection.close()

    def display_score(updateScore: int) -> None:
        """Fetch the score of pacman."""
        nonlocal score
        score = updateScore

    def game_over() -> None:
        """Checks if the game is over"""
        nonlocal gameOver
        gameOver = True

    def level_completed() -> None:
        """Checks if the game has been won"""
        nonlocal levelCompleted
        levelCompleted = True

    event.enroll("game_over", game_over)
    event.enroll("display_score", display_score)
    event.enroll("level_completed", level_completed)

    # Creating an object mazeLogic
    mazeLogic = MazeLogic(event)

    # Adding a class to a groupsingle
    pacmanGroup = pygame.sprite.GroupSingle()

    pacmanGroup.add(Pacman(event, theme[0]["pacman"]))

    # Adding the 4 ghosts' classes to a group
    ghostGroup = pygame.sprite.Group()

    ghostGroup.add(PathFinding_Ghost(event, theme[0]["Ghost4"], theme[0]["Frightened"]))
    ghostGroup.add(RandomGhost(event, theme[0]["Ghost1"], theme[0]["Frightened"]))
    ghostGroup.add(
        LongestTunnel_Ghost(event, theme[0]["Ghost3"], theme[0]["Frightened"])
    )
    ghostGroup.add(Scatter_Ghost(event, theme[0]["Ghost2"], theme[0]["Frightened"]))

    clock = pygame.time.Clock()

    # Creating display with WIDTH and HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pacman 2.0")

    draw_maze(0, theme[1], theme[2])
    step = 0

    # Creating a mask for the maze
    create_mask()

    # Spawn the sprites
    event.associate("spawn_entities")

    # Main loop
    while True:
        # Draw and update everything
        for close in pygame.event.get():
            if close.type == pygame.QUIT:
                # Event to kill all threads
                event.associate("kill_process")
                pygame.quit()
                sys.exit()

        # Draws a black screen after each frame
        screen.fill((0, 0, 0))
        draw_maze(int(step), theme[1], theme[2])

        if gameOver:
            display_game_over(screen)
            keys = pygame.key.get_pressed()
            for close in pygame.event.get():
                if close.type == pygame.QUIT or keys[pygame.K_SPACE]:
                    # Event to kill all threads
                    event.associate("kill_process")
                    pygame.quit()
                    sys.exit()
        elif levelCompleted:
            display_level_completed(screen)
            keys = pygame.key.get_pressed()
            for close in pygame.event.get():
                if close.type == pygame.QUIT or keys[pygame.K_SPACE]:
                    # Event to kill all threads
                    event.associate("kill_process")
                    pygame.quit()
                    sys.exit()
        else:
            if step < 1020:
                step += 4
            else:
                # Call the update methods of each sprite to play the game
                pacmanGroup.draw(screen)
                pacmanGroup.update()
                ghostGroup.draw(screen)
                ghostGroup.update()
                mazeLogic.update(screen)
                textSurface = font.render(f"Score : {score}", True, "white")
                screen.blit(textSurface, (7, 831))

        pygame.display.update()
        clock.tick(60)


def main(username) -> None:
    """
    Main function to display everything on the window.

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checking if a button is pressed
                button0.check_input(pygame.mouse.get_pos())
                button1.check_input(pygame.mouse.get_pos())
                button2.check_input(pygame.mouse.get_pos())
                button3.check_input(pygame.mouse.get_pos())
                if button4.check_input(pygame.mouse.get_pos()):
                    running = False
                button5.check_input(pygame.mouse.get_pos())

        window.fill("Black")

        # Drawing rectangles to outline the screen
        pygame.draw.rect(window, (220, 220, 0), (0, 0, 750, 875), 6)
        pygame.draw.rect(window, (220, 220, 0), (10, 10, 730, 855), 6)

        window.blit(image6, (85, 50))

        # drawing and setting color for buttons A, B, C, D, and E
        buttonA.set_color()
        buttonB.set_color()
        buttonC.set_color()
        buttonD.set_color()
        buttonE.set_color()
        buttonF.set_color()

        button0.update()
        button1.update()
        button2.update()
        button3.update()
        button4.update()
        button5.update()

        # To display ghost when hovering on text label
        if button0.animate_button(pygame.mouse.get_pos()):
            window.blit(image1, (160, 230))
        if button1.animate_button(pygame.mouse.get_pos()):
            window.blit(image2, (160, 330))
        if button2.animate_button(pygame.mouse.get_pos()):
            window.blit(image3, (120, 430))
        if button3.animate_button(pygame.mouse.get_pos()):
            window.blit(image4, (165, 530))
        if button5.animate_button(pygame.mouse.get_pos()):
            window.blit(image5, (165, 630))
        if button4.animate_button(pygame.mouse.get_pos()):
            window.blit(image5, (165, 730))

        pygame.display.update()

    # Quit Pygame
    pygame.quit()
