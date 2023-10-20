import pygame as pg
from pygame import gfxdraw as gfx
from jeu import *

# TODO:
# Ameliorer les graphismes


class Interface:

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
                color = Interface.Colors.BLACK
            else:
                color = None

            return color


    def __init__(self, height = 5, width = 11) -> None:
    
        # Used to make sure when a key is held down that we only press it once
        self.previous_keys = []
        self.pos_rectified = (0,0)
        # By default select the first shape
        self.held_shape_id = 1
        self.held_shape = Piece(self.held_shape_id)

        self.board = Board(height, width)

        # Creates the pygame window
        self.bkg_color = Interface.Colors.DARK_GREY
        self.WIN_WIDTH = width * self.SQUARE_SIZE
        self.WIN_HEIGHT = height * self.SQUARE_SIZE
        self.screen = pg.display.set_mode((self.WIN_WIDTH , self.WIN_HEIGHT))
        pg.display.set_caption(self.TITLE)

        self.isRunning = True

    def update(self) -> None:
        """
        Called once every frame
        """
        self.screen.fill(self.bkg_color)
        x,y = 0,0
        
        for ligne in self.board:
            for case in ligne:
                if case != 0:
                    self.drawSquare(case,x,y)
                x += self.SQUARE_SIZE
            x = 0
            y += self.SQUARE_SIZE

        self.drawPreview()
        self.drawGrid()
        pg.display.flip() 
        pg.display.update()

    def drawGrid(self) -> None:
        #Draws horizontal lines
        for y in range(len(self.board)):
            pg.draw.line(self.screen, Interface.Colors.BLACK, (0, y*self.SQUARE_SIZE), (self.WIN_WIDTH, y*self.SQUARE_SIZE))

        # Draws vertical lines
        for x in range(len(self.board[0])):
            pg.draw.line(self.screen, Interface.Colors.BLACK, (x * self.SQUARE_SIZE, 0), (x * self.SQUARE_SIZE, self.WIN_WIDTH))

    def drawSquare(self, squareID:int, x:int, y:int) -> None:
        # radius = 40
        # # Draw the disk representing one part of a shape
        # gfx.aacircle(self.screen, int(x+self.SQUARE_SIZE/2), int(y+self.SQUARE_SIZE/2), radius, Interface.Colors.getColorFromID(squareID))
        # gfx.filled_circle(self.screen, int(x+self.SQUARE_SIZE/2), int(y+self.SQUARE_SIZE/2), radius, Interface.Colors.getColorFromID(squareID))
        pg.draw.rect(self.screen, Interface.Colors.getColorFromID2(squareID), pg.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def drawPreview(self) -> None:
        # Create a surface to enable alpha channel
        s = pg.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
        s.set_alpha(64)
        for shapeX in range(len(self.held_shape.piece)):
            for shapeY in range(len(self.held_shape.piece[shapeX])):
                if self.held_shape.piece[shapeX][shapeY] != 0 :
                    c = Interface.Colors.getColorFromID(self.held_shape_id)
                    pg.draw.rect(s, (*c, 10),pg.Rect(0, 0, self.SQUARE_SIZE, self.SQUARE_SIZE))
                    self.screen.blit(s, (
                                        (self.pos_rectified[1]+shapeY) * self.SQUARE_SIZE,
                                        (self.pos_rectified[0]+shapeX) * self.SQUARE_SIZE
                                        )
                    )

    def events(self) -> None:
        """
        Call events() before update()
        """
        self.mousePos = pg.mouse.get_pos()
        self.pos_rectified = int(self.mousePos[1] / self.SQUARE_SIZE), int(self.mousePos[0] / self.SQUARE_SIZE)
        keys = pg.key.get_pressed()
        for event in pg.event.get():        
            if event.type == pg.QUIT: 
                self.isRunning = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_LEFT:
                    self.board.placeShape(self.held_shape, self.pos_rectified)
                if event.button == pg.BUTTON_RIGHT:
                    id = self.board[self.pos_rectified[0]][self.pos_rectified[1]]
                    self.removeShape(id)

        if keys[pg.K_ESCAPE] :
            self.isRunning = False
        if keys[pg.K_LEFT] and keys[pg.K_LEFT] != self.previous_keys[pg.K_LEFT]:
            self.changeShapeID("+")
        if keys[pg.K_RIGHT] and  keys[pg.K_RIGHT] != self.previous_keys[pg.K_RIGHT]:
            self.changeShapeID("-")
        if keys[pg.K_r] and keys[pg.K_r] != self.previous_keys[pg.K_r]:
            self.held_shape.turnClockwise()
        if keys[pg.K_e] and keys[pg.K_e] != self.previous_keys[pg.K_e]:
            self.held_shape.mirror()

        self.previous_keys = keys

    def changeShapeID(self, mode:str) -> None:
        """
        Changes the ID of the shape currently in the players hand
        Does checking to make sure the ID does go higher than the number of shapes present in the game
        """
        if mode == "+" and self.held_shape_id < 12:
            self.held_shape_id += 1
        elif mode == "-" and self.held_shape_id > 1:
            self.held_shape_id -= 1
        elif mode == "+" and self.held_shape_id == 12:
            self.held_shape_id = 1
        elif mode == "-" and self.held_shape_id == 1:
            self.held_shape_id = 12
        else:
            self.held_shape_id = 1

        self.held_shape = Piece(self.held_shape_id)

    def removeShape(self, id:int) -> None:
        """
        Removes a shape from the board given its ID
        """
        if id in self.board.used_shapes:
            self.board.used_shapes.remove(id)
            for x in range(len(self.board)):
                for y in range(len(self.board[x])):
                    if self.board[x][y] == id:
                        self.board[x][y] = 0





if __name__ == "__main__":
    pg.init()
    inte = Interface()
    pg.time.Clock().tick(60)
    while inte.isRunning:
        inte.events()
        inte.update()