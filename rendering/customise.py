import sys

import pygame
from pygame.locals import *

sys.path.append(r"../PACMAN")
from datatypes.GameCharacters import CharacterChoice

# Initialize Pygame
pygame.init()

# Set up the window
window_width = 750
window_height = 875
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pacman")
font_file1 = "./assets/fonts/Gameplay.ttf"
font = pygame.font.Font(font_file1, 25)
font_file = "./assets/fonts/PacfontGood-yYye.ttf"
font1 = pygame.font.Font(font_file, 35)
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

cm1 = pygame.transform.scale(
    pygame.image.load("./assets/sprite/CookieMonster4.png"), (100, 100)
)
cm2 = pygame.transform.scale(
    pygame.image.load("./assets/sprite/cookie image.png"), (100, 100)
)
classic1 = pygame.transform.scale(
    pygame.image.load("./assets/sprite/menughost1.png"), (100, 100)
)
classic2 = pygame.transform.scale(
    pygame.image.load("./assets/sprite/2.png"), (100, 100)
)
retro1 = pygame.transform.scale(
    pygame.image.load("./assets/sprite/Pacman-1.png"), (100, 100)
)
retro2 = pygame.transform.scale(
    pygame.image.load("./assets/sprite/Ghost-whip-1.png"), (100, 100)
)
special1 = pygame.transform.scale(
    pygame.image.load("./assets/sprite/spb1.png"), (100, 100)
)
special2 = pygame.transform.scale(
    pygame.image.load("./assets/sprite/Raiden4.png"), (100, 100)
)

# List to store user's choice and loads the appropriate files for each sprites
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

game_mode = {
    "Classic": WHITE,  # Color of text
    "Retro": WHITE,
    "Cookie Monster": WHITE,
    "Special": WHITE,
}

maze_color = {"Cyan": WHITE, "Blue": WHITE, "Yellow": WHITE}

dot_color = {"White": WHITE, "Red": WHITE, "Green": WHITE}


