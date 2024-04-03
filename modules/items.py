import pygame as pg
from settings import *
import random as rd
from utils import *

class ItemSprite(pg.sprite.Sprite):
    """
    Class responsible for BaseItem:
        -items layering
    
    """
    def __init__(self, game, groups):
        self._layer = POW_LAYER
        self.groups = groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

class PlatItem(ItemSprite):
    """
    Class responsible for PlatItem:
        description: its the mushrooms on the platforms
        -update() make sure they update with moving platforms also

    
    """
    def __init__(self, game, plat):
        groups = game.all_sprites, game.boosters
        super().__init__(game, groups)
        self.plat = plat
        self.image = self.game.spritesheet_items.get_image(72, 219, 70, 70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top

    def update(self):
        self.rect.centerx = self.plat.rect.centerx

class Checkpoint(ItemSprite):
    """
    Class responsible for Checkpoint:
        -added to the check_points group
    
    """
    def __init__(self, game, x, y, type):
        groups = game.all_sprites, game.check_points
        super().__init__(game, groups)
        self.image = self.game.spritesheet_items.get_image(504, 288, 70, 70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

class Key(ItemSprite):
    """
    Class responsible for Key:
        -added to the keys group
    
    """
    def __init__(self, game, x, y):
        groups = game.all_sprites, game.keys
        super().__init__(game, groups)
        self.image = self.game.spritesheet_items.get_image(72, 363, 70, 70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spike(ItemSprite):
    """
    Class responsible for Spike:
        -animated mouvment
        -seperate group: spikes
        - 
    
    """
    def __init__(self, game, x, y, type, time):
        groups = game.all_sprites, game.spikes
        super().__init__(game, groups)
        if type == 0:
            self.images = [
                self.game.spritesheet_items.get_image(347, 0, 45, 70),
                self.game.spritesheet_items.get_image(0, 0, 0, 0)
            ]
        elif type == 1:
            self.images = [
                pg.transform.rotate(self.game.spritesheet_items.get_image(347, 0, 45, 70), 180),
                self.game.spritesheet_items.get_image(0, 0, 0, 0),
            ]
        self.index = 0
        self.type = type
        self.image = self.images[self.index]
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_toggle_time = time
        self.toggle_time = rd.randint(800,1000)

    def update(self):
        if self.game.game_ground.spawn_spikes:
            now = pg.time.get_ticks()
            time_since_last_toggle = now - self.last_toggle_time

            if time_since_last_toggle >= self.toggle_time:
                self.toggle_spike()  
                self.last_toggle_time = now  

    def toggle_spike(self):
        if self.index == 1:
            self.game.spikes_sound.play()
        self.index = 1 - self.index
        self.image = self.images[self.index]
        self.image.set_colorkey("black")

