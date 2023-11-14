import pygame as pg

class Button:

    CENTERED = -1

    def __init__(self, pos:tuple[int,int],
                 size:tuple[int,int],
                 surface:pg.Surface,
                 bg_color = (0,0,0),
                 text:str = None,
                 text_color = (255,255,255),
                 border_color = (255,255,255),
                 border_size:int = 1,
                 font:str = "Verdana.ttf",
                 font_size:int = 24,
                 font_alliasing:bool = True,
                 callback = None,
                 callbak_args = ()):
        
        self.size = size
        self.surface = surface
        self.bg_color = bg_color
        self.text = text
        self.text_color = text_color
        self.border_color = border_color
        self.border_size = border_size
        self.callback = callback

        if (pos[0] == self.CENTERED):
            pos = (self.surface.get_width()//2-size[0]//2, pos[1])
        if (pos[1] == self.CENTERED):
            pos = (pos[0], self.surface.get_height()//2-size[1]/2)

        self.rect = pg.Rect(pos, size)
        self.border = pg.Rect((pos[0]-border_size,pos[1]-border_size), (size[0]+border_size, size[1]+border_size))
        self.font = pg.font.SysFont(font, font_size)
        self.is_drawn = False
        self.font_alliasing = font_alliasing
        self.pos = pos
        self.prev_state = False
        self.callback_args = callbak_args

    def draw(self) -> None:
        # Draws the button border    
        if self.border_color != None:
            border_draw = pg.Surface((self.size[0]+self.border_size*2, self.size[1]+self.border_size*2))
            border_draw.fill(self.border_color)
            self.surface.blit(border_draw, (self.pos[0]-self.border_size, self.pos[1]-self.border_size))

        # Draws the button
        button_draw = pg.Surface(self.size)
        button_draw.fill(self.bg_color)
        self.surface.blit(button_draw, self.pos)

        # Draws the button text
        if self.text != None:
            text_draw = self.font.render(self.text, self.font_alliasing, self.text_color)
            text_draw_rect = text_draw.get_rect()
            text_draw_rect.center = self.rect.center
            self.surface.blit(text_draw, text_draw_rect)
    
    def update(self, surface) -> None:
        
        if (pg.mouse.get_pressed()[0] and self.isHovered() and not self.prev_state):
            self.onClick()
        self.prev_state = pg.mouse.get_pressed()[0]

    def isHovered(self) -> bool:
        return self.rect.collidepoint(pg.mouse.get_pos())

    def onClick(self) -> None:
        if self.callback != None:
            self.callback(*self.callback_args)
            self.prev_state = True

    def changePos(self, pos:tuple[int, int]):
        self.pos = pos