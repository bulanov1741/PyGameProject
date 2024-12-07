import pygame

class Player():
    def __init__(self, main, x, y, with_washer=0):
        self.main = main # Класс - главный
        self.x, self.y, self.with_washer = x, y, with_washer
        self.player = pygame.image.load('player_image.png').convert_alpha()

    def show(self):
        self.main.screen.blit(self.player, (self.x, self.y))

    

