import pygame as pg

class Spritesheet:
 
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    
    def get_image(self,x,y,width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        return image

def format_time(delayed_time):
        minutes = delayed_time // 60
        seconds = delayed_time % 60
        
        if minutes < 10:
            minutes_str = f"0{minutes}"
        else:
            minutes_str = str(minutes)
        
        if seconds < 10:
            seconds_str = f"0{seconds}"
        else:
            seconds_str = str(seconds)
        if minutes > 0:
            return f"{seconds_str}:{minutes_str}"
        else:
            return f"{seconds_str}:00"