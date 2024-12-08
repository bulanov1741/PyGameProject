import sys
import pygame
from PyQt6.QtWidgets import QApplication

from player import Player


class Main():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
        self.running = True
        self.location_washer = 1 # 0 - ни у кого, 1 - у своей команды, 2 - у чужой команды
        # Игроки
        self.a1, self.a2, self.a3, self.a4, self.a5 = Player(self, 0, 5), Player(self, 5, 5), Player(self, 15, 5), \
            Player(self, 25, 5), Player(self, 35, 5)
        self.goalkeeper1, self.goalkeeper2 = Player(self, 45, 5), Player(self, 45, 800)
        self.b1, self.b2, self.b3, self.b4, self.b5 = Player(self, 5, 800), Player(self, 15, 800), Player(self, 25,
                                                                                                          800), \
            Player(self, 35, 800), Player(self, 45, 800)
        self.players = [self.a1, self.a2, self.a3, self.a4, self.a5, self.b1, self.b2, self.b3, self.b4, self.b5,
                        self.goalkeeper1, self.goalkeeper2]

        self.initUI()

    def initUI(self):
        while self.running:
            for event in pygame.event.get():
                # Поле
                self.field = pygame.image.load('hockey_field.jpg').convert_alpha()
                self.screen.blit(self.field, (0, 0))
                # Расставляем игроков на поле
                for i in self.players:
                    i.show()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.location_washer == 1:
                        self.a1.broadcast(event)

                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec())
