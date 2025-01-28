import pygame
import math
from random import randint
from pygame import K_w, K_d, K_s, K_a, K_LSHIFT

from const import Const
from player import Player, Goalkeeper
from washer import Washer


class Game(object):
    def __init__(self, width_m, height_m, screen, dt):
        self.width_m, self.height_m = width_m, height_m
        self.screen_total_game = screen
        self.fps = 45
        self.dt = dt
        self.screen = pygame.Surface((self.width_m, self.height_m * 3))
        self.location_washer = 1  # 0 - ни у кого, 1 - у своей команды, 2 - у чужой команды
        self.moving = (False, False, False, False, False)  # зажатость клавиш wsad LShift
        self.field = pygame.image.load('hockey_field.jpg').convert_alpha()  # Поле
        # Игроки
        self.a1, self.a2, self.a3, self.a4, self.a5 = Player(self, 850, 1650), Player(self, 1150, 1650), \
            Player(self, 550, 1650), Player(self, 1075, 1920), Player(self, 625, 1920)
        self.goalkeeper1, self.goalkeeper2 = Goalkeeper(self, 885, 2870), Goalkeeper(self, 885, 370, team=1)
        self.b1, self.b2, self.b3, self.b4, self.b5 = Player(self, 850, 1550, team=1), Player(self, 1150, 1550, team=1), \
            Player(self, 550, 1550, team=1), Player(self, 1075, 1280, team=1), Player(self, 625, 1280, team=1)
        self.players_own = [self.a1, self.a2, self.a3, self.a4, self.a5, self.goalkeeper1]  # наша команда
        self.players_opponent = [self.b1, self.b2, self.b3, self.b4, self.b5, self.goalkeeper2]  # команда соперника
        self.chosen_player = self.a1  # Выбранный игрок
        self.owning_washer = self.b1  # Владеющий шайбой у соперника
        self.in_out = 0  # Если шайба в зоне подбора шайбы - 1, нет - 0

        self.washer = Washer(950, 1650, 10, (1685, 3155), self, 0, 0)

        self.last_with_washer = {1: ['-', '-'], 2: ['-', '-']}  # Последние, кто владел шайбой
        self.start_time_last_touch = pygame.time.get_ticks()  # Время начала игрока без шайбы

        self.const = Const() # Основные константы и переменные

        self.clock = pygame.time.Clock()

        self.render()

    def render(self):
        self.running = True
        while self.running:
            self.events()
            self.render_game()
            pygame.time.Clock().tick(self.fps)
            pygame.display.flip()
            self.clock.tick(80)

    def events(self):
        for event in pygame.event.get():
            self.moving = (pygame.key.get_pressed()[K_w], pygame.key.get_pressed()[K_s],
                           pygame.key.get_pressed()[K_a], pygame.key.get_pressed()[K_d],
                           pygame.key.get_pressed()[K_LSHIFT])
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.location_washer == 1:
                        # Передача
                        self.broadcast(self.washer.x - pygame.mouse.get_pos()[0],
                                       self.washer.y - pygame.mouse.get_pos()[
                                           1] + min(0.5 * self.height_m - self.washer.y, 0))  # Дельта x и дельта у
                    if self.location_washer == 0:
                        if abs(self.chosen_player.x - self.washer.x) ** 2 + abs(
                                self.chosen_player.y - self.washer.y) ** 2 <= (self.chosen_player.moving * 2) ** 2:
                            self.chosen_player.update(self.washer.x - self.chosen_player.x,
                                                      self.washer.y - self.chosen_player.y)
                    for i in self.players_own:
                        if i.x + 100 >= pygame.mouse.get_pos()[0] >= i.x and i.y + 100 >= \
                                pygame.mouse.get_pos()[1] - min(0.5 * self.height_m - self.washer.y, 0) \
                                >= i.y:
                            self.chosen_player = i
                            break

                # Удар. Начало
                elif event.button == 3:
                    self.x0, self.y0 = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                # Удар. Продолжение
                if event.button == 3:
                    if self.location_washer == 1:
                        x1, y1 = event.pos
                        current_time = pygame.time.get_ticks()  # Время конца удара
                        self.broadcast(self.x0 - x1, self.y0 - y1, v=1000)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

    def render_game(self):
        # Поле
        self.screen.blit(self.field, (0, 0))
        # self.screen.blit()
        dt = self.dt
        self.chosen_player.move()  # Движение выбранного игрока
        if self.location_washer == 1:
            self.attack(self.chosen_player)
        elif self.location_washer == 2:
            self.attack(self.owning_washer)

        # Расставляем игроков на поле
        for i in self.players_own:
            i.draw()
            # Проверка на нахождение шайбы у игрока
            if self.location_washer != 1:
                if i.x + 92 <= self.washer.x <= i.x + 102 and i.y - 2 <= self.washer.y <= i.y + 2:
                    if (i != self.last_with_washer[1][0] \
                            or pygame.time.get_ticks() - self.start_time_last_touch > 1000) and self.in_out == 0:
                        self.location_washer = 1
                        self.chosen_player = i
                        self.in_out = 1

        for i in self.players_opponent:
            i.draw()
            if self.location_washer < 1:
                if i.x + 98 <= self.washer.x <= i.x + 102 and i.y + 98 <= self.washer.y <= i.y + 102:
                    if (i != self.last_with_washer[2][0] \
                            or pygame.time.get_ticks() - self.start_time_last_touch > 1000) and self.in_out == 0:
                        self.location_washer = 2
                        self.owning_washer = i
                        self.in_out = 1

        if self.location_washer == 0:  # Если она не у игроков, то она летает сама по себе
            self.washer.move(dt)
            self.in_out = 0
            self.border()
            self.selection()  # Подбор шайбы

        elif self.location_washer == 2:
            self.tactic_opposing_player_with_washer(self.owning_washer)

        self.zone_checking()
        self.washer.draw(self.screen)
        self.screen_total_game.blit(self.screen,
                                    (0, max(min(0.5 * self.height_m - self.washer.y, 0), -1.75 * self.height_m)))
        pygame.display.flip()

    # Передача / Удар
    def broadcast(self, x, y, v=0):
        if v == 0:
            v = (
                        x ** 2 + y ** 2) ** 0.5  # расстояние между двумя точками, шайба должна прилететь из одной точки в другую за 1 секунду
        angle = self.find_angle(x, y)
        self.washer.strike(v, angle)
        self.loss_washer()
        self.location_washer = 0

    # Функция нахождения угла
    def find_angle(self, x, y):
        try:
            angle = math.atan(x / y)
            if y > 0:
                angle = 1.5 * math.pi - angle
            elif y < 0:
                angle = 0.5 * math.pi - angle
        except Exception as e:
            if x > 0:
                angle = math.pi
            elif x <= 0:
                angle = 0
        return angle

    def attack(self, player_with_washer):
        if self.location_washer < 2:
            taker = min(self.players_opponent[:-1],
                        key=lambda x: (x.x - self.washer.x) ** 2 + (x.y - self.washer.y) ** 2)  # Отбирающий шайбу
            taker.move_player_without_washer(self.washer.x - 100, self.washer.y - 100)
            if self.players_own.index(player_with_washer) < 3:  # Если игрок с шайбой нападающий
                for i in range(3):
                    if self.players_own[i] != player_with_washer:
                        self.players_own[i].move_player_without_washer(self.players_own[i].x, player_with_washer.y)
                        self.players_opponent[i].move_player_without_washer(self.players_opponent[i].x,
                                                                            self.players_own[i].y - 150)
                for i in range(3, 5):
                    self.players_own[i].move_player_without_washer(self.players_own[i].x, player_with_washer.y + 270)
                    self.players_opponent[i].move_player_without_washer(self.players_opponent[i].x,
                                                                        self.players_own[i].y - 690)
            else:
                for i in range(3):
                    self.players_own[i].move_player_without_washer(self.players_own[i].x, player_with_washer.y - 270)
                    self.players_opponent[i].move_player_without_washer(self.players_opponent[i].x,
                                                                        self.players_own[i].y - 150)
                for i in range(3, 5):
                    if self.players_own[i] != player_with_washer:
                        self.players_own[i].move_player_without_washer(self.players_own[i].x, player_with_washer.y)
                        self.players_opponent[i].move_player_without_washer(self.players_opponent[i].x,
                                                                            self.players_own[i].y - 420)
        elif self.location_washer == 2:
            if self.players_opponent.index(player_with_washer) < 3:  # Если игрок с шайбой нападающий
                for i in range(3):
                    if self.players_opponent[i] != player_with_washer:
                        self.players_opponent[i].move_player_without_washer(self.players_opponent[i].x,
                                                                            player_with_washer.y)
                for i in range(3, 5):
                    self.players_opponent[i].move_player_without_washer(self.players_opponent[i].x,
                                                                        player_with_washer.y - 270)
            else:
                for i in range(3):
                    self.players_opponent[i].move_player_without_washer(self.players_opponent[i].x,
                                                                        player_with_washer.y + 270)
                for i in range(3, 5):
                    if self.players_opponent[i] != player_with_washer:
                        self.players_opponent[i].move_player_without_washer(self.players_opponent[i].x,
                                                                            player_with_washer.y)

    def selection(self):  # Подбор шайбы
        taker_own = min(self.players_own[:-1],
                        key=lambda x: (x.x - self.washer.x) ** 2 + (x.y - self.washer.y) ** 2)
        taker_opponent = min(self.players_opponent[:-1],
                             key=lambda x: (x.x - self.washer.x) ** 2 + (x.y - self.washer.y) ** 2)
        taker_own.move_player_without_washer(self.washer.x - 100, self.washer.y)
        taker_opponent.move_player_without_washer(self.washer.x - 100, self.washer.y - 100)
        self.attack(taker_own)

    def tactic_opposing_player_with_washer(self, player):
        action = randint(1, 10)  # 1 - передача, 2 - если в зоне удар, 2(3) - 9 - движение
        if action == 1:
            player_for_broadcast = self.players_opponent[randint(0, 5)]
            if player_for_broadcast != player:
                self.broadcast(self.washer.x - player_for_broadcast.x + 100,
                               self.washer.y - player_for_broadcast.y + 100)
        elif action == 2 and self.washer.y > 2075:
            self.broadcast(self.washer.x - randint(850, 1021), self.washer.y - 2945, v=1000)
        else:
            player.move_player_without_washer(895, 2945)

    # Потеря шайбы
    def loss_washer(self):
        if self.location_washer == 1:
            self.last_with_washer[1][0], self.last_with_washer[1][1] = self.chosen_player, self.last_with_washer[1][0]
        else:
            self.last_with_washer[2][0], self.last_with_washer[2][1] = self.owning_washer, self.last_with_washer[2][0]
        self.start_time_last_touch = pygame.time.get_ticks()  # Время начала игрока без шайбы

    def border(self):
        color_now = self.screen.get_at((int(self.washer.x), int(self.washer.y)))  # цвет пикселя, где находится шайба
        if 40 <= color_now[0] <= 80 and abs(color_now[1] - color_now[2]) <= 10 and (
                self.washer.y < 390 or self.washer.y > 2870):
            if abs(self.washer.x - 180) < abs(self.washer.x - 1685):
                center_of_circle_x = 460
            else:
                center_of_circle_x = 1685 - 280
            if abs(self.washer.x - 100) < abs(self.washer.x - 3155):
                center_of_circle_y = 380
            else:
                center_of_circle_y = 3155 - 280
            tangent_angle = math.atan((center_of_circle_y - self.washer.y) / (center_of_circle_x - self.washer.x))
            angle = self.washer.angle - 2 * (self.washer.angle + tangent_angle - math.pi / 2) + math.pi
            self.washer.dx = self.washer.speed * math.cos(angle)
            self.washer.dy = self.washer.speed * math.sin(angle)
            self.washer.angle = angle

    def zone_checking(self):
        if self.washer.y <= self.const.icing_line_1:
            if self.const.icing_state == 1:
                self.icing()
            self.washer.zone = 1

        elif self.washer.y <= self.const.blue_line_1[0]:
            if self.washer.zone > 2 and min(self.players_own, key=lambda x: x.y).y <= self.const.blue_line_1[1]:
                if self.location_washer == 1:
                    self.offside()
                else:
                    self.const.offside_state = 1
            self.washer.zone = 2

        elif self.const.blue_line_1[1] <= self.washer.y <= self.const.centre_line:
            self.washer.zone = 3
            self.const.offside_state = 0

        elif self.washer.y <= self.const.blue_line_2[1]:
            self.washer.zone = 4
            self.const.offside_state = 0

        elif self.const.blue_line_2[0] <= self.washer.y < self.const.icing_line_2:
            if self.washer.zone < 5 and max(self.players_opponent, key=lambda x: x.y).y + 100 >= self.const.blue_line_2[1]:
                if self.location_washer == 2:
                    self.offside()
                else:
                    self.const.offside_state = 2
            self.washer.zone = 5

        else:
            if self.const.icing_state == 2:
                self.icing()
            self.washer.zone = 6

        if self.washer.zone > 3 and self.location_washer == 0:
            self.const.icing_state = 1
        elif self.washer.zone < 4 and self.location_washer == 0:
            self.const.icing_state = 2
        else:
            self.const.icing_state = 0

    def offside(self): # Вне игра
        print('OFFSIDE')

    def icing(self): # Проброс
        print('ICING')
