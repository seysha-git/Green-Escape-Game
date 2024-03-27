import pygame as pg
from settings import *
import random as rd
from utils import *

class BaseSprite(pg.sprite.Sprite):
    def __init__(self, game, groups):
        self.groups = groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

class PlatItem(BaseSprite):
    def __init__(self, game, plat):
        groups = game.all_sprites, game.boosters
        super().__init__(game, groups)
        self._layer = POW_LAYER
        self.plat = plat
        self.image = self.game.spritesheet_items.get_image(72, 219, 70, 70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top

    def update(self):
        self.rect.centerx = self.plat.rect.centerx

class Checkpoint(BaseSprite):
    def __init__(self, game, x, y, type):
        groups = game.all_sprites, game.check_points
        super().__init__(game, groups)
        self.image = self.game.spritesheet_items.get_image(504, 288, 70, 70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

class Key(BaseSprite):
    def __init__(self, game, x, y):
        groups = game.all_sprites, game.keys
        super().__init__(game, groups)
        self.image = self.game.spritesheet_items.get_image(72, 363, 70, 70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spike(BaseSprite):
    def __init__(self, game, x, y, type, time):
        groups = game.all_sprites, game.spikes
        super().__init__(game, groups)
        if type == 0:
            self.images = [
                self.game.spritesheet_items.get_image(347, 0, 70, 70),
                self.game.spritesheet_items.get_image(0, 0, 0, 0)
            ]
        elif type == 1:
            self.images = [
                pg.transform.rotate(self.game.spritesheet_items.get_image(347, 0, 70, 70), 180),
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
        now = pg.time.get_ticks()
        time_since_last_toggle = now - self.last_toggle_time

        # If 2 seconds have passed since the last toggle
        if time_since_last_toggle >= self.toggle_time:
            self.toggle_spike()  # Toggle the spike
            self.last_toggle_time = now  # Update the last toggle time

    def toggle_spike(self):
        self.index = 1 - self.index
        self.image = self.images[self.index]
        self.image.set_colorkey("black")





class PlatItem(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.boosters
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.image = self.game.spritesheet_items.get_image(72,219,70,70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top
    def update(self):
        self.rect.centerx = self.plat.rect.centerx

class Checkpoint(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.check_points
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.image = self.game.spritesheet_items.get_image(504,288,70,70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Key(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.keys
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet_items.get_image(72,363,70,70)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spike(pg.sprite.Sprite):
    def __init__(self, game, x, y, type, time):
        self.groups = game.all_sprites, game.spikes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if type == 0:
            self.images = [
                self.game.spritesheet_items.get_image(347, 0, 70, 70),
                self.game.spritesheet_items.get_image(0, 0, 0, 0)
            ]
        elif type == 1:
            self.images = [
                pg.transform.rotate(self.game.spritesheet_items.get_image(347, 0, 70, 70), 180),
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
        now = pg.time.get_ticks()
        time_since_last_toggle = now - self.last_toggle_time

        # If 2 seconds have passed since the last toggle
        if time_since_last_toggle >= self.toggle_time:
            self.toggle_spike()  # Toggle the spike
            self.last_toggle_time = now  # Update the last toggle time

    def toggle_spike(self):
        self.index = 1 - self.index
        self.image = self.images[self.index]
        self.image.set_colorkey("black")

