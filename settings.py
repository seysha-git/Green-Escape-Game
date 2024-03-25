import pygame as pg
import os
pg.init()

#Game settings
WIN_WIDTH = 1500
WIN_HEIGHT = 900
FPS = 60

#fonts settings
SCROLLING_TEXT_FONT = pg.font.Font("freesansbold.ttf", 24)
MENU_FONT = pg.font.Font("freesansbold.ttf", 24)
TITLE = "WW2 Story gmae"
FONT_NAME = 'arial'


#Spritesheet directories
SPRITESHEET_CHAR = "p1_spritesheet.png"
SPRITESHEET_PLATFORM = "tiles_spritesheet.png"
SPRITESHEET_ITEMS = "items_spritesheet.png"
SPRITESHEET_ENEMIES = "enemies_spritesheet.png"
SPRITESHEET_HUD = "hud_spritesheet.png"
SPRITESHEET_PRINCESS = "p3_spritesheet.png"
TS_FILE = "topscores.txt"

#Character z-index layering
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
ENEMIES_LAYER = 2

#Player properaties
MAIN_CHAR_COLOR = "white"
MAIN_ACC = 5
MAIN_FRICTION = 0.12
MAIN_GRAVITY = 0.8
MAIN_JUMP_VEL = 15



#Character siing properties
BULLET_WIDTH, BULLET_HEIGHT = 20,20
MAIN_CHAR_WIDTH, MAIN_CHAR_HEIGHT = 50,100










































































































