import sqlite3

import pygame
from passlib.hash import bcrypt_sha256

from rendering import cutscene1, mainmenu
from rendering.mainmenu import Button

pygame.init()

# Set the font file path
font_file = "./assets/fonts/FantasmytasSt-8YDJ.ttf"
font_file1 = "./assets/fonts/subway-ticker/SUBWT___.ttf"
font_file2 = "./assets/fonts/Gameplay.ttf"

# set the font sizes
font_size = 100
font_size1 = 30


window = pygame.display.set_mode([750, 875])


class input_text:
    """
    A class representing an input text box.

    ...

    Attributes
    ----------
    rect : pygame.Rect

    -
    rectangle representing the position and size of the text box

    font : pygame.font.Font

    -
    font used for rendering the text

    font1 : pygame.font.Font

    -
    font used for rendering the password (hidden characters)

    text : str

    -
    the actual text entered by the user

    showtext : str

    -
    the text to be displayed on the screen (password characters hidden)

    clicked : bool

    -
    indicates if the text box is currently clicked

    color_notclicked : str

    -
    color of the text box when not clicked

    color_clicked : str

    -
    color of the text box when clicked

    username : bool

    -
    indicates if the text box is for entering username or password

    Methods
    -------
    handle_event(event: pygame.event.Event) -> None:

    -
    Handles the events (mouse click and keyboard press) for the text box.

    update() -> None:

    -
    Updates the color of the text box based on its clicked state.

    draw(window: pygame.Surface) -> None:

    -
    Renders and displays the text box on the screen.

    get_text() -> str:

    -
    Returns the text entered in the text box.

    """

    def __init__(self, position, size, color, color_clicked, username):
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.font = pygame.font.Font(font_file1, font_size1)
        self.font1 = pygame.font.Font(font_file, 40)
        self.text = ""
        self.showtext = ""
        self.clicked = False
        self.color_notclicked = color
        self.color_clicked = color_clicked
        # boolean : True if user is entering username , False if user is entering password
        self.username = username

    def handle_event(self, event):
        """To check if user clicked input box and display character pressed"""

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
            else:
                self.clicked = False

        if event.type == pygame.KEYDOWN:
            if self.clicked:
                # remove last character is backspace is pressed
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.showtext = self.showtext[:-1]
                elif event.key != pygame.K_RETURN:
                    # adding the charcter input to the text string
                    if len(self.text) < 8:
                        self.text += event.unicode

                        # To not show password on screen
                        self.showtext += "o"

    def update(self) -> None:
        """Change color of text box if user click"""
        if self.clicked:
            self.color = self.color_clicked
        else:
            self.color = self.color_notclicked

    def draw(self, window: pygame.display) -> None:
        """Show the character entered by user"""
        pygame.draw.rect(window, self.color, self.rect, border_radius=15)
        if self.username:
            # if user is entering username
            text_surface = self.font.render(self.text, True, "Black")
            text_rect = text_surface.get_rect(center=self.rect.center)
        else:
            # if user is entering password (do not show password on screen)
            text_surface = self.font1.render(self.showtext, True, "Black")
            text_rect = text_surface.get_rect(center=self.rect.center)

        window.blit(text_surface, text_rect)

    def get_text(self) -> None:
        return self.text


class Ghost_deco:
    """
    A class representing a ghost decoration.

    ...

    Attributes
    ----------
    xpos : int

    -
    x-coordinate position of the ghost

    ypos : int

    -
    y-coordinate position of the ghost

    state : bool

    -
    indicates if the ghost is in the current state

    font : pygame.font.Font

    -
    font used for rendering the ghost text

    text : str

    -
    the text displayed on the ghost

    color : str

    -
    color of the ghost

    toggle_color : str

    -
    color of the ghost in the toggled state

    toggle_text : str

    -
    the text displayed on the ghost in the toggled state


    text_surface : pygame.Surface

    -
    rendered surface of the text

    rect : pygame.Rect

    -
    rectangle representing the position and size of the ghost decoration

    text_surface1 : pygame.Surface

    -
    rendered surface of the toggle text

    Methods
    -------
    update() -> None:
        Updates the display state of the ghost on the screen.
    """

    def __init__(
        self,
        xpos: int,
        ypos: int,
        text: str,
        toggle_text: str,
        color,
        toggle_color,
        state: bool,
    ):
        self.xpos = xpos
        self.ypos = ypos
        self.state = state
        self.font = pygame.font.Font(font_file, font_size)
        self.text = text
        self.color = color
        self.toggle_color = toggle_color
        self.toggle_text = toggle_text
        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect(center=(self.xpos, self.ypos))
        self.text_surface1 = self.font.render(self.toggle_text, True, self.toggle_color)

    def update(self) -> None:
        """
        Updates the display state of the ghost on the screen.
        """
        if self.state:
            window.blit(self.text_surface, self.rect)
        else:
            window.blit(self.text_surface1, self.rect)


def label(text: str, pos_x: int, pos_y: int) -> None:
    """
    Displays text on the screen.

    Parameters
    ----------
    text : str

    -
    The text to be displayed.

    pos_x : int

    -
    The x-coordinate position of the text.

    pos_y : int

    -
    The y-coordinate position of the text.

    """

    font = pygame.font.Font(font_file2, 45)
    text_surface = font.render(text, True, (220, 220, 0))
    window.blit(text_surface, (pos_x, pos_y))


