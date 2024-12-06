import sys
import pygame
from PyQt6.QtWidgets import QApplication

from player import Player

class Main():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
        self.done = False
        self.initUI()

    def initUI(self):
        while not self.done:
            for event in pygame.event.get():
                # Поле
                self.field = pygame.image.load('hockey_field.jpg').convert_alpha()
                self.screen.blit(self.field, (0, 0))
                # Игроки
                a1, a2, a3, a4, a5,  = Player(self, 0, 5), Player(self, 5, 5), Player(self, 15, 5), \
                    Player(self, 25, 5), Player(self, 35, 5)
                goalkeeper1, goalkeeper2 = Player(self, 45, 5), Player(self, 45, 800)
                b1, b2, b3, b4, b5 = Player(self, 5, 800), Player(self, 15, 800), Player(self, 25, 800), \
                    Player(self, 35, 800), Player(self, 45, 800)

                if event.type == pygame.QUIT:
                    self.done = True
                pygame.display.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
