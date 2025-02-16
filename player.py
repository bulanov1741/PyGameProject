import math

import pygame
from pygame import K_w, K_s, K_a, K_d, K_q, K_e, K_RSHIFT, K_LSHIFT

from const import Const


class Player():
    def __init__(self, main, x, y, team=0, reverse_picture=False):
        self.main = main  # Класс - главный
        self.const = self.main.const
        self.x, self.y = x, y
        self.necessary_x, self.necessary_y = x, y  # необходимые координаты, куда игрок должен приехать
        if team == 0:
            self.player_image = pygame.image.load('player_image.png').convert_alpha()
            if reverse_picture:
                self.player_image = pygame.transform.flip(self.player_image, False, True)
        else:
            self.player_image = pygame.image.load('player_opponent_image.png').convert_alpha()
            if reverse_picture:
                self.player_image = pygame.transform.flip(self.player_image, False, True)
        self.rect = self.player_image.get_rect()
        self.moving = 5 * self.const.k_m[0]

    def draw(self):  # Показываем
        self.main.screen.blit(self.player_image, (self.x, self.y))

    def update(self, x=0, y=0):
        # Столкновение с игроками
        for i in self.main.players_own + self.main.players_opponent:
            if i != self:
                if y < 0:
                    if self.y >= i.y + 100 > self.y + y and (self.x <= i.x <= self.x + 100 or i.x <= self.x <= i.x + 100):
                        y = (i.y + 100 - self.y) + (y - i.y - 100 + self.y) // 2
                        i.update(x, y)
                        break
                else:
                    if self.y + 100 <= i.y < self.y + y + 100 and (self.x <= i.x <= self.x + 100 or i.x <= self.x <= i.x + 100):
                        y = (self.y + 100 - i.y) + (self.y + 100 - i.y) // 2
                        i.update(x, y)
                        break
                if x < 0:
                    if self.x >= i.x + 100 > self.x + x and (self.y <= i.y <= self.y + 100 or i.y <= self.y <= i.y + 100):
                        x = (i.x + 100 - self.x) + (x - i.x - 100 + self.x) // 2
                        i.update(x, y)
                        break
                else:
                    if self.x + 100 <= i.x < self.x + x + 100 and (self.y <= i.y <= self.y + 100 or i.y <= self.y <= i.y + 100):
                        x = (i.x - 100 - self.x) + (i.x - 100 - self.x) // 2
                        i.update(x, y)
                        break


        # Столкновение с бортами
        if x < 0:
            color_1 = self.main.screen.get_at((int(self.x) + x, int(self.y)))
            color_2 = self.main.screen.get_at((int(self.x) + x, int(self.y) + 100))
        else:
            color_1 = self.main.screen.get_at((int(self.x) + 100 + x, int(self.y)))
            color_2 = self.main.screen.get_at((int(self.x) + 100 + x, int(self.y) + 100))
        if y > 0:
            color_3 = self.main.screen.get_at((int(self.x), int(self.y) + 100 + y))
            color_4 = self.main.screen.get_at((int(self.x) + 100, int(self.y) + 100 + y))
        else:
            color_3 = self.main.screen.get_at((int(self.x), int(self.y) + y))
            color_4 = self.main.screen.get_at((int(self.x) + 100, int(self.y) + y))
        if 40 <= color_1[0] <= 80 and abs(color_1[1] - color_1[2]) <= 10 or 40 <= color_2[0] <= 80 and abs(
                color_2[1] - color_2[2]) <= 10:
            x = 0
        if 40 <= color_3[0] <= 80 and abs(color_3[1] - color_3[2]) <= 10 or 40 <= color_4[0] <= 80 and abs(
                color_4[1] - color_4[2]) <= 10:
            y = 0
        self.x += x
        self.y += y


    def move(self):
        moving = self.moving
        if self.main.moving[4]:
            moving *= 2  # Ускорение
        Ox, Oy = 0, 0  # По осям
        if self.main.moving[0]:  # Вперед
            Oy -= 1
        if self.main.moving[1]:  # Назад
            Oy += 1
        if self.main.moving[2]:  # Вправо
            Ox -= 1
        if self.main.moving[3]:  # Влево
            Ox += 1
        if Oy != 0 and Ox != 0:
            self.update(moving * Ox * (2 ** 0.5 / 2), moving * Oy * (2 ** 0.5 / 2))
        else:
            self.update(moving * Ox, moving * Oy)
        if self.main.location_washer == 1:  # Шайба у игрока
            self.main.washer.dx, self.main.washer.dy = Ox * moving, Oy * moving
            self.main.washer.x, self.main.washer.y = self.x + 100, self.y

    def move_player_without_washer(self, x, y):
        self.necessary_x = x
        self.necessary_y = y
        try:
            k = (self.moving ** 2 / ((self.necessary_x - self.x) ** 2 + (self.necessary_y - self.y) ** 2)) ** 0.5
            self.update(k * (self.necessary_x - self.x), k * (self.necessary_y - self.y))
        except Exception as e:
            k = 0
        if self.main.location_washer == 2 and self.main.owning_washer == self:
            self.main.washer.x, self.main.washer.y = self.x + 100, self.y + 100


class Goalkeeper(Player):
    def __init__(self, main, x, y, team=0, reverse_picture=False):
        self.team = team
        self.x_zero, self.y_zero = x, y
        self.main = main  # Класс - главный
        self.const = self.main.const
        self.x, self.y = x, y
        self.necessary_x, self.necessary_y = x, y  # необходимые координаты, куда игрок должен приехать
        if team == 0:
            self.player_image = pygame.image.load('player_image.png').convert_alpha()
            if reverse_picture:
                self.player_image = pygame.transform.flip(self.player_image, False, True)
        else:
            self.player_image = pygame.image.load('player_opponent_image.png').convert_alpha()
            if reverse_picture:
                self.player_image = pygame.transform.flip(self.player_image, False, True)
        self.moving = 3 * self.const.k_m[0]
        self.rect = self.player_image.get_rect()

    def update(self, x=0, y=0):
        self.x = min(max(self.x + x, self.x_zero - 130 * self.const.k_m[0]), self.x_zero + 130 * self.const.k_m[0])
        self.y = min(max(self.y + y, self.y_zero - 70 * self.const.k_m[1]), self.y_zero + 70 * self.const.k_m[1])

    def position(self, x_washer, y_washer):
        if pygame.time.get_ticks() % 20 == 0:
            gates = (928, 2951 * (self.team == 0) + 303 * (self.team == 1))
            self.necessary_y = gates[1] - 120 * (self.team == 0) + 20 * (self.team == 1)
            if self.team == 0 and y_washer > gates[1] or self.team == 1 and y_washer < gates[1]:
                self.necessary_x = gates[0] + 66 * (x_washer > gates[0]) - 66 * (x_washer < gates[0]) - 50
            else:
                self.necessary_x = gates[0] - (
                            (gates[0] - x_washer) * (self.necessary_y - gates[1]) // (y_washer - gates[1])) // 10 * 10 - 50
        self.move_player_without_washer(self.necessary_x, self.necessary_y)