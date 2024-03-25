import pygame as pg, sys
from settings import *

class Button:
    def __init__(self, screen, text, width, height, pos, color="#475F77"):
        self.pressed = False
        self.top_rect = pg.Rect(pos, (width, height))
        self.top_color = color
        self.screen = screen
        self.text = text

        self.text_surf = MENU_FONT.render(self.text, True, "white")
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
    def draw(self):
        pg.draw.rect(self.screen, self.top_color, self.top_rect, border_radius= 12)
        self.screen.blit(self.text_surf, self.text_rect)
        
    def check_click(self):
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            
            self.top_color = "red"
            if pg.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    print("click")
                    self.pressed = False
        else:
            self.top_color = "#475F77"        