def main(username: str) -> None:
    """Main function to run the customization screen."""
    global u_name
    global choice
    u_name = username
    running = True
    while running:
        # Handle events

        # Clear the screen
        window.fill(BLACK)
        text_surface = font.render("Back", True, "red")
        rect = text_surface.get_rect(center=(45, 25))
        window.blit(text_surface, rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if rect.collidepoint(pos):
                    return choice
                if classic_text_rect.collidepoint(pos):
                    # Checks if user has selected a theme
                    game_mode["Classic"] = RED
                    game_mode["Retro"] = WHITE
                    game_mode["Cookie Monster"] = WHITE
                    game_mode["Special"] = WHITE
                    choice[0] = {
                        "pacman": CharacterChoice.ClassicPacmanFrames,
                        "Ghost1": CharacterChoice.ClassicGhostFrame1,
                        "Ghost2": CharacterChoice.ClassicGhostFrame2,
                        "Ghost3": CharacterChoice.ClassicGhostFrame3,
                        "Ghost4": CharacterChoice.ClassicGhostFrame4,
                        "Frightened": CharacterChoice.FrightenedGhostFrame,
                    }

                elif retro_text_rect.collidepoint(pos):
                    game_mode["Classic"] = WHITE
                    game_mode["Retro"] = RED
                    game_mode["Cookie Monster"] = WHITE
                    game_mode["Special"] = WHITE
                    choice[0] = {
                        "pacman": CharacterChoice.RetroPacmanFrame,
                        "Ghost1": CharacterChoice.RetroGhost1,
                        "Ghost2": CharacterChoice.RetroGhost2,
                        "Ghost3": CharacterChoice.RetroGhost3,
                        "Ghost4": CharacterChoice.RetroGhost4,
                        "Frightened": CharacterChoice.FrightenedGhostFrame,
                    }

                elif cm_text_rect.collidepoint(pos):
                    game_mode["Classic"] = WHITE
                    game_mode["Retro"] = WHITE
                    game_mode["Cookie Monster"] = RED
                    game_mode["Special"] = WHITE
                    choice[0] = {
                        "pacman": CharacterChoice.CookiePacmanFrame,
                        "Ghost1": CharacterChoice.RetroGhost1,
                        "Ghost2": CharacterChoice.RetroGhost2,
                        "Ghost3": CharacterChoice.RetroGhost3,
                        "Ghost4": CharacterChoice.RetroGhost4,
                        "Frightened": CharacterChoice.CookieFrightenedFrame,
                    }

                elif special_text_rect.collidepoint(pos):
                    game_mode["Classic"] = WHITE
                    game_mode["Retro"] = WHITE
                    game_mode["Cookie Monster"] = WHITE
                    game_mode["Special"] = RED
                    choice[0] = {
                        "pacman": CharacterChoice.SpecialPacmanFrames,
                        "Ghost1": CharacterChoice.CookiePacmanFrame,
                        "Ghost2": CharacterChoice.SpecialGhostFrame1,
                        "Ghost3": CharacterChoice.SpecialGhostFrame2,
                        "Ghost4": CharacterChoice.SpecialGhostFrame3,
                        "Frightened": CharacterChoice.CookieFrightenedFrame,
                    }

                elif maze_color1_rect.collidepoint(pos):
                    maze_color["Cyan"] = "Cyan"
                    maze_color["Blue"] = WHITE
                    maze_color["Yellow"] = WHITE
                    choice[1] = "Cyan"

                elif maze_color2_rect.collidepoint(pos):
                    maze_color["Cyan"] = WHITE
                    maze_color["Blue"] = "Blue"
                    maze_color["Yellow"] = WHITE
                    choice[1] = "Blue"

                elif maze_color3_rect.collidepoint(pos):
                    maze_color["Cyan"] = WHITE
                    maze_color["Blue"] = WHITE
                    maze_color["Yellow"] = "Yellow"
                    choice[1] = "Yellow"

                elif dot_color1_rect.collidepoint(pos):
                    dot_color["White"] = RED
                    dot_color["Red"] = WHITE
                    dot_color["Green"] = WHITE
                    choice[2] = "White"

                elif dot_color2_rect.collidepoint(pos):
                    dot_color["White"] = WHITE
                    dot_color["Red"] = RED
                    dot_color["Green"] = WHITE
                    choice[2] = "Red"

                elif dot_color3_rect.collidepoint(pos):
                    dot_color["White"] = WHITE
                    dot_color["Red"] = WHITE
                    dot_color["Green"] = "Green"
                    choice[2] = "Green"

        # Render and display the first set of text labels
        classic_text = font.render("Classic", True, game_mode["Classic"])
        classic_text_rect = classic_text.get_rect(topleft=(500, 220))
        window.blit(classic_text, classic_text_rect)

        retro_text = font.render("Retro", True, game_mode["Retro"])
        retro_text_rect = retro_text.get_rect(topleft=(115, 470))
        window.blit(retro_text, retro_text_rect)

        cm_text = font.render("Cookie Monster", True, game_mode["Cookie Monster"])
        cm_text_rect = cm_text.get_rect(topleft=(50, 220))
        window.blit(cm_text, cm_text_rect)

        special_text = font.render("Special", True, game_mode["Special"])
        special_text_rect = special_text.get_rect(topleft=(500, 470))
        window.blit(special_text, special_text_rect)

        # Render and display the second set of text labels
        maze_color1 = font.render("Cyan", True, maze_color["Cyan"])
        maze_color1_rect = maze_color1.get_rect(topleft=(120, 600))
        window.blit(maze_color1, maze_color1_rect)

        maze_color2 = font.render("Blue", True, maze_color["Blue"])
        maze_color2_rect = maze_color2.get_rect(topleft=(120, 700))
        window.blit(maze_color2, maze_color2_rect)

        maze_color3 = font.render("Yellow", True, maze_color["Yellow"])
        maze_color3_rect = maze_color3.get_rect(topleft=(100, 800))
        window.blit(maze_color3, maze_color3_rect)

        # Render and display the third set of text labels
        dot_color1 = font.render("White", True, dot_color["White"])
        dot_color1_rect = dot_color1.get_rect(topleft=(530, 600))
        window.blit(dot_color1, dot_color1_rect)

        dot_color2 = font.render("Red", True, dot_color["Red"])
        dot_color2_rect = dot_color2.get_rect(topleft=(540, 700))
        window.blit(dot_color2, dot_color2_rect)

        dot_color3 = font.render("Green", True, dot_color["Green"])
        dot_color3_rect = dot_color3.get_rect(topleft=(530, 800))
        window.blit(dot_color3, dot_color3_rect)

        window.blit(font1.render("GAME MODE", True, "cyan"), (240, 20))
        window.blit(font1.render("MAZE COLOR", True, "cyan"), (30, 550))
        window.blit(font1.render("DOT COLOR", True, "cyan"), (450, 550))

        window.blit(cm1, (50, 100))
        window.blit(cm2, (170, 100))
        window.blit(classic1, (50, 330))
        window.blit(classic2, (170, 330))
        window.blit(retro1, (450, 100))
        window.blit(retro2, (575, 100))
        window.blit(special1, (450, 330))
        window.blit(special2, (575, 330))
        # button(pygame.mouse.get_pos())
        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
