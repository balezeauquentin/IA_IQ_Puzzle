import pygame as pg
from button import Button
import brutforce
from jeu import *

import threading
import time

# TODO:
# Ameliorer les graphismes


class Interface:
    """
    Get ready to see a lot of ugly and boring code !
    """

    #Default size of a square from a shape
    SQUARE_SIZE = 100
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
        WHITE = (255, 255 ,255) 
        LIGHT_BLUE = (150, 225, 255)
        BLUE = (100, 100, 255)
        TURQUOIZE = (0 ,125, 125)
        DARK_RED = (150, 0, 50)
        DARK_GREY = (64,64,64)
        
        def getColorFromID(id:int):
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
        
        def getColorFromID2(id:int):
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


    def __init__(self, height:int = 5, width:int = 11) -> None:
    
        # Used to make sure when a key is held down that we only press it once
        self.previous_keys = []
        self.pos_rectified = (0,0)

        # By default select the first shape
        self.held_shape_id = 1
        self.held_shape = Piece(self.held_shape_id)

        self.board = Board(height, width)

        # Creates the pygame window
        self.bkg_color = Interface.Colors.DARK_GREY
        self.GRID_OFFSET = (0, int(self.SQUARE_SIZE))
        self.WIN_WIDTH = width * self.SQUARE_SIZE
        self.WIN_HEIGHT = height * self.SQUARE_SIZE  + self.GRID_OFFSET[1]
        self.screen = pg.display.set_mode((self.WIN_WIDTH , self.WIN_HEIGHT))
        pg.display.set_caption(self.TITLE)

        self.isRunning = True
        self.game_finished = False

        self.buttons:list[Button] = []
        self.launch_bruteforce_but = Button((self.SQUARE_SIZE/2, self.SQUARE_SIZE/4), (self.SQUARE_SIZE,self.SQUARE_SIZE/2), self.screen, brutforce.launch_brutforce, self, text="Test")
        self.buttons.append(self.launch_bruteforce_but)
        self.buttons.append(
            Button((self.SQUARE_SIZE*2, self.SQUARE_SIZE/4), (self.SQUARE_SIZE,self.SQUARE_SIZE/2), self.screen, self.quit, text="quit", border_color=self.Colors.RED)
        )

    def update_events(self) -> None:
        """
        Call events() before draw()
        """
        if self.game_finished:
            return

        self.mouse_pos = pg.mouse.get_pos()
        self.pos_rectified =  self.rectify_mouse_position()
        keys = pg.key.get_pressed()
        for event in pg.event.get():        
            if event.type == pg.QUIT: 
                self.isRunning = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_LEFT and self.isMouseInGrid():
                    if self.board.canPlaceShape(self.held_shape, self.pos_rectified):
                        self.board.placeShape(self.held_shape, self.pos_rectified)
                        self.inc_shape_ID()
                        if self.board.isFinished():
                            self.game_finished = True
                if event.button == pg.BUTTON_RIGHT:
                    id = self.board[self.pos_rectified[0]][self.pos_rectified[1]]
                    self.remove_shape(id)

        if keys[pg.K_ESCAPE]:
            self.quit()
        if keys[pg.K_LEFT] and keys[pg.K_LEFT] != self.previous_keys[pg.K_LEFT]:
            self.inc_shape_ID()
        if keys[pg.K_RIGHT] and  keys[pg.K_RIGHT] != self.previous_keys[pg.K_RIGHT]:
            self.dec_shape_ID()
        if keys[pg.K_r] and keys[pg.K_r] != self.previous_keys[pg.K_r]:
            self.held_shape.turnClockwise()
        if keys[pg.K_e] and keys[pg.K_e] != self.previous_keys[pg.K_e]:
            self.held_shape.mirror()
        if keys[pg.K_p] and keys[pg.K_p] != self.previous_keys[pg.K_p]:
            brutforce.launch_brutforce(self)
        if keys[pg.K_t] and keys[pg.K_t] != self.previous_keys[pg.K_t]:
            # Probleme 1 : 
            #   Pygame a pas l'air de kiffer le thread
            #   Solution possible : faire en sorte que l'algo tourne sans l'interface et retourne les résultats pour ensuite les afficher
            #   Peut etre faire quelque chose pour pouvoir choisir entre voir l'algo qui résoud en temps réel et juste voir les solutions
            t = threading.Thread(target=self.launch_thread, args=(self.Colors.BLUE,), daemon=True)
            t.start()

        for button in self.buttons:
            button.update()

        self.previous_keys = keys

    def draw(self) -> None:
        """
        Called once every frame
        """
        self.screen.fill(self.bkg_color)
        self.draw_shapes()
        self.draw_preview()
        self.draw_grid()
        for but in self.buttons:
            but.draw()

        if self.game_finished:
            self.drawWinScreen()
        pg.display.flip() 
        pg.display.update()

    def draw_shapes(self) -> None:
        x,y = 0,0
        for ligne in self.board:
            for case in ligne:
                if case != 0:
                    self.draw_square(case,x,y)
                x += self.SQUARE_SIZE
            x = 0
            y += self.SQUARE_SIZE

    def draw_grid(self) -> None:
        #Draws horizontal lines
        for y in range(len(self.board)):
            pg.draw.line(self.screen, Interface.Colors.BLACK, (self.GRID_OFFSET[0], y*self.SQUARE_SIZE +self.GRID_OFFSET[1]), (self.WIN_WIDTH + self.GRID_OFFSET[0], y*self.SQUARE_SIZE + self.GRID_OFFSET[1]))

        # Draws vertical lines
        for x in range(len(self.board[0])):
            pg.draw.line(self.screen, Interface.Colors.BLACK, (x * self.SQUARE_SIZE , self.GRID_OFFSET[1]), (x * self.SQUARE_SIZE, self.WIN_WIDTH))

    def draw_square(self, squareID:int, x:int, y:int) -> None:
        square = pg.Rect(x + self.GRID_OFFSET[0], y + self.GRID_OFFSET[1], self.SQUARE_SIZE, self.SQUARE_SIZE)
        pg.draw.rect(self.screen, Interface.Colors.getColorFromID2(squareID), square)

    def draw_preview(self) -> None:
        if not self.isMouseInGrid():
            return
        # Create a surface to enable alpha channe²
        sur = pg.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
        sur.set_alpha(64)
        for shapeX in range(len(self.held_shape.piece)):
            for shapeY in range(len(self.held_shape.piece[shapeX])):
                if self.held_shape.piece[shapeX][shapeY] != 0 :
                    shape_color = Interface.Colors.getColorFromID2(self.held_shape_id)
                    pg.draw.rect(sur, shape_color,pg.Rect(0, 0, self.SQUARE_SIZE, self.SQUARE_SIZE))
                    self.screen.blit(sur, (
                                            (self.pos_rectified[1]+shapeY) * self.SQUARE_SIZE + self.GRID_OFFSET[0],
                                            (self.pos_rectified[0]+shapeX) * self.SQUARE_SIZE + self.GRID_OFFSET[1]
                                        )
                    )


    def rectify_mouse_position(self) -> tuple[int,int]:
        """
        Transforms the mouse position into something that makes it easy to index into the grid
        """
        mouse_pos = pg.mouse.get_pos()
        rectified = int((mouse_pos[1] - self.GRID_OFFSET[1])/ self.SQUARE_SIZE), int((mouse_pos[0] - self.GRID_OFFSET[0])/ self.SQUARE_SIZE)
        return rectified

    def inc_shape_ID(self) -> None:
        if self.held_shape_id < 12:
            self.held_shape_id += 1
        else:
            self.held_shape_id = 1
        while self.held_shape_id in self.board.used_shapes:
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
        while self.held_shape_id in self.board.used_shapes:
            if self.held_shape_id > 1:
                self.held_shape_id -= 1
            else:
                self.held_shape_id = 12
        self.held_shape = Piece(self.held_shape_id)

    def remove_shape(self, id:int) -> None:
        """
        Removes a shape from the board given its ID
        """
        if id in self.board.used_shapes:
            self.board.used_shapes.remove(id)
            for x in range(len(self.board)):
                for y in range(len(self.board[x])):
                    if self.board[x][y] == id:
                        self.board[x][y] = 0
    
    def quit(self):
        self.isRunning = False

    def isMouseInGrid(self) -> bool:
        grid_rect = pg.Rect(self.GRID_OFFSET, (self.WIN_WIDTH, self.WIN_HEIGHT))
        return grid_rect.collidepoint(self.mouse_pos)
    
    def drawWinScreen(self) -> None:
        winRect = pg.Rect(self.WIN_WIDTH//4, self.WIN_HEIGHT//4, self.WIN_WIDTH//2, self.WIN_HEIGHT//2)
        winRectBorder = pg.Rect(winRect.left-1, winRect.top-1, winRect.width+2, winRect.height+2)
        pg.draw.rect(self.screen, self.Colors.WHITE, winRectBorder)
        pg.draw.rect(self.screen, self.Colors.BLACK, winRect)

        # Draws the text
        text = pg.font.SysFont("verdana.ttf", 48)
        text_draw = text.render("The game is finished !", True, self.Colors.WHITE)
        text_draw_rect = text_draw.get_rect()
        text_draw_rect.center = winRect.center
        self.screen.blit(text_draw, text_draw_rect)

    def launch_thread(self, c):
        print("Tesst")
        time.sleep(2)
        print("Tesst")
        


if __name__ == "__main__":
    pg.init()
    inte = Interface()
    pg.time.Clock().tick(60)
    while inte.isRunning:
        inte.update_events()
        inte.draw()