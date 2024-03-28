import pygame as pg
import sys
from settings import *
from modules.characters import *
from modules.guide_items import *
from os import path
from game_ground import GameGround
pg.font.init()
from utils import *
import pandas as pd



class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.font_name = pg.font.match_font(FONT_NAME)
        self.clock = pg.time.Clock()
        self.running = True
        self.completed = False
        self.player_dead = False
        self.load_game_data()
        self.game_ground = GameGround(self)
        self.time_played = 0
        self.last_game_ended = 0
    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()

        self.ground_platforms = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.roofs = pg.sprite.Group()
        self.jump_platforms = pg.sprite.Group()
        self.background_sprites = pg.sprite.Group()
        self.player_bullets = pg.sprite.Group()
        self.course_bullets = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.logos =pg.sprite.Group()
        
        self.keys = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.boosters = pg.sprite.Group()
        
        self.grounds = pg.sprite.Group()
        self.check_points = pg.sprite.Group()
        self.enemies = pg.sprite.Group()

        self.game_ground.new()
        pg.mixer.music.load(path.join(self.snd_dir, "part3.ogg"))
        self.run()
    def load_game_data(self):
        self.dir = path.dirname(__file__)
        try:
            self.game_data = pd.read_csv("game_data.csv")
        except FileNotFoundError:
            self.game_data = pd.DataFrame({
                "best_time": [0],  
                "best_aim": [0],
                "best_health": [0],
            })
            self.game_data.to_csv("game_data.csv")

        img_dir = path.join(self.dir, "images")
        self.spritesheet_char = Spritesheet(path.join(img_dir, SPRITESHEET_CHAR))
        self.spritesheet_platform = Spritesheet(path.join(img_dir, SPRITESHEET_PLATFORM))
        self.spritesheet_items = Spritesheet(path.join(img_dir, SPRITESHEET_ITEMS))
        self.spritesheet_enemies = Spritesheet(path.join(img_dir, SPRITESHEET_ENEMIES))
        self.spritesheet_huds = Spritesheet(path.join(img_dir, SPRITESHEET_HUD))
        self.spritesheet_princess = Spritesheet(path.join(img_dir, SPRITESHEET_PRINCESS))
        
        self.get_sounds_data()
        self.level_guide()
    def get_sounds_data(self):
        self.snd_dir = path.join(self.dir, "sounds")
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, "Jump33.wav"))
        self.gems_sound = pg.mixer.Sound(path.join(self.snd_dir, "boost.wav"))
        self.lost_game = pg.mixer.Sound(path.join(self.snd_dir, "Jingle_Lose_00.mp3"))
        self.won_game = pg.mixer.Sound(path.join(self.snd_dir, "Jingle_Win_00.mp3"))
        self.spikes_sound = pg.mixer.Sound(path.join(self.snd_dir, "Trap_00.mp3"))
        self.you_lose_sound = pg.mixer.Sound(path.join(self.snd_dir, "you_lose.ogg"))
        self.you_win_sound = pg.mixer.Sound(path.join(self.snd_dir, "you_win.ogg"))
        self.shoot_sound = pg.mixer.Sound(path.join(self.snd_dir, "rlaunch.wav"))
        self.enemies_hit_sound = pg.mixer.Sound(path.join(self.snd_dir, "zombie-6.wav"))
        self.check_points_sound = pg.mixer.Sound(path.join(self.snd_dir, "power_up.ogg"))
        self.sound_1 = pg.mixer.Sound(path.join(self.snd_dir, "1.ogg"))
        self.sound_2 = pg.mixer.Sound(path.join(self.snd_dir, "2.ogg"))
        self.sound_3 = pg.mixer.Sound(path.join(self.snd_dir, "3.ogg"))
    def update_game_data(self, column_name, new_value):
        self.game_data[column_name] = new_value
        self.game_data.to_csv("game_data.csv", index=True)
    def level_guide(self):
        self.scrolling_text_font = pg.font.Font("freesansbold.ttf", 20)
        self.levels_messages = [ 
            "Følg stjernene og kom deg til døren",
            "Unngå bombene. Dukk under paraply for beskyttelse",
            "This is CP nr 3"
        ]
        self.guide_rect = pg.Rect(WIN_WIDTH//2-200, 80,600,100)
        self.active_message = 0
        self.message = self.levels_messages[self.active_message]
        self.snip_guide = self.scrolling_text_font.render(self.message, True, 'white')
        self.counter = 9
        self.speed = 4
        self.all_message_completed = False
        self.done = False
    def animated_message(self):
        if self.active_message < len(self.levels_messages):
            if self.counter < self.speed * len(self.message):
                self.counter += 1
            elif self.counter >= self.speed* len(self.message):
                self.done = True
        self.snip_guide = self.scrolling_text_font.render(self.message[0:self.counter//self.speed], True, "white")
    def draw_guide_message(self):
        if not self.all_message_completed:
            pg.draw.rect(self.screen, "#475F77", self.guide_rect, border_radius= 12)
            self.screen.blit(self.snip_guide, (self.guide_rect.x + 10, self.guide_rect.y + 40))
    def create_new_message(self):
        if self.active_message < len(self.levels_messages) -1:
            self.active_message += 1
            self.done = False
            self.all_message_completed = False
            self.message = self.levels_messages[self.active_message]
            self.counter = 0
        else:
            return
    def run(self):
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.5)
        self.playing = True
        while self.playing:
            self.animated_message()
            self.clock.tick(FPS)
            self.game_ground.events()
            self.update()
            self.draw()
            
        pg.mixer.music.fadeout(500)
    def update(self):
        self.game_ground.update()
        self.all_sprites.update()
        self.update_time()
    def update_time(self):
        self.now = pg.time.get_ticks()
        self.delayed_time = (self.now - self.last_game_ended)//1000
    def reset_timer(self):
        self.last_game_ended = self.now
    def draw(self):
        self.screen.fill((50, 168, 82))
        self.all_sprites.draw(self.screen)
        self.navbar()
        self.game_ground.player.draw()
        self.draw_guide_message()
        pg.display.update()
    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, "part1.ogg"))
        pg.mixer.music.play(loops=-1)
        self.screen.fill("light green")
        pg.draw.rect(self.screen, "black", (0, 220, WIN_WIDTH, 20))
        pg.draw.rect(self.screen, "black", (0, WIN_HEIGHT-180, WIN_WIDTH, 20))
        self.draw_text("Mitt Platform spill", 100, "white",450,100)
        self.draw_text(f'Beste tid: {self.game_data["best_time"].iloc[0]} sek', 60, "white", 600, 280 )
        self.draw_text("Kontrollene", 50, "white", 640, 400)
        self.w = Button(self.screen, "w", 120, 70, (660,500))
        self.a = Button(self.screen, "a", 120, 70, (660,600))
        self.s = Button(self.screen, "s", 120, 70, (520,600))
        self.d = Button(self.screen, "d", 120, 70, (820,600))

        self.play_button = Button(self.screen, "Spill nå", 200, 60, (500,800), "green")
        self.play_button.draw()
        self.quit_button = Button(self.screen, "Avslutt", 200, 60, (720, 800))
        self.quit_button.draw()
        self.w.draw()
        self.a.draw()
        self.s.draw()
        self.d.draw()
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
    def show_over_screen(self):
        
        self.screen.fill("dark grey")

        self.play_button = Button(self.screen, "Spill igjen", 200, 50, (520, 800))
        self.quit_button = Button(self.screen, "Avslutt", 200, 50, (780, 800))
        self.play_button.draw()
        self.quit_button.draw()
        if self.running:
            if self.completed:
                self.won_game.play()
                self.you_win_sound.play()
                self.title = "Bra Jobba!"
                pg.draw.rect(self.screen, "light blue", (460, 290, 620, 400), 0, 5)
                self.handle_completed_game()
                self.reset_timer()
            elif self.player_dead:
                self.lost_game.play()
                self.title = "Du døde"
                pg.draw.rect(self.screen, "black", (460, 290, 620, 400), 0, 5)
                self.draw_text(f"Godt forsøk, prøv igjen :)", 50, "white", 460, 500)
                self.reset_timer()
                self.you_lose_sound.play()
            self.draw_text(f"{self.title}", 120, "white", 570, 80)

            if self.completed:
                self.display_game_statistics()
            pg.draw.rect(self.screen, "black", (0, 220, WIN_WIDTH, 20))
            pg.draw.rect(self.screen, "black", (0, WIN_HEIGHT - 180, WIN_WIDTH, 20))

            pg.display.flip()
            self.wait_for_key()
    def handle_completed_game(self):
        hit_ratio = self.game_ground.player.get_hit_ratio()
        health = self.game_ground.player.health

        self.update_best_records(hit_ratio, health)

        self.draw_text("Statistikk", 50, "white", 460 + 220, 320)
        self.draw_text(f"Beste tid: {self.game_data['best_time'].iloc[0]}          Din tid: {self.delayed_time}", 30,
                    "white", 460 + 100, 400)
        self.draw_text(f"Best aim:  {self.game_data['best_aim'].iloc[0]}%          Ditt aim : {hit_ratio}%", 30,
                    "white", 460 + 100, 460)
        self.draw_text(f"Mest liv: {self.game_data['best_health'].iloc[0]}/100          Ditt liv: {health}/100", 30,
                    "white", 460 + 100, 520)
        #self.draw_text(f"Godt forsøk, prøv igjen :)", 30, "white", 460 + 150, 620)

    def update_best_records(self, hit_ratio, health):
        if self.delayed_time < self.game_data["best_time"].iloc[0] or self.game_data["best_time"].iloc[0] == 0:
            self.update_game_data("best_time", [self.delayed_time])
        if health > self.game_data["best_health"].iloc[0]:
            self.update_game_data("best_health", [health])
        if hit_ratio > self.game_data["best_aim"].iloc[0]:
            self.update_game_data("best_aim", hit_ratio)

    def display_game_statistics(self):
        hit_ratio = self.game_ground.player.get_hit_ratio()
        health = self.game_ground.player.health

        # Display statistics
        self.draw_text("Statistikk", 50, "white", 460 + 220, 320)
        self.draw_text(f"Beste tid: {self.game_data['best_time'].iloc[0]}          Din tid: {self.delayed_time}", 30,
                    "white", 460 + 100, 400)
        self.draw_text(f"Best aim:  {self.game_data['best_aim'].iloc[0]}%          Ditt aim : {hit_ratio}%", 30,
                    "white", 460 + 100, 460)
        self.draw_text(f"Mest liv: {self.game_data['best_health'].iloc[0]}/100          Ditt liv: {health}/100", 30,
                    "white", 460 + 100, 520)
        self.draw_text(f"Godt forsøk, prøv igjen :)", 30, "white", 460 + 150, 620)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(60)
            self.play_button.check_click()
            self.quit_button.check_click()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit() 
            if self.play_button.pressed:
                waiting = False
                self.completed = False
            if self.quit_button.pressed:
                sys.exit()
    def draw_text(self, text:str, size:tuple, color:tuple, x:int, y:int):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.screen.blit(text_surface, text_rect)
    def get_logo(self, type):
        images = {
            "main": self.spritesheet_huds.get_image(55,49,47,47),
            "princess": self.spritesheet_huds.get_image(49,190,47,47),
            "keys": self.spritesheet_huds.get_image(146,147,44,40)
        }
        image = images[type]
        image.set_colorkey("black")
        return image
    def navbar(self):
        navbar_rect = pg.Rect(0,0, WIN_WIDTH, 60)
        pg.draw.rect(self.screen, (77, 219, 115), navbar_rect)
        self.screen.blit(self.get_logo("main"), (30,10))
        self.screen.blit(self.get_logo("princess"), (WIN_WIDTH//2-10, 10))
        for i in range(self.game_ground.player.keys):
            self.screen.blit(self.get_logo("keys"), (100+ 70*i, 10))
        pg.draw.rect(self.screen, "light blue", (WIN_WIDTH-240, 10, 150, 40), 0, 5)
        self.draw_text(f"Tid: {self.format_time(self.delayed_time)}", 30, "white", WIN_WIDTH-220, 12)
    def format_time(self, delayed_time):
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


        
