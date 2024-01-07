"""This module is responsible for enabling interactions between the user and the program while
also displaying to the user what is happening with the algorithm"""

import pygame as pg
import brutforce
from button import Button
from jeu import *


## @package interface
#  This module contains the Interface class which is used to manage the game interface.

## The Interface class is used to manage the game interface.
class Interface:
    ## The title of the game.
    TITLE = "IQ Puzzler"
    ## The default width of the game window.
    DEFAULT_WIDTH = 1600
    ## The default height of the game window.
    DEFAULT_HEIGHT = 900

    ## The Colors class is used to manage the colors used in the game.
    class Colors:
        ## The color red.
        RED = (220, 25, 0)
        ## The color dark blue.
        DARK_BLUE = (20, 39, 150)
        ## The color green.
        GREEN = (0, 255, 0)
        ## The color magenta.
        MAGENTA = (255, 0, 255)
        ## The color cyan.
        CYAN = (0, 255, 255)
        ## The color yellow.
        YELLOW = (255, 255, 0)
        ## The color pink.
        PINK = (255, 0, 192)
        ## The color purple.
        PURPLE = (64, 0, 64)
        ## The color orange.
        ORANGE = (255, 128, 0)
        ## The color dark green.
        DARK_GREEN = (0, 255, 128)
        ## The color grey.
        GREY = (128, 128, 128)
        ## The color black.
        BLACK = (0, 0, 0)
        ## The color lime green.
        LIME_GREEN = (150, 255, 50)
        ## The color white.
        WHITE = (255, 255, 255)
        ## The color light blue.
        LIGHT_BLUE = (150, 225, 255)
        ## The color blue.
        BLUE = (100, 100, 255)
        ## The color turquoise.
        TURQUOIZE = (0, 125, 125)
        ## The color dark red.
        DARK_RED = (150, 0, 50)
        ## The color dark grey.
        DARK_GREY = (64, 64, 64)

        ## @brief Returns a color given the ID of a shape.
        #  @param id The ID of the shape.
        #  @return The color corresponding to the shape ID.

        def getColorFromID(id: int):
            """
            Returns a color given the ID of a shape
            """
            if id == 1:
                color = Interface.Colors.DARK_BLUE
            elif id == 2:
                color = Interface.Colors.RED
            elif id == 3:
                color = Interface.Colors.LIGHT_BLUE
            elif id == 4:
                color = Interface.Colors.BLUE
            elif id == 5:
                color = Interface.Colors.LIME_GREEN
            elif id == 6:
                color = Interface.Colors.TURQUOIZE
            elif id == 7:
                color = Interface.Colors.DARK_RED
            elif id == 8:
                color = Interface.Colors.YELLOW
            elif id == 9:
                color = Interface.Colors.ORANGE
            elif id == 10:
                color = Interface.Colors.DARK_GREEN
            elif id == 11:
                color = Interface.Colors.PINK
            elif id == 12:
                color = Interface.Colors.PURPLE
            else:
                color = None

            return color

        def getColorFromID2(id: int):
            """
            Returns a color given the ID of a shape
            """
            if id == 1:
                color = Interface.Colors.RED
            elif id == 2:
                color = Interface.Colors.BLUE
            elif id == 3:
                color = Interface.Colors.GREEN
            elif id == 4:
                color = Interface.Colors.MAGENTA
            elif id == 5:
                color = Interface.Colors.CYAN
            elif id == 6:
                color = Interface.Colors.YELLOW
            elif id == 7:
                color = Interface.Colors.ORANGE
            elif id == 8:
                color = Interface.Colors.PINK
            elif id == 9:
                color = Interface.Colors.PURPLE
            elif id == 10:
                color = Interface.Colors.DARK_GREEN
            elif id == 11:
                color = Interface.Colors.GREY
            elif id == 12:
                color = Interface.Colors.WHITE
            else:
                color = None
            return color

    def __init__(self, height: int = 5, width: int = 11) -> None:
        # Used to make sure when a key is held down that we only press it once
        self.previous_keys = []
        self.pos_rectified = (0, 0)
        self.fullscreen = False

        # By default select the first shape
        self.held_shape_id = 1
        self.held_shape = Piece(self.held_shape_id)
        self.board = Board(height, width)

        # Creates the pygame window
        self.bkg_color = Interface.Colors.DARK_GREY
        self.SCREEN = pg.display.set_mode((self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT), pg.RESIZABLE)
        self.previous_h = 0
        self.previous_w = 0

        # Defines the variables using the window size
        self.calculate_square_size()
        self.top_space = self.square_size
        self.calculate_offset()
        pg.display.set_caption(self.TITLE)

        self.isRunning = True
        self.game_finished = False

        self.current_mode = "Main"
        self.button_font_size = 16 + self.square_size//5

        # The buttons for each state of the interface
        self.MENUS = {
            "Main": [
                Button((Button.CENTERED, 1/3),self.SCREEN,
                       callback=self.launch, text="Start",
                       font_size=self.button_font_size * 3 // 2,
                       padding=(20,20,20,20),border_size=4),

                Button((Button.CENTERED, 2/3),self.SCREEN,
                       callback=self.quit, text="Exit",
                       font_size=self.button_font_size * 3 // 2,
                       padding=(20,20,20,20),border_size=4)
            ],
            "Running": [
                Button((0.2, 0.1), self.SCREEN,
                        callback=brutforce.launch_brutforce, callbak_args=(self,), text="Bruteforce",
                        font_size=self.button_font_size, border_size=4,border_color=self.Colors.GREEN),

                Button((0.4, 0.1), self.SCREEN,
                        callback=self.back_to_main, text="Quit", border_color=self.Colors.RED,
                        font_size=self.button_font_size, border_size=4)
            ]
        }

    # Calculates the offset to make the grid stay at the relativce center of the windo
    def calculate_offset(self) -> None:
        self.grid_offset = (self.SCREEN.get_width() - self.square_size * self.board.width,
                       self.SCREEN.get_height() - self.square_size * self.board.height - self.top_space)

    # Calculates the size of the cells of the grid to be able to adapt with window resizing 
    def calculate_square_size(self) -> None:
        self.square_size = self.SCREEN.get_width() // self.board.width

    def can_place_shape(self) -> bool:
        return self.board.canPlaceShape(self.held_shape, (self.pos_rectified[1], self.pos_rectified[0]))

    
    def place_shape(self) -> None:
        self.board.placeShape(self.held_shape, (self.pos_rectified[1], self.pos_rectified[0]))


    def update_events(self) -> None:
        """
        Call events() before draw()
        """
        self.mouse_pos = pg.mouse.get_pos()
        self.pos_rectified = self.rectify_mouse_position()
        self.keys = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.isRunning = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if self.current_mode == "Running":
                    if event.button == pg.BUTTON_LEFT and self.is_mouse_in_grid():
                        if self.can_place_shape():
                            self.place_shape()
                            self.inc_shape_ID()
                            if self.board.isFinished():
                                self.game_finished = True
                    if event.button == pg.BUTTON_RIGHT and self.is_mouse_in_grid():
                        id = self.board[self.pos_rectified[1]][self.pos_rectified[0]]
                        self.remove_shape(id)

            if event.type == pg.VIDEORESIZE:
                self.calculate_square_size()
                self.calculate_offset()

        if self.key_pressed(pg.K_ESCAPE):
            self.quit()

        if self.key_pressed(pg.K_F11):
            self.fullscreen = not self.fullscreen
            self.update_screen_mode()

        if self.current_mode == "Running":
            if self.key_pressed(pg.K_LEFT):
                self.inc_shape_ID()
            if self.key_pressed(pg.K_RIGHT):
                self.dec_shape_ID()
            if self.key_pressed(pg.K_r):
                self.held_shape.turnClockwise()
            if self.key_pressed(pg.K_e):
                self.held_shape.mirror()
            if self.key_pressed(pg.K_p):
                brutforce.launch_brutforce(self)

        for but in self.MENUS[self.current_mode]:
            but.update()

        self.previous_keys = self.keys

    # Returns true when a key is first pressed and not when held
    def key_pressed(self, key: int):
        return self.keys[key] and self.keys[key] != self.previous_keys[key]

    # Adapts the displaying of the grid when transitionning to fullscreen and back
    def update_screen_mode(self):
        if self.fullscreen:
            self.previous_h = self.SCREEN.get_height()
            self.previous_w = self.SCREEN.get_width()
            pg.display.set_mode((0, 0), pg.FULLSCREEN)

        else:
            pg.display.set_mode((self.previous_w, self.previous_h), pg.RESIZABLE)

        self.calculate_square_size()
        self.calculate_offset()

    # Draws the everything that can be seen on the interface
    def draw(self) -> None:
        """
        Called once every frame
        """
        self.SCREEN.fill(self.bkg_color)
        if self.current_mode == "Running":
            self.draw_shapes()
            self.draw_preview()
            self.draw_grid()
        
        for but in self.MENUS[self.current_mode]:
            but.draw()

        pg.display.flip()
        pg.display.update()

    def draw_shapes(self) -> None:
        x, y = 0, 0
        for ligne in self.board:
            for tile in ligne:
                if tile != 0:
                    self.draw_square(tile, x, y)
                x += self.square_size
            x = 0
            y += self.square_size

    def draw_grid(self) -> None:
        off_x, off_y = self.grid_offset
        # Draws horizontal lines
        for y in range(len(self.board) + 1):
            pg.draw.line(self.SCREEN, Interface.Colors.BLACK,
                         (off_x//2, y * self.square_size + self.top_space + off_y//2),
                         (self.square_size * self.board.width + off_x//2, y * self.square_size + self.top_space + off_y//2)
            )

        # Draws vertical lines
        for x in range(len(self.board[0]) + 1):
            pg.draw.line(self.SCREEN, Interface.Colors.BLACK,
                         (x * self.square_size + off_x//2, self.top_space + off_y//2),
                         (x * self.square_size + off_x//2, self.board.height * self.square_size + self.top_space + off_y//2)
            )

    def draw_square(self, squareID: int, x: int, y: int) -> None:
        square = pg.Rect(x + self.grid_offset[0] // 2, y + self.grid_offset[1]//2 + self.top_space, self.square_size, self.square_size)
        pg.draw.rect(self.SCREEN, Interface.Colors.getColorFromID2(squareID), square)

    # Draws the preview of the shape when it can be placed where the mouse is postioned
    def draw_preview(self) -> None:
        if not self.can_place_shape():
            return
        
        # Create a surface to enable alpha channel
        sur = pg.Surface((self.square_size, self.square_size))
        sur.set_alpha(64)
        for shapeY in range(len(self.held_shape.piece)):
            for shapeX in range(len(self.held_shape.piece[shapeY])):
                if self.held_shape.piece[shapeY][shapeX] != 0:
                    shape_color = Interface.Colors.getColorFromID2(self.held_shape_id)
                    pg.draw.rect(sur, shape_color, pg.Rect(0, 0, self.square_size, self.square_size))
                    self.SCREEN.blit(sur,
                                    (
                                        (self.pos_rectified[0] + shapeX) * self.square_size + self.grid_offset[0]//2,
                                        (self.pos_rectified[1] + shapeY) * self.square_size + self.top_space + self.grid_offset[1]//2
                                    )
                    )

    # Normalises the mouse position on the window to coordiantes on the grid ex: (1920,1080) => (11,5)
    def rectify_mouse_position(self) -> tuple[int, int]:
        """
        Transforms the mouse position into something that makes it easy to index into the grid
        """
        mouse_pos = pg.mouse.get_pos()
        rectified = ((mouse_pos[0] - self.grid_offset[0]//2) // self.square_size,
                    (mouse_pos[1] - self.grid_offset[1]//2 - self.top_space) // self.square_size)
        return rectified

    # Changes the currently previewed and held shape
    def inc_shape_ID(self) -> None:
        if self.held_shape_id < 12:
            self.held_shape_id += 1
        else:
            self.held_shape_id = 1
        while self.held_shape_id in self.board.used_shapes and len(self.board.used_shapes) != 12:
            if self.held_shape_id < 12:
                self.held_shape_id += 1
            else:
                self.held_shape_id = 1
        self.held_shape = Piece(self.held_shape_id)

    # Changes the currently previewed and held shape
    def dec_shape_ID(self) -> None:
        if self.held_shape_id > 1:
            self.held_shape_id -= 1
        else:
            self.held_shape_id = 12
        while self.held_shape_id in self.board.used_shapes and len(self.board.used_shapes) != 12:
            if self.held_shape_id > 1:
                self.held_shape_id -= 1
            else:
                self.held_shape_id = 12
        self.held_shape = Piece(self.held_shape_id)

    # If a shape is placed under the mouse when the user right clicks
    def remove_shape(self, id: int) -> None:
        """
        Removes a shape from the board given its ID
        """
        if id in self.board.used_shapes:
            self.board.used_shapes.remove(id)
            for x in range(len(self.board)):
                for y in range(len(self.board[x])):
                    if self.board[x][y] == id:
                        self.board[x][y] = 0

    # Changes the menu to the main menu
    def back_to_main(self) -> None:
        self.current_mode = "Main"

    # Changes the menu to the game menu
    def launch(self) -> None:
        self.current_mode = "Running"

    def quit(self) -> None:
        self.isRunning = False

    # Returns if the mouse cursor postion is in the displayed grid
    def is_mouse_in_grid(self) -> bool:
        grid_rect = pg.Rect(self.grid_offset, (self.SCREEN.get_width(), self.SCREEN.get_height()))
        return grid_rect.collidepoint(self.mouse_pos)