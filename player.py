import pygame
from pygame import K_w, K_s, K_a, K_d, K_q, K_e, K_RSHIFT


class Player():
    def __init__(self, main, x, y, with_washer=0):
        self.main = main # Класс - главный
        self.x, self.y, self.with_washer = x, y, with_washer
        self.player = pygame.image.load('player_image.png').convert_alpha()

    def show(self): # Показываем
        self.main.screen.blit(self.player, (self.x, self.y))

    def move(self):
        moving = 5
        if pygame.key.get_pressed()[K_RSHIFT]:
            moving = 10  # Ускорение
        if pygame.key.get_pressed()[K_w]:
            self.y -= moving
        if pygame.key.get_pressed()[K_s]:
            self.y += moving
        if pygame.key.get_pressed()[K_a]:
            self.x -= moving
        if pygame.key.get_pressed()[K_d]:
            self.x += moving

    def throw(self): # Бросок
        pass
    def broadcast(self, event): # Передача
        print(event.pos)



    

