import math

import pygame
from pygame import K_w, K_s, K_a, K_d, K_q, K_e, K_RSHIFT, K_LSHIFT


class Player():
    def __init__(self, main, x, y, with_washer=0):
        self.main = main # Класс - главный
        self.x, self.y, self.with_washer = x, y, with_washer
        self.player = pygame.image.load('player_image.png').convert_alpha()
        self.rect = self.player.get_rect()

    def draw(self): # Показываем
        self.main.screen.blit(self.player, (self.x, self.y))

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






    