def check_username_unique(username: str) -> bool:
    """
    Checks if the username entered by the user is unique.

    Parameters
    ----------

    username : str

    -
    The username to be checked.

    Returns
    -------

    bool

    -
    True if the username is unique, False otherwise.

    """
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT username FROM user
    """
    )
    rows = cursor.fetchall()

    for row in rows:
        if row[0] == username:
            connection.commit()
            connection.close()
            return True

    connection.commit()
    connection.close()


def signup(username: str, password: str) -> None:
    """
    Adds user credentials for sign up (after validation) in the database.

    Parameters
    ----------

    username : str

    -
    The username to be added.

    password : str

    -
    The password to be added.

    """

    # Hashing the password
    password = bcrypt_sha256.hash(password)
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO user (username, password)
        VALUES (?, ?)
    """,
        (username, password),
    )
    connection.commit()
    connection.close()


def check_credentials(username: str, password: str) -> bool:
    """
    Checks if the credentials entered by the user match.

    Parameters
    ----------

    username : str

    -
    The username to be checked.

    password : str

    -
    The password to be checked.

    Returns
    -------
    bool

    -
    True if the credentials match, False otherwise.

    """

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT username,password FROM user
    """
    )
    rows = cursor.fetchall()

    for row in rows:
        if row[0] == username:
            # check if input password matches hashed password
            if bcrypt_sha256.verify(password, row[1]):
                connection.commit()
                connection.close()
                return True

    connection.commit()
    connection.close()


def error_message(error1: bool, error2: bool, error3: bool) -> None:
    """
    Displays validation error messages on the screen.

    Parameters
    ----------

    error1 : bool

    -
    Indicates if there is an error related to blank fields or spaces.

    error2 : bool

    -
    Indicates if there is an error related to duplicate usernames.

    error3 : bool

    -
    Indicates if there is an error related to mismatched credentials.

    """
    if error1 == True:
        error_text1 = pygame.font.Font(font_file1, 20).render(
            "Username and password cannot be blank or contain space", True, "Red"
        )
        window.blit(error_text1, (80, 375))

    if error2 == True:
        error_text2 = pygame.font.Font(font_file1, 20).render(
            "This username exists already", True, "Red"
        )
        window.blit(error_text2, (200, 375))

    if error3 == True:
        error_text3 = pygame.font.Font(font_file1, 20).render(
            "Username and password do not match", True, "Red"
        )
        window.blit(error_text3, (175, 375))


def main():
    """
    The main function for running the login/sign-up screen.

    It handles user inputs, validates credentials, displays error messages, and
    manages the screen elements and transitions.
    """

    input_box = input_text((400, 100), (300, 70), " blue", (220, 210, 0), True)
    input_box1 = input_text((400, 250), (300, 70), " blue", (220, 210, 0), False)

    button = Button(600, 500, "Login", font_file1)
    button1 = Button(200, 500, "Sign Up", font_file1)

    x_pos = -360
    state = True
    error1 = False
    error2 = False
    error3 = False

    running = True

    while running:
        window.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                space = False
                username = input_box.get_text()
                password = input_box1.get_text()

                for i in username:
                    if i == " ":
                        space = True
                for j in password:
                    if j == " ":
                        space = True

                # if user clicked login button
                if button.check_input(pygame.mouse.get_pos()) == True:
                    if check_credentials(username, password) == True:
                        error3 = False
                        mainmenu.main(username)
                        exit()

                    else:
                        error3 = True
                        error1 = False
                        error2 = False

                # if user clicked sign up button
                if button1.check_input(pygame.mouse.get_pos()) == True:
                    # validation to ensure that password/username is not blank/doesnt contain space
                    if username == "" or password == "" or space:
                        error1 = True
                        error2 = False
                        error3 = False
                    else:
                        error1 = False

                    if check_username_unique(username):
                        error2 = True
                        error1 = False
                        error3 = False
                    else:
                        error2 = False

                    if error1 is False and error2 is False:
                        # updating username and password in database
                        signup(username, password)
                        cutscene1.main(username)
                        exit()

            input_box.handle_event(event)
            input_box1.handle_event(event)

        input_box.update()
        input_box1.update()

        button.animate_button(pygame.mouse.get_pos())
        button1.animate_button(pygame.mouse.get_pos())

        # Instances of Ghost_deco class representing different ghosts
        ghost0 = Ghost_deco(x_pos, 700, "B", "C", (34, 202, 224), (245, 46, 192), state)
        ghost1 = Ghost_deco(x_pos + 60, 700, "A", "M", (0, 255, 132), "purple", state)
        ghost2 = Ghost_deco(x_pos + 120, 700, "T", "U", "yellow", "cyan", state)
        ghost3 = Ghost_deco(x_pos + 180, 700, "P", "V", "pink", "red", state)
        ghost4 = Ghost_deco(x_pos + 240, 700, "N", "o", "orange", (255, 218, 0), state)
        ghost5 = Ghost_deco(x_pos + 300, 700, "X", "Z", "Blue", "yellow", state)
        ghost6 = Ghost_deco(
            x_pos + 360, 700, "S", "P", (255, 110, 0), (255, 24, 0), state
        )

        ghosts = [ghost0, ghost1, ghost2, ghost3, ghost4, ghost5, ghost6]

        for ghost in ghosts:
            ghost.update()

        button.update()
        button1.update()

        pygame.draw.rect(window, "Blue", (0, 0, 750, 875), 6)
        pygame.draw.rect(window, "Black", (5, 5, 740, 865), 6)
        pygame.draw.rect(window, "Blue", (10, 10, 730, 855), 6)

        # Adding text tabel to the screen
        label("Username :", 80, 110)
        label("Password :", 80, 260)

        input_box.draw(window)
        input_box1.draw(window)

        # changing state of ghost and position when reached end of screen
        x_pos = x_pos + 2
        if x_pos > 750:
            x_pos = -360
            state = not state

        # displaying any error messages that arise when validating password
        error_message(error1, error2, error3)

        pygame.display.flip()

    pygame.quit()
