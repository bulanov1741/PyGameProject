
import sys
import pygame
import screeninfo as screeninfo
from PyQt6.QtWidgets import QApplication
from menu import Menu
from Game import Game
from DataManager import GameDataManager


class Main():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Хоккей")
        self.width_m = screeninfo.get_monitors()[0].width
        self.height_m = screeninfo.get_monitors()[0].height
        self.size = (self.width_m, self.height_m)
        self.screen_total_game = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.load_logo()
        self.running = True
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000

        self.status = 0 # 0 - main menu, 1 - game

        self.DataManager = GameDataManager()

        self.init_music_sections() # для оптимизации загрузки
        self.initUI()


    def initUI(self):
        while self.running:
            self.clock.tick(60)
            self.exit_detect()
            if self.status == 0:
                Menu(*self.size, self.screen_total_game, self.dt, self.DataManager, self.menu_sound_path)
                self.status = 1
            elif self.status == 1:
                Game(*self.size, self.screen_total_game, self.dt)
                self.status = 0
            self.screen_total_game.fill((0, 0, 0))
            pygame.display.flip()

    def load_logo(self): # Из-за долгой работы sqlite можно отобразить лого и прочее. статус: не реализовано.
        font = pygame.font.Font(None, 90)
        text = font.render("LMS", True, (100, 100, 100))
        text_rect = text.get_rect(center=(400, 300))
        self.screen_total_game.blit(text, text_rect)

    def init_music_sections(self): # предзагрузка всех объектов музыки пайгейма для каждого игрвого окна
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
