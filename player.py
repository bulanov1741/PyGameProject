import math

import pygame
from pygame import K_w, K_s, K_a, K_d, K_q, K_e, K_RSHIFT, K_LSHIFT


class Player():
    def __init__(self, main, x, y, with_washer=0):
        self.main = main # Класс - главный
        self.x, self.y, self.with_washer = x, y, with_washer
        self.player = pygame.image.load('player_image.png').convert_alpha()

    def draw(self): # Показываем
        self.main.screen.blit(self.player, (self.x, self.y))

    def move(self):
        moving = 5
        if pygame.key.get_pressed()[K_LSHIFT]:
            moving = 10  # Ускорение
        Ox, Oy = 0, 0 # По осям
        if pygame.key.get_pressed()[K_w]:
            Oy -= 1
        if pygame.key.get_pressed()[K_s]:
            Oy += 1
        if pygame.key.get_pressed()[K_a]:
            Ox -= 1
        if pygame.key.get_pressed()[K_d]:
            Ox += 1
        if Oy != 0 and Ox != 0:
            self.x += moving * Ox * (2 ** 0.5 / 2)
            self.y += moving * Oy * (2 ** 0.5 / 2)
        else:
            self.x += moving * Ox
            self.y += moving * Oy
        if self.main.location_washer == 1: # Шайба у игрока
            self.main.washer.dx, self.main.washer.dy = Ox * moving, Oy * moving
            self.main.washer.x, self.main.washer.y = self.x + 100, self.y + 100






    

