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

    def move(self, main):
        moving = 5
        if pygame.key.get_pressed()[K_LSHIFT]:
            moving = 10  # Ускорение
        if pygame.key.get_pressed()[K_w]:
            self.y -= moving
        if pygame.key.get_pressed()[K_s]:
            self.y += moving
        if pygame.key.get_pressed()[K_a]:
            self.x -= moving
        if pygame.key.get_pressed()[K_d]:
            self.x += moving
        if main.location_washer == 1: # Шайба у игрока
            main.washer.x, main.washer.y = self.x + 100, self.y + 100

    def throw(self): # Бросок
        pass

    def broadcast(self, event, main): # Передача
        print(math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x)))
        main.washer.strike(20, math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x)))
        main.location_washer = 0




    

