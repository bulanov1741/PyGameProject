
import sys
import pygame
import screeninfo as screeninfo
from PyQt6.QtWidgets import QApplication
from menu import Menu
from Game import Game
from DataManager import GameDataManager
import time

class Main():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Hockey")
        self.width_m = screeninfo.get_monitors()[0].width
        self.height_m = screeninfo.get_monitors()[0].height
        self.size = (self.width_m, self.height_m)
        self.screen_total_game = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.running = True
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000

        self.status = 0 # 0 - main menu, 1 - game
        self.level = 1
        self.DataManager = GameDataManager()
        self.init_music_sections() # для оптимизации загрузки
        self.initUI()


    def initUI(self):
        while self.running:
            self.clock.tick(60)
            self.exit_detect()
            if self.status == 0:
                menu = Menu(*self.size, self.screen_total_game, self.dt, self.DataManager, self.menu_sound_path)
                self.level = menu.check_level()
                self.status = 1
            elif self.status == 1:
                if self.level == 1:
                    Game(*self.size, self.screen_total_game, self.dt, 0)
                elif self.level == 2: # либо дублировать Game с чуть переписанным кодом, либо переписать Game в универсальный класс для всех уровней
                    Game(*self.size, self.screen_total_game, self.dt, 1)
                self.status = 0
            self.screen_total_game.fill((0, 0, 0))
            pygame.display.flip()

    def render_logo(self): # Из-за долгой работы sqlite можно отобразить лого и прочее. статус: не реализовано.
        font = pygame.font.Font(None, 90)
        text = font.render("Loading", True, (255, 255, 255))
        self.screen_total_game.blit(text, (self.width_m // 2 - 100, self.height_m // 2))
        pygame.display.flip()


    def init_music_sections(self): # предзагрузка всех объектов музыки пайгейма для каждого игрвого окна
        self.render_logo()
        self.menu_sound_path = self.DataManager.load_sound("menu")

    def exit_detect(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec())
