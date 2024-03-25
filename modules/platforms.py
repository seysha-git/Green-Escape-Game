import pygame as pg
from settings import *
from utils import *
from modules.items import Spike
import random as rd

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x,y, type="ground"):
        self._layer = PLATFORM_LAYER
        self.type = type
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet_platform.get_image(792, 0,70,70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class GroundPlatform(Platform):
    def __init__(self, game, x,y, type="ground"):
        super().__init__(game, x,y,type)
        self.groups = game.all_sprites, game.ground_platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images = {
             "ground": self.game.spritesheet_platform.get_image(648,0,70,70),
             "half_ground": self.game.spritesheet_platform.get_image(576,432,70,70),
             "lava": self.game.spritesheet_platform.get_image(504, 0,70,30),
             "half_up_left": self.game.spritesheet_platform.get_image(576,144,70,70), 
        }
        self.image = self.images[type]
        self.image.set_colorkey("black")
        #self.mask = pg.mask.from_surface(self.image)

class BackgroundBlocks(Platform):
    def __init__(self, game,x,y, type=""):
        super().__init__(game, x,y,type)
        self.groups = game.all_sprites, game.background_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images = {
             "door_open_mid": self.game.spritesheet_platform.get_image(648, 288,70,70),
             "door_open_top": self.game.spritesheet_platform.get_image(648, 216,70,70),
             "cloud": self.game.spritesheet_items.get_image(0, 146,128,71), 
             "water": self.game.spritesheet_platform.get_image(504, 216,70,70),
             "flag_green":self.game.spritesheet_items.get_image(216,432,70,70), 
             "tresure": self.game.spritesheet_huds.get_image(146,147,44,40), 
             "star": self.game.spritesheet_items.get_image(504,288,70,70), 
             "stairs": self.game.spritesheet_platform.get_image(648,144,70,70), 
             "rope": self.game.spritesheet_platform.get_image(360,864,70,70), 
             "umbrella_shield": pg.transform.scale(pg.image.load("./images/umbrellaOpen.png").convert_alpha(), (120,160)),
        }
        self.image = self.images[type]
        self.image.set_colorkey("black") 

class WallPlatform(Platform):
    def __init__(self, game,x,y, type="wall"):
        super().__init__(game, x,y)
        self.type = type
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.spritesheet_platform.get_image(0,432,70,70)
        self.image.set_colorkey("black")
class RoofPlatform(Platform):
    def __init__(self, game,x,y):
        super().__init__(game, x,y)
        self.groups = game.all_sprites, game.roofs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.spritesheet_platform.get_image(0,432,70,70)
        self.image.set_colorkey("black")
        

class JumpPlatform(Platform):
    def __init__(self, game, x,y):
        super().__init__(game, x,y)
        self.groups = game.all_sprites, game.jump_platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.spritesheet_platform.get_image(720,432,70,70)
        self.image.set_colorkey("black")


class MovingJumpPlatform(JumpPlatform):
    def __init__(self, game, x, y, time, start_dir):
        super().__init__(game, x, y)
        self.time = time
        self.toggle_time_interval = 500
        self.direction = start_dir
    def update(self):
        now = pg.time.get_ticks()
        time_since_last_toggle = now - self.time
        self.rect.x += self.direction
        if time_since_last_toggle >= self.toggle_time_interval:
            self.direction *= -1
            self.time = now



                
        
        




