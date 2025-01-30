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
        self.fps = 70
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
        self.start_time_last_touch = pygame.time.get_ticks() / 1000  # Время начала игрока без шайбы

        self.const = Const()  # Основные константы и переменные

        self.clock = pygame.time.Clock()

        self.render()

    def render(self):
        self.running = True
        while self.running:
            self.events()
            self.render_game()
            pygame.time.Clock().tick(self.fps)
            pygame.display.flip()

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
                    if self.location_washer == 2:
                        if abs(self.chosen_player.x - pygame.mouse.get_pos()[0]) <= self.chosen_player.moving and \
                                abs(self.chosen_player.y - pygame.mouse.get_pos()[1]) <= self.chosen_player.moving:
                            for i in self.players_opponent:
                                if i.x + 100 >= pygame.mouse.get_pos()[0] >= i.x and i.y + 100 >= \
                                        pygame.mouse.get_pos()[1] - min(0.5 * self.height_m - self.washer.y, 0) \
                                        >= i.y:
                                    self.chosen_player.update(i.x - self.chosen_player.x, i.y - self.chosen_player.y)
                                    if i == self.owning_washer:
                                        self.location_washer = 0
                                    i.update(10, 10)

                                break
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
                        current_time = pygame.time.get_ticks() / 1000  # Время конца удара
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
                        or pygame.time.get_ticks() / 1000 - self.start_time_last_touch > 1) and self.in_out != 1:
                        self.location_washer = 1
                        self.chosen_player = i
                        self.in_out = 1

        for i in self.players_opponent:
            i.draw()
            if self.location_washer != 2:
                if i.x + 98 <= self.washer.x <= i.x + 102 and i.y + 98 <= self.washer.y <= i.y + 102:
                    if (i != self.last_with_washer[2][0] \
                        or pygame.time.get_ticks() / 1000 - self.start_time_last_touch > 1) and self.in_out != 2:
                        self.location_washer = 2
                        self.owning_washer = i
                        self.in_out = 2

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
        action = randint(1, 50)  # 1 - передача, 2 - если в зоне удар, 2(3) - 9 - движение
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
        self.start_time_last_touch = pygame.time.get_ticks() / 1000  # Время начала игрока без шайбы

    def border(self):
        try:
            color_now = self.screen.get_at(
                (int(self.washer.x), int(self.washer.y)))  # цвет пикселя, где находится шайба
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
        except:
            self.face_off(self.const.face_offs.index(
                min(self.const.face_offs, key=lambda x: (x[0] - self.washer.x) ** 2 + (x[1] - self.washer.y) ** 2)))

    def zone_checking(self):
        if self.washer.y <= self.const.icing_line_1:
            if self.const.icing_state == 1:
                self.icing()
            self.washer.zone = 1

        elif self.washer.y <= self.const.blue_line_1[0]:
            if self.washer.zone > 2 and min([i.y for i in self.players_own]) + 100 <= self.const.blue_line_1[0]:
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
            if self.washer.zone < 5 and max([i.y for i in self.players_opponent]) >= self.const.blue_line_2[0]:
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

    def offside(self):  # Вне игра
        self.face_off(self.const.face_offs.index(
            min([self.const.face_off_blue_1, self.const.face_off_blue_2, self.const.face_off_blue_3,
                 self.const.face_off_blue_4], key=lambda x: (x[0] - self.washer.x) ** 2 + (x[1] - self.washer.y) ** 2)))

    def icing(self):  # Проброс
        self.face_off(self.const.face_offs.index(
            min([self.const.face_off_zone_1, self.const.face_off_zone_2, self.const.face_off_zone_3,
                 self.const.face_off_zone_4], key=lambda x: (x[0] - self.washer.x) ** 2 + (x[1] - self.washer.y) ** 2)))

    def face_off(self, number_face_off=0):
        face_of = self.const.face_offs[number_face_off]
        # Растановка на сбрасывании
        self.players_own[0].x, self.players_own[0].y = face_of[0] - 85, face_of[1]
        self.players_own[1].x, self.players_own[1].y = face_of[0] + 215, face_of[1]
        self.players_own[2].x, self.players_own[2].y = face_of[0] - 385, face_of[1]
        self.players_own[3].x, self.players_own[3].y = face_of[0] + 140, face_of[1] + 290
        self.players_own[4].x, self.players_own[4].y = face_of[0] - 210, face_of[1] + 290

        self.players_opponent[0].x, self.players_opponent[0].y = face_of[0] - 85, face_of[1] - 100
        self.players_opponent[1].x, self.players_opponent[1].y = face_of[0] + 215, face_of[1] - 100
        self.players_opponent[2].x, self.players_opponent[2].y = face_of[0] - 385, face_of[1] - 100
        self.players_opponent[3].x, self.players_opponent[3].y = face_of[0] + 140, face_of[1] - 370
        self.players_opponent[4].x, self.players_opponent[4].y = face_of[0] - 210, face_of[1] - 370

        self.washer.x, self.washer.y = face_of

        start = pygame.time.get_ticks()
        total = 0
        n = 0
        while pygame.time.get_ticks() - start < 5000:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        n += 1
            self.screen.blit(self.field, (0, 0))
            for i in self.players_own + self.players_opponent:
                i.draw()
            self.screen_total_game.blit(self.screen,
                                        (0, max(min(0.5 * self.height_m - self.washer.y, 0),
                                                -1.75 * self.height_m)))
            pygame.display.flip()
            if n > 10:
                total = 1
                break
        self.washer.angle = randint(10 + (total == 0) * 180, 170 + (total == 0) * 180)
        self.washer.speed = randint(100, 200)
        self.washer.y += 100 - 200 * (total == 0)
