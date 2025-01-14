import math

import pygame
from pygame import K_w, K_s, K_a, K_d, K_q, K_e, K_RSHIFT, K_LSHIFT


class Player():
    def __init__(self, main, x, y, team=0):
        self.main = main # Класс - главный
        self.x, self.y = x, y
        self.necessary_x, self.necessary_y = x, y # необходимые координаты, куда игрок должен приехать
        if team == 0:
            self.player_image = pygame.image.load('player_image.png').convert_alpha()
        else:
            self.player_image = pygame.image.load('player_opponent_image.png').convert_alpha()
        self.rect = self.player_image.get_rect()

    def draw(self): # Показываем
        self.main.screen.blit(self.player_image, (self.x, self.y))

    def move(self):
        moving = 5
        if self.main.moving[4]:
            moving = 10  # Ускорение
        Ox, Oy = 0, 0 # По осям
        if self.main.moving[0]: # Вперед
            Oy -= 1
        if self.main.moving[1]: # Назад
            Oy += 1
        if self.main.moving[2]: # Вправо
            Ox -= 1
        if self.main.moving[3]: # Влево
            Ox += 1
        if Oy != 0 and Ox != 0:
            self.x += moving * Ox * (2 ** 0.5 / 2)
            self.y += moving * Oy * (2 ** 0.5 / 2)
        else:
            self.x += moving * Ox
            self.y += moving * Oy
        if self.main.location_washer == 1: # Шайба у игрока
            self.main.washer.dx, self.main.washer.dy = Ox * moving, Oy * moving
            self.main.washer.x, self.main.washer.y = self.x + 100, self.y

    def move_player_without_washer(self, x, y):
        self.necessary_x = x
        self.necessary_y = y
        try:
            k = (25 / ((self.necessary_x - self.x) ** 2 + (self.necessary_y - self.y) ** 2)) ** 0.5
        except Exception as e:
            k = 0
        self.x += k * (self.necessary_x - self.x)
        self.y += k * (self.necessary_y - self.y)
        if self.main.location_washer == 2 and self.main.owning_washer == self:
            self.main.washer.x, self.main.washer.y = self.x + 100, self.y + 100







    

