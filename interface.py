import pygame as pg
import threading
import brutforce
from button import Button
from jeu import *


# TODO:
# Ameliorer les graphismes




class Interface:
    TITLE = "IQ Puzzler"

    

    # Couleurs (r,g,b)
    class Colors:
        RED = (220, 25, 0)
        DARK_BLUE = (20, 39, 150)
        GREEN = (0, 255, 0)
        MAGENTA = (255, 0, 255)
        CYAN = (0, 255, 255)
        YELLOW = (255, 255, 0)
        PINK = (255, 0, 192)
        PURPLE = (64, 0, 64)
        ORANGE = (255, 128, 0)
        DARK_GREEN = (0, 255, 128)
        GREY = (128, 128, 128)
        BLACK = (0, 0, 0)
        LIME_GREEN = (150, 255, 50)
        WHITE = (255, 255, 255)
        LIGHT_BLUE = (150, 225, 255)
        BLUE = (100, 100, 255)
        TURQUOIZE = (0, 125, 125)
        DARK_RED = (150, 0, 50)
        DARK_GREY = (64, 64, 64)

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
        self.square_size = pg.display.Info().current_w // 11
        self.fullscreen = False

        # By default select the first shape
        self.held_shape_id = 1
        self.held_shape = Piece(self.held_shape_id)
        self.board = Board(height, width)

        # Creates the pygame window
        self.bkg_color = Interface.Colors.DARK_GREY
        self.grid_offset = (0, int(self.square_size))
        self.win_width = width * self.square_size
        self.win_height = height * self.square_size + self.grid_offset[1]
        self.SCREEN = pg.display.set_mode((self.win_width, self.win_height))
        pg.display.set_caption(self.TITLE)

        self.isRunning = True
        self.game_finished = False

        self.current_mode = "Main"

        self.button_font_size = 18 + self.square_size//4

        self.MENUS = {
            "Main": [
                Button((Button.CENTERED, self.win_height // 3 - self.square_size), (self.square_size*2, self.square_size), self.SCREEN,
                       bg_color=self.Colors.BLACK, callback=self.launch, text="Start",
                       font_size=self.button_font_size, border_size=4),
                Button((Button.CENTERED, self.win_height // 3 * 2), (self.square_size*2, self.square_size), self.SCREEN,
                       bg_color=self.Colors.BLACK, callback=self.quit, text="Exit",
                       font_size=self.button_font_size, border_size=4)
            ],
            "Running": [
                    Button((self.square_size // 2, self.square_size // 4),
                            (self.square_size, self.square_size // 2), self.SCREEN,
                            callback=brutforce.launch_brutforce, callbak_args=(self), text="Launch",
                            font_size=self.button_font_size, border_size=4,border_color=self.Colors.GREEN),

                    Button((self.square_size * 2, self.square_size // 4), (self.square_size, self.square_size // 2),
                            self.SCREEN, callback=self.back_to_main, text="Quit", border_color=self.Colors.RED,
                            font_size=self.button_font_size, border_size=4)
            ]
        }

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
                        if self.board.canPlaceShape(self.held_shape, self.pos_rectified):
                            self.board.placeShape(self.held_shape, self.pos_rectified)
                            self.inc_shape_ID()
                            if self.board.isFinished():
                                self.game_finished = True
                    if event.button == pg.BUTTON_RIGHT:
                        id = self.board[self.pos_rectified[0]][self.pos_rectified[1]]
                        self.remove_shape(id)

        if self.key_pressed(pg.K_ESCAPE):
            self.quit()

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
            if self.key_pressed(pg.K_F11):
                self.fullscreen = not self.fullscreen
                self.update_screen_mode()

        for but in self.MENUS[self.current_mode]:
            but.update()

        self.previous_keys = self.keys

    def key_pressed(self, key: int):
        return self.keys[key] and self.keys[key] != self.previous_keys[key]

    def update_screen_mode(self):
        if self.fullscreen:
            pg.display.set_mode((0, 0), pg.FULLSCREEN)
            self.win_height = pg.display.Info().current_h
            self.win_width = pg.display.Info().current_w
            self.grid_offset = (self.grid_offset[0] + self.win_width - self.square_size*11,
                                self.grid_offset[1] + self.win_height - self.square_size*6)
        else:
            self.grid_offset = (self.grid_offset[0] - self.win_width + self.square_size*11,
                                self.grid_offset[1] - self.win_height + self.square_size*6)
            self.win_height = self.square_size * self.board.height + self.grid_offset[1]
            self.win_width = self.square_size * self.board.width + self.grid_offset[0]
            pg.display.set_mode((self.win_width, self.win_height))

    def draw(self) -> None:
        """
        Called once every frame
        """
        self.SCREEN.fill(self.bkg_color)
        if self.current_mode == "Running":
            self.draw_shapes()
            self.draw_preview()
            self.draw_grid()

            if self.game_finished:
                self.draw_win_screen()
        
        for but in self.MENUS[self.current_mode]:
            but.draw()

        pg.display.flip()
        pg.display.update()

    def draw_shapes(self) -> None:
        x, y = 0, 0
        for ligne in self.board:
            for case in ligne:
                if case != 0:
                    self.draw_square(case, x, y)
                x += self.square_size
            x = 0
            y += self.square_size

    def draw_grid(self) -> None:
        off_x, _ = self.grid_offset

        # Draws horizontal lines
        for y in range(len(self.board) + 1):
            pg.draw.line(self.SCREEN, Interface.Colors.BLACK, (off_x//2, self.win_height - y * self.square_size),
                         (self.win_width - off_x//2, self.win_height - y * self.square_size))

        # Draws vertical lines
        for x in range(len(self.board[0]) + 1):
            pg.draw.line(self.SCREEN, Interface.Colors.BLACK,
                         (x * self.square_size + off_x//2, self.win_height - self.board.height * self.square_size),
                         (x * self.square_size + off_x//2, self.win_height))

    def draw_square(self, squareID: int, x: int, y: int) -> None:
        square = pg.Rect(x + self.grid_offset[0] // 2, y + self.grid_offset[1], self.square_size, self.square_size)
        pg.draw.rect(self.SCREEN, Interface.Colors.getColorFromID2(squareID), square)

    def draw_preview(self) -> None:
        if not self.is_mouse_in_grid():
            return
        # Create a surface to enable alpha channel
        sur = pg.Surface((self.square_size, self.square_size))
        sur.set_alpha(64)
        for shapeX in range(len(self.held_shape.piece)):
            for shapeY in range(len(self.held_shape.piece[shapeX])):
                if self.held_shape.piece[shapeX][shapeY] != 0:
                    shape_color = Interface.Colors.getColorFromID2(self.held_shape_id)
                    pg.draw.rect(sur, shape_color, pg.Rect(0, 0, self.square_size, self.square_size))
                    self.SCREEN.blit(sur,
                                     (
                                         (self.pos_rectified[1] + shapeY) * self.square_size + self.grid_offset[0]//2,
                                         (self.pos_rectified[0] + shapeX) * self.square_size + self.grid_offset[1]
                                     )
                    )

    def rectify_mouse_position(self) -> tuple[int, int]:
        """
        Transforms the mouse position into something that makes it easy to index into the grid
        """
        mouse_pos = pg.mouse.get_pos()
        rectified = int((mouse_pos[1] - self.grid_offset[1]) / self.square_size), int(
            (mouse_pos[0] - self.grid_offset[0]) / self.square_size)
        return rectified

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

    def back_to_main(self):
        self.current_mode = "Main"

    def launch(self):
        self.current_mode = "Running"

    def quit(self):
        self.isRunning = False

    def is_mouse_in_grid(self) -> bool:
        grid_rect = pg.Rect(self.grid_offset, (self.win_width, self.win_height))
        return grid_rect.collidepoint(self.mouse_pos)

    def draw_win_screen(self) -> None:
        winRect = pg.Rect(self.win_width // 4, self.win_height // 4, self.win_width // 2, self.win_height // 2)
        winRectBorder = pg.Rect(winRect.left - 1, winRect.top - 1, winRect.width + 2, winRect.height + 2)
        pg.draw.rect(self.SCREEN, self.Colors.WHITE, winRectBorder)
        pg.draw.rect(self.SCREEN, self.Colors.BLACK, winRect)

        # Draws the text
        text = pg.font.SysFont("verdana.ttf", 48)
        text_draw = text.render("The game is finished !", True, self.Colors.WHITE)
        text_draw_rect = text_draw.get_rect()
        text_draw_rect.center = winRect.center
        self.SCREEN.blit(text_draw, text_draw_rect)




if __name__ == "__main__":
    pg.init()
    inte = Interface()
    pg.time.Clock().tick(60)
    while inte.isRunning:
        inte.update_events()
        inte.draw()
