import sys
from turtledemo import clock

import pygame
from PyQt6.QtWidgets import QApplication
from pygame import K_w, K_d, K_s, K_a

from player import Player
from washer import Washer


class Main():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
        self.running = True
        self.location_washer = 0 # 0 - ни у кого, 1 - у своей команды, 2 - у чужой команды
        self.field = pygame.image.load('hockey_field.jpg').convert_alpha() # Поле
        # Игроки
        self.a1, self.a2, self.a3, self.a4, self.a5 = Player(self, 0, 5), Player(self, 5, 5), Player(self, 15, 5), \
            Player(self, 25, 5), Player(self, 35, 5)
        self.goalkeeper1, self.goalkeeper2 = Player(self, 45, 5), Player(self, 45, 800)
        self.b1, self.b2, self.b3, self.b4, self.b5 = Player(self, 5, 800), Player(self, 15, 800), Player(self, 25,
                                                                                                          800), \
            Player(self, 35, 800), Player(self, 45, 800)
        self.players_own = [self.a1, self.a2, self.a3, self.a4, self.a5, self.goalkeeper1] # наша команда
        self.players_opponent = [self.b1, self.b2, self.b3, self.b4, self.b5, self.goalkeeper2] # команда соперника
        self.chosen_player = self.a1 # Выбранный игрок

        self.washer = Washer(800, 450, 10, (1600, 900), 0, 0)

        self.initUI()

    def initUI(self):
        while self.running:
            for event in pygame.event.get():

                if self.location_washer == 0: # Если она не у игроков, то она летает сама по себе
                    self.washer.move(1)

                if pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_s] or\
                    pygame.key.get_pressed()[K_d]:
                    self.chosen_player.move(self)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.location_washer == 1:
                        self.chosen_player.broadcast(event, self)

                    elif self.location_washer == 2:
                        for i in [self.a1, self.a2, self.a3, self.a4, self.a5]:
                            if i.x + 100 >= event.pos[0] >= i.x and i.y + 100 >= event.pos[1] >= i.y:
                                self.chosen_player = i
                                break

                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.update()


            # Поле
            self.screen.blit(self.field, (0, 0))
            # Расставляем игроков на поле
            for i in self.players_own:
                i.draw()
                if self.location_washer != 1:
                    if (i.x + 98, i.y + 98) <= (self.washer.x, self.washer.y) <= (i.x + 100, i.y + 100):
                        self.location_washer = 1
                        self.chosen_player = i
            for i in self.players_opponent:
                i.draw()
                if self.location_washer < 2:
                    if (i.x, i.y) == (self.washer.x, self.washer.y):
                        self.location_washer = 2

            self.washer.draw(self.screen)
            self.washer.move(1)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec())
