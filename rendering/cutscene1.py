import cv2
import pygame
from pygame.locals import K_SPACE, KEYDOWN

from rendering import mainmenu

pygame.init()

# Font file path
font_file = "./assets/fonts/Gameplay.ttf"

window = pygame.display.set_mode((750, 875))
clock = pygame.time.Clock()

# Text data
text1 = "HELP"
text2 = "PACMAN"
text3 = "SAVE"
text4 = "MS PACMAN"

# Load the font and render text surfaces
font = pygame.font.Font(font_file, 40)
text_surface1 = font.render(text1, True, (220, 220, 0))
text_surface2 = font.render(text2, True, (220, 220, 0))
text_surface3 = font.render(text3, True, (220, 220, 0))
text_surface4 = font.render(text4, True, (220, 220, 0))

# Text positions
rect1 = text_surface1.get_rect(center=(368, 275))
rect2 = text_surface2.get_rect(center=(368, 375))
rect3 = text_surface3.get_rect(center=(368, 475))
rect4 = text_surface4.get_rect(center=(368, 575))

# Load the song
pygame.mixer.music.load("./assets/sound/pacman_intermission.wav")


def text() -> None:
    """Display the text surfaces on the game window"""
    window.blit(text_surface1, rect1)
    window.blit(text_surface2, rect2)
    window.blit(text_surface3, rect3)
    window.blit(text_surface4, rect4)


def main(username: str) -> None:
    """
    Main function to run the game.

    Parameters
    ----------
    username : str
        The username of the player.
    """
    # Video capture
    video = cv2.VideoCapture("./assets/sprite/cutscene.mp4")
    success, video_frame = video.read()
    run = success

    # Start playing the song in the background
    pygame.mixer.music.play(-1)

    while run:
        clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            elif (event.type == KEYDOWN and event.key == K_SPACE) or (
                event.type == pygame.MOUSEBUTTONDOWN
            ):
                # Stop the song and go to the main menu
                pygame.mixer.music.stop()
                mainmenu.main(username)
                exit()

        success, video_frame = video.read()
        if success:
            # Correct the rotation of the video frame
            video_frame = cv2.rotate(video_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Flip the video horizontally
            video_frame = cv2.flip(video_frame, 0)

            # Convert the video frame to RGB format
            video_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2RGB)

            # Resize the frame to match the window dimensions
            video_frame = cv2.resize(video_frame, (650, 700))

            # Create a Pygame surface from the frame
            video_surf = pygame.surfarray.make_surface(video_frame)

            window.blit(video_surf, (40, 0))
        else:
            window.fill("Black")
            text()

        pygame.display.flip()

    pygame.quit()
