import math
import sys

import pygame
from PyQt6.QtWidgets import QApplication
from pygame import K_w, K_d, K_s, K_a, K_LSHIFT

from player import Player
from washer import Washer


class Main():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
        self.running = True
        self.location_washer = 0  # 0 - ни у кого, 1 - у своей команды, 2 - у чужой команды
        self.field = pygame.image.load('hockey_field.jpg').convert_alpha()  # Поле
        # Игроки
        self.a1, self.a2, self.a3, self.a4, self.a5 = Player(self, 0, 5), Player(self, 5, 5), Player(self, 15, 5), \
            Player(self, 25, 5), Player(self, 35, 5)
        self.goalkeeper1, self.goalkeeper2 = Player(self, 45, 5), Player(self, 45, 800)
        self.b1, self.b2, self.b3, self.b4, self.b5 = Player(self, 5, 800), Player(self, 15, 800), Player(self, 25,
                                                                                                          800), \
            Player(self, 35, 800), Player(self, 45, 800)
        self.players_own = [self.a1, self.a2, self.a3, self.a4, self.a5, self.goalkeeper1]  # наша команда
        self.players_opponent = [self.b1, self.b2, self.b3, self.b4, self.b5, self.goalkeeper2]  # команда соперника
        self.chosen_player = self.a1  # Выбранный игрок

        self.washer = Washer(800, 450, 10, (1600, 900), 0, 0)

        self.clock = pygame.time.Clock()

        self.initUI()

    def initUI(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[
                    K_s] or \
                        pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_LSHIFT]:
                    self.chosen_player.move()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.location_washer == 1:
                            # Передача
                            self.broadcast(self.washer.x - pygame.mouse.get_pos()[0],
                                           self.washer.y - pygame.mouse.get_pos()[
                                               1])  # Дельта x и дельта у

                        elif self.location_washer != 1:
                            for i in self.players_own:
                                if i.x + 100 >= pygame.mouse.get_pos()[0] >= i.x and i.y + 100 >= \
                                        pygame.mouse.get_pos()[1] \
                                        >= i.y:
                                    self.chosen_player = i
                                    break

                    # Удар. Начало
                    elif event.button == 3:
                        x0, y0 = event.pos
                        start_time = pygame.time.get_ticks()  # Время начала удара

                if event.type == pygame.MOUSEBUTTONUP:
                    # Удар. Продолжение
                    if event.button == 3:
                        if self.location_washer == 1:
                            x1, y1 = event.pos
                            current_time = pygame.time.get_ticks()  # Время конца удара
                            self.broadcast(x0 - x1, y0 - y1, v=1000)

                if event.type == pygame.QUIT:
                    self.running = False

            # Поле
            self.screen.blit(self.field, (0, 0))
            # Расставляем игроков на поле
            for i in self.players_own:
                i.draw()
                # Проверка на нахождение шайбы у игрока
                if self.location_washer != 1:
                    if i.x + 98 <= self.washer.x <= i.x + 100 and i.y + 98 <= self.washer.y <= i.y + 100:
                        self.location_washer = 1
                        self.chosen_player = i
            for i in self.players_opponent:
                i.draw()
                if self.location_washer < 2:
                    if (i.x, i.y) == (self.washer.x, self.washer.y):
                        self.location_washer = 2

            if self.location_washer == 0:  # Если она не у игроков, то она летает сама по себе
                self.washer.move(dt)

            self.washer.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

    # Передача / Удар
    def broadcast(self, x, y, v=0):
        try:
            if v == 0:
                v = (
                            x ** 2 + y ** 2) ** 0.5  # расстояние между двумя точками, шайба должна прилететь из одной точки в другую за 1 секунду
            angle = math.atan(x / y)
            if y > 0:
                angle = 1.5 * math.pi - angle
                self.washer.y += 2
            elif y < 0:
                angle = 0.5 * math.pi - angle
                self.washer.y += 2
        except Exception as e:
            if x > 0:
                angle = math.pi
            elif x <= 0:
                angle = 0
        finally:
            self.washer.strike(v, angle)
            self.location_washer = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec())
