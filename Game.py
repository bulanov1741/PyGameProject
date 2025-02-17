import pygame
import math
from random import randint
from pygame import K_w, K_d, K_s, K_a, K_LSHIFT, Font

from button import Button, Icon
from const import Const
from player import Player, Goalkeeper
from washer import Washer


class Game(object):
    def __init__(self, width_m, height_m, screen, dt, player_team):
        self.width_m, self.height_m = width_m, height_m
        self.const = Const(self.width_m, self.height_m)  # Основные константы и переменные
        self.ptm = player_team  # команда игрока
        self.optm = int(not player_team)  # команда опонента
        self.screen_total_game = screen
        self.fps = 70
        self.dt = dt
        self.screen = pygame.Surface((self.width_m, self.height_m * 3))
        self.location_washer = 1  # 0 - ни у кого, 1 - у своей команды, 2 - у чужой команды
        self.moving = (False, False, False, False, False)  # зажатость клавиш wsad LShift
        self.field = pygame.image.load('hockey_field.jpg').convert_alpha()  # Поле
        self.field = pygame.transform.scale(self.field, (
            self.width_m, 3352 * self.const.k_m[1]))  # Подгоняем картинку под размеры монитора
        self.scoreboard = pygame.image.load('scoreboard.png').convert_alpha()  # Табло со счетом
        self.tablo_after_period = pygame.image.load(
            'tablo_after_period.jpg').convert_alpha()  # Табло со статистикой за период
        self.pause_icon = Icon('pause_icon.png', (self.width_m - 75, 0))  # Иконка паузы # Иконка паузы
        self.pause_image = pygame.image.load('pause.jpg').convert_alpha()  # Когда пауза
        # Игроки
        self.a1, self.a2, self.a3, self.a4, self.a5 = Player(self, 850, 1650, self.ptm, self.ptm), Player(self, 1150,
                                                                                                          1650,
                                                                                                          self.ptm,
                                                                                                          self.ptm), \
            Player(self, 550, 1650, self.ptm, self.ptm), Player(self, 1075, 1920, self.ptm, self.ptm), Player(self, 625,
                                                                                                              1920,
                                                                                                              self.ptm,
                                                                                                              self.ptm)
        self.goalkeeper1, self.goalkeeper2 = Goalkeeper(self, 885 * self.const.k_m[0], 2870 * self.const.k_m[1],
                                                        self.ptm, self.ptm), Goalkeeper(self, 885 * self.const.k_m[0],
                                                                                        370 * self.const.k_m[1],
                                                                                        self.optm,
                                                                                        self.ptm)
        self.b1, self.b2, self.b3, self.b4, self.b5 = Player(self, 850 * self.const.k_m[0], 1550 * self.const.k_m[1],
                                                             self.optm, self.ptm), Player(self, 1150,
                                                                                          1550,
                                                                                          self.optm,
                                                                                          self.ptm), \
            Player(self, 550, 1550, self.optm, self.ptm), Player(self, 1075, 1280, self.optm, self.ptm), Player(self,
                                                                                                                625,
                                                                                                                1280,
                                                                                                                self.optm,
                                                                                                                self.ptm)
        self.players_own = [self.a1, self.a2, self.a3, self.a4, self.a5, self.goalkeeper1]  # наша команда
        self.players_opponent = [self.b1, self.b2, self.b3, self.b4, self.b5, self.goalkeeper2]  # команда соперника
        self.chosen_player = self.a1  # Выбранный игрок
        self.owning_washer = self.b1  # Владеющий шайбой у соперника
        self.in_out = 0  # Если шайба в зоне подбора шайбы - 1, нет - 0

        self.washer = Washer(950, 1650, 10, (1685, 3155), self, 0, 0)

        self.last_with_washer = {1: ['-', '-'], 2: ['-', '-']}  # Последние, кто владел шайбой
        self.last_team_with_washer = 1  # 1 - наша команда, 2 - команда-соперник
        self.start_time_last_touch = pygame.time.get_ticks() / 1000  # Время начала игрока без шайбы

        self.clock = pygame.time.Clock()
        self.time_period_passed = 20_000  # Время начала периода
        self.start = 1
        self.render()

    def render(self):
        self.running = True
        while self.running:
            if self.start == 1:
                self.face_off(0)
                self.start = 0
            self.events()
            self.render_game()
            pygame.time.Clock().tick(self.fps)
            pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.moving = (pygame.key.get_pressed()[K_w], pygame.key.get_pressed()[K_s],
                           pygame.key.get_pressed()[K_a], pygame.key.get_pressed()[K_d],
                           pygame.key.get_pressed()[K_LSHIFT])
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Пауза
                    if self.pause_icon.rect.collidepoint(pygame.mouse.get_pos()):
                        self.pause()
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
                        self.const.shots[0] += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

    def render_game(self):
        # Поле
        self.screen.blit(self.field, (0, 0))
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
        self.scoreboard_data()
        self.screen_total_game.blit(self.scoreboard, (0, 0))  # Отображаем табло
        self.pause_icon.draw(self.screen_total_game)
        if self.time_period_passed <= 0:
            self.intermission()  # Перерыв
        self.time_period_passed -= (1000 / 3) / self.fps
        self.record_for_replay()  # Запись действий
        pygame.display.flip()

    # Передача / Удар
    def broadcast(self, x, y, v=0):
        if v == 0:
            v = (
                        x ** 2 + y ** 2) ** 0.5 * 2  # расстояние между двумя точками, шайба должна прилететь из одной точки в другую за 1 секунду
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
        if self.chosen_player != self.goalkeeper1:
            self.goalkeeper1.position(self.washer.x, self.washer.y)
        self.goalkeeper2.position(self.washer.x, self.washer.y)
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
        elif action == 2 and self.washer.y > 2075 * self.const.k_m[1]:
            self.broadcast(self.washer.x - randint(850 * self.const.k_m[0], 1021 * self.const.k_m[0]),
                           self.washer.y - 2945 * self.const.k_m[1], v=2000)
            self.const.shots[1] += 1
        else:
            player.move_player_without_washer(895 * self.const.k_m[0], 2945 * self.const.k_m[1])

    # Потеря шайбы
    def loss_washer(self):
        if self.location_washer == 1:
            self.last_with_washer[1][0], self.last_with_washer[1][1] = self.chosen_player, self.last_with_washer[1][0]
            self.last_team_with_washer = 1
        else:
            self.last_with_washer[2][0], self.last_with_washer[2][1] = self.owning_washer, self.last_with_washer[2][0]
            self.last_team_with_washer = 2
        self.start_time_last_touch = pygame.time.get_ticks() / 1000  # Время начала игрока без шайбы

    def border(self):
        if self.washer.x + self.washer.radius < self.const.min_x or \
                self.washer.x - self.washer.radius > self.const.max_x or \
                self.washer.y + self.washer.radius < self.const.min_y or \
                self.washer.y - self.washer.radius > self.const.max_y:
            self.inscription_about_situation("THE PUCK OUTSIDE THE PLAYING AREA")
            self.face_off(self.const.face_offs.index(
                min(self.const.face_offs, key=lambda x: (x[0] - self.washer.x) ** 2 + (x[1] - self.washer.y) ** 2)))
        else:
            color_now = self.screen.get_at(
                (int(self.washer.x), int(self.washer.y)))  # цвет пикселя, где находится шайба
            if 40 <= color_now[0] <= 80 and abs(color_now[1] - color_now[2]) <= 10 and (
                    self.washer.y < 390 * self.const.k_m[1] or self.washer.y > 2870 * self.const.k_m[1]):
                if abs(self.washer.x - 180 * self.const.k_m[0]) < abs(self.washer.x - 1685 * self.const.k_m[0]):
                    center_of_circle_x = 460 * self.const.k_m[0]
                else:
                    center_of_circle_x = (1685 - 280) * self.const.k_m[0]
                if abs(self.washer.x - 100) < abs(self.washer.x - 3155):
                    center_of_circle_y = 380 * self.const.k_m[1]
                else:
                    center_of_circle_y = (3155 - 280) * self.const.k_m[1]
                tangent_angle = math.atan((center_of_circle_y - self.washer.y) / (center_of_circle_x - self.washer.x))
                angle = self.washer.angle - 2 * (self.washer.angle + tangent_angle - math.pi / 2) + math.pi
                self.washer.dx = self.washer.speed * math.cos(angle)
                self.washer.dy = self.washer.speed * math.sin(angle)
                self.washer.angle = angle

    def zone_checking(self):
        if self.washer.y <= self.const.icing_line_1:
            if self.const.icing_state[0] == 1:
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
            if self.const.icing_state[1] == 1:
                self.icing()
            self.washer.zone = 6

        if self.washer.zone > 3 and self.location_washer == 0 and self.last_team_with_washer == 1:
            self.const.icing_state[0] = 1
        elif self.washer.zone < 4 and self.location_washer == 0 and self.last_team_with_washer == 2:
            self.const.icing_state[1] = 1
        else:
            self.const.icing_state = [0, 0]

    def offside(self):  # Вне игры
        self.inscription_about_situation('OFFSIDE')
        place_offcide = min([self.const.face_off_blue_1, self.const.face_off_blue_2, self.const.face_off_blue_3,
                             self.const.face_off_blue_4],
                            key=lambda x: (x[0] - self.washer.x) ** 2 + (x[1] - self.washer.y) ** 2)
        self.stoppage()  # Показываем повтор
        self.const.offsides[
            place_offcide == self.const.face_off_blue_3 or place_offcide == self.const.face_off_blue_4] += 1
        self.face_off(self.const.face_offs.index(place_offcide))

    def icing(self):  # Проброс
        self.inscription_about_situation('ICING')
        place_icing = min([self.const.face_off_zone_1, self.const.face_off_zone_2, self.const.face_off_zone_3,
                           self.const.face_off_zone_4],
                          key=lambda x: (x[0] - self.washer.x, -1 * abs(self.washer.y - x[1])))
        self.stoppage()  # Показываем повтор
        self.const.icings[place_icing == self.const.face_off_zone_3 or place_icing == self.const.face_off_zone_4] += 1
        self.face_off(self.const.face_offs.index(place_icing))

    def goal(self, team):
        start = pygame.time.get_ticks()
        n = 0
        while pygame.time.get_ticks() - start < 7000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        n += 1
            self.screen.blit(self.field, (0, 0))
            if (pygame.time.get_ticks() - start) % 100 == 0:
                if team == 1:
                    pygame.draw.rect(self.screen, pygame.Color(250, 100, 100), (866, 2951, 990, 3018))
                elif team == 2:
                    pygame.draw.rect(self.screen, pygame.Color(250, 100, 100), (866, 236, 990, 303))
            for i in self.players_own + self.players_opponent:
                i.draw()
            self.screen_total_game.blit(self.screen,
                                        (0, max(min(0.5 * self.height_m - self.washer.y, 0),
                                                -1.75 * self.height_m)))
            text = self.const.font_situation.render('GOOOOOOOAL', False, (255, 0, 0))
            self.screen_total_game.blit(text, (
                (self.width_m - text.size[0]) // 2, (self.height_m - text.size[1]) // 2))
            pygame.display.flip()
            if n > 3:
                break
            pygame.time.Clock().tick(self.fps)
        self.stoppage()  # Показываем повтор

    def face_off(self, number_face_off=0):  # Вбрасывание
        face_of = self.const.face_offs[number_face_off]
        # Растановка на вбрасывании
        self.players_own[0].x, self.players_own[0].y = face_of[0] - 85 * self.const.k_m[0], face_of[1]
        self.players_own[1].x, self.players_own[1].y = face_of[0] + 215 * self.const.k_m[0], face_of[1]
        self.players_own[2].x, self.players_own[2].y = face_of[0] - 385 * self.const.k_m[0], face_of[1]
        self.players_own[3].x, self.players_own[3].y = face_of[0] + 140 * self.const.k_m[0], face_of[1] + 290 * \
                                                       self.const.k_m[1]
        self.players_own[4].x, self.players_own[4].y = face_of[0] - 210 * self.const.k_m[0], face_of[1] + 290 * \
                                                       self.const.k_m[1]

        self.players_opponent[0].x, self.players_opponent[0].y = face_of[0] - 85 * self.const.k_m[0], face_of[1] - 100 * \
                                                                 self.const.k_m[1]
        self.players_opponent[1].x, self.players_opponent[1].y = face_of[0] + 215 * self.const.k_m[0], face_of[
            1] - 100 * self.const.k_m[1]
        self.players_opponent[2].x, self.players_opponent[2].y = face_of[0] - 385 * self.const.k_m[0], face_of[
            1] - 100 * self.const.k_m[1]
        self.players_opponent[3].x, self.players_opponent[3].y = face_of[0] + 140 * self.const.k_m[0], face_of[
            1] - 370 * self.const.k_m[1]
        self.players_opponent[4].x, self.players_opponent[4].y = face_of[0] - 210 * self.const.k_m[0], face_of[
            1] - 370 * self.const.k_m[1]

        self.washer.x, self.washer.y = face_of

        start = pygame.time.get_ticks()
        total = 0
        n = 0
        while pygame.time.get_ticks() - start < 5000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
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
            pygame.time.Clock().tick(self.fps)
        self.washer.angle = randint(10 + (total == 0) * 180, 170 + (total == 0) * 180)
        self.washer.speed = randint(100, 200)
        self.washer.y += 100 - 200 * (total == 0)
        self.const.face_offs_counts[total == 0] += 1

    def scoreboard_data(self):  # Отображение счета
        our_score = self.const.font_score.render(str(self.const.our_score), False, (255, 255, 255), (11, 40, 58))
        opponent_score = self.const.font_score.render(str(self.const.opponent_score), False, (255, 255, 255),
                                                      (152, 45, 41))
        period = self.const.font_score.render(str(self.const.period), False, (0, 0, 0), (231, 233, 230))
        # Время
        minutes = '0' * (self.time_period_passed < 10000) + str(int(self.time_period_passed // 1000))
        seconds = ('0' * (self.time_period_passed % 1000 // 5 * 3 < 10) + str(self.time_period_passed % 1000 // 5 * 3))[
                  :2]
        time = self.const.font_score.render(minutes + ':' + seconds, False, (0, 0, 0), (231, 233, 230))

        self.scoreboard.blit(our_score, (378 * self.const.k_m[0], 59 * self.const.k_m[1]))
        self.scoreboard.blit(opponent_score, (451 * self.const.k_m[0], 59 * self.const.k_m[1]))
        self.scoreboard.blit(period, (645 * self.const.k_m[0], 59 * self.const.k_m[1]))
        self.scoreboard.blit(time, (753 * self.const.k_m[0], 59 * self.const.k_m[1]))

    def intermission(self):  # Перерыв между периодами
        shots_our = self.const.font_score.render(str(self.const.shots[0]), False, (232, 234, 233))
        shots_opponent = self.const.font_score.render(str(self.const.shots[1]), False, (232, 234, 233))
        shots_on_goal_our = self.const.font_score.render(str(self.const.shots_on_goal[0]), False, (232, 234, 233))
        shots_on_goal_opponent = self.const.font_score.render(str(self.const.shots_on_goal[1]), False, (232, 234, 233))
        offsides_our = self.const.font_score.render(str(self.const.offsides[0]), False, (232, 234, 233))
        offsides_opponent = self.const.font_score.render(str(self.const.offsides[1]), False, (232, 234, 233))
        icings_our = self.const.font_score.render(str(self.const.icings[0]), False, (232, 234, 233))
        icings_opponent = self.const.font_score.render(str(self.const.icings[1]), False, (232, 234, 233))
        face_offs_counts_our = self.const.font_score.render(str(self.const.face_offs_counts[0]), False, (232, 234, 233))
        face_offs_counts_opponent = self.const.font_score.render(str(self.const.face_offs_counts[1]), False,
                                                                 (232, 234, 233))
        penalty_our = self.const.font_score.render(str(self.const.penalty[0]), False, (232, 234, 233))
        penalty_opponent = self.const.font_score.render(str(self.const.penalty[1]), False, (232, 234, 233))
        powerplay_goals_our = self.const.font_score.render(str(self.const.powerplay_goals[0]), False, (232, 234, 233))
        powerplay_goals_opponent = self.const.font_score.render(str(self.const.powerplay_goals[1]), False,
                                                                (232, 234, 233))
        shorthanded_goals_our = self.const.font_score.render(str(self.const.shorthanded_goals[0]), False,
                                                             (232, 234, 233))
        shorthanded_goals_opponent = self.const.font_score.render(str(self.const.shorthanded_goals[1]), False,
                                                                  (232, 234, 233))

        period = self.const.font_statistic_period.render(str(self.const.period), False,
                                                         (232, 234, 233))
        score_own = self.const.font_statistic_score.render(str(self.const.our_score), False,
                                                           (13, 14, 18))
        score_opponent = self.const.font_statistic_score.render(str(self.const.opponent_score), False,
                                                                (13, 14, 18))
        # Статистика
        tablo_after_period = pygame.Surface((1150 * self.const.k_m[0], 840 * self.const.k_m[1]))
        tablo_after_period.blit(self.tablo_after_period, (0, 0))
        tablo_after_period.blit(shots_our, (90 * self.const.k_m[0], 360 * self.const.k_m[1]))
        tablo_after_period.blit(shots_on_goal_our, (90 * self.const.k_m[0], 420 * self.const.k_m[1]))
        tablo_after_period.blit(offsides_our, (90 * self.const.k_m[0], 480 * self.const.k_m[1]))
        tablo_after_period.blit(icings_our, (90 * self.const.k_m[0], 540 * self.const.k_m[1]))
        tablo_after_period.blit(face_offs_counts_our, (90 * self.const.k_m[0], 600 * self.const.k_m[1]))
        tablo_after_period.blit(penalty_our, (90 * self.const.k_m[0], 660 * self.const.k_m[1]))
        tablo_after_period.blit(powerplay_goals_our, (90 * self.const.k_m[0], 720 * self.const.k_m[1]))
        tablo_after_period.blit(shorthanded_goals_our, (90 * self.const.k_m[0], 780 * self.const.k_m[1]))
        tablo_after_period.blit(shots_opponent, (960 * self.const.k_m[0], 360 * self.const.k_m[1]))
        tablo_after_period.blit(shots_on_goal_opponent, (960 * self.const.k_m[0], 420 * self.const.k_m[1]))
        tablo_after_period.blit(offsides_opponent, (960 * self.const.k_m[0], 480 * self.const.k_m[1]))
        tablo_after_period.blit(icings_opponent, (960 * self.const.k_m[0], 540 * self.const.k_m[1]))
        tablo_after_period.blit(face_offs_counts_opponent, (960 * self.const.k_m[0], 600 * self.const.k_m[1]))
        tablo_after_period.blit(penalty_opponent, (960 * self.const.k_m[0], 660 * self.const.k_m[1]))
        tablo_after_period.blit(powerplay_goals_opponent, (960 * self.const.k_m[0], 720 * self.const.k_m[1]))
        tablo_after_period.blit(shorthanded_goals_opponent, (960 * self.const.k_m[0], 780 * self.const.k_m[1]))
        tablo_after_period.blit(period, (477 * self.const.k_m[0], 40 * self.const.k_m[1]))
        tablo_after_period.blit(score_own, (414 * self.const.k_m[0], 146 * self.const.k_m[1]))
        tablo_after_period.blit(score_opponent, (618 * self.const.k_m[0], 146 * self.const.k_m[1]))

        start = pygame.time.get_ticks()
        n = 0
        while pygame.time.get_ticks() - start < 7000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        n += 1
            self.screen.blit(self.field, (0, 0))
            self.screen_total_game.blit(self.screen,
                                        (0, max(min(0.5 * self.height_m - self.washer.y, 0),
                                                -1.75 * self.height_m)))
            self.screen_total_game.blit(tablo_after_period,
                                        ((self.width_m - 1122 * self.const.k_m[0]) // 2,
                                         (self.height_m - 820 * self.const.k_m[1]) // 2))
            pygame.display.flip()
            if n > 2:
                break
            pygame.time.Clock().tick(self.fps)
        if self.const.period == 3:
            self.running = False
        else:
            self.const.period += 1
            self.time_period_passed = 20000
            self.face_off(0)

    def inscription_about_situation(self, line, count=1, time=5000):  # Причина остановки игры
        start = pygame.time.get_ticks()
        n = 0
        while pygame.time.get_ticks() - start < time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        n += 1
            self.screen.blit(self.field, (0, 0))
            for i in self.players_own + self.players_opponent:
                i.draw()
            self.screen_total_game.blit(self.screen,
                                        (0, max(min(0.5 * self.height_m - self.washer.y, 0),
                                                -1.75 * self.height_m)))
            text = self.const.font_situation.render(line, False, (255, 0, 0))
            self.screen_total_game.blit(text, ((self.width_m - text.size[0]) // 2, (self.height_m - text.size[1]) // 2))
            pygame.display.flip()
            if n > count:
                break
            pygame.time.Clock().tick(self.fps)

    def record_for_replay(self):  # Запись игры
        a = self.players_own + self.players_opponent + [self.washer]
        for i in range(13):
            self.const.all_replay[i].pop(0)
            self.const.all_replay[i].append((a[i].x, a[i].y))

    def replay(self):  # Повтор
        n = 0
        a = self.players_own + self.players_opponent + [self.washer]
        try:
            start_ind = min([ind for ind in range(350) if self.const.a1_replay[ind] != (0, 0)])
        except:
            start_ind = 0
        for i in range(start_ind, 350):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        n += 1
            self.screen.blit(self.field, (0, 0))
            for j in range(13):
                a[j].x, a[j].y = self.const.all_replay[j][i]
                if j == 12:
                    a[j].draw(self.screen)
                else:
                    a[j].draw()
            self.screen_total_game.blit(self.screen,
                                        (0, max(min(0.5 * self.height_m - self.washer.y, 0),
                                                -1.75 * self.height_m)))
            pygame.display.flip()
            if n > 2:
                break
            pygame.time.Clock().tick(self.fps)

    def stoppage(self):  # Остановка игры
        self.transition()  # Заставка
        self.replay()
        for i in self.const.all_replay:
            i = [(0, 0)] * 350
        self.transition()

    def transition(self):  # Переход на повтор
        n = 0
        while n < 110:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    n = 110
            self.screen.blit(self.field, (0, 0))
            for i in self.players_own + self.players_opponent:
                i.draw()
            self.screen_total_game.blit(self.screen,
                                        (0, max(min(0.5 * self.height_m - self.washer.y, 0),
                                                -1.75 * self.height_m)))
            self.screen_total_game.blit(self.const.anim_transition[n // 10], (0, 0))
            n += 1
            pygame.display.flip()
            pygame.time.Clock().tick(self.fps)

    def pause(self):
        # Все данные для окна паузы
        score_our = self.const.font_pause_score.render(str(self.const.our_score), False,
                                                       (255, 255, 255))
        score_opponent = self.const.font_pause_score.render(str(self.const.opponent_score), False,
                                                            (255, 255, 255))
        time_1 = self.const.font_pause_time.render(str(int(self.time_period_passed // 10000)), False,
                                                   (255, 255, 255))
        time_2 = self.const.font_pause_time.render(str(int(self.time_period_passed // 1000 % 10)), False,
                                                   (255, 255, 255))
        time_3 = self.const.font_pause_time.render(str(int(self.time_period_passed % 1000 // 5 * 3 // 100)), False,
                                                   (255, 255, 255))
        time_4 = self.const.font_pause_time.render(str(int(self.time_period_passed % 1000 // 5 * 3 // 10 % 10)), False,
                                                   (255, 255, 255))
        period = self.const.font_pause_period.render(str(self.const.period), False, (255, 255, 255))
        team_our = self.const.font_pause_name.render(str('ВЫ'), False, (0, 0, 0))
        team_opponent = self.const.font_pause_name.render(str('ПРОТИВНИК'), False, (0, 0, 0))

        button_continue = Button(200 * self.const.k_m[0], 575 * self.const.k_m[1],
                                 200 * self.const.k_m[0], 60 * self.const.k_m[1], 'CONTINUE', (0, 0, 0),
                                 (200, 200, 200))
        button_exit = Button(600 * self.const.k_m[0], 575 * self.const.k_m[1],
                             150 * self.const.k_m[0], 60 * self.const.k_m[1], 'EXIT', (0, 0, 0),
                             (200, 200, 200))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_pos = (pygame.mouse.get_pos()[0] - (self.width_m - self.pause_image.size[0]) // 2, \
                                     pygame.mouse.get_pos()[1] - (self.height_m - self.pause_image.size[1]) // 2)
                        if button_continue.x <= mouse_pos[0] <= button_continue.x + button_continue.width and \
                                button_continue.y <= mouse_pos[1] <= button_continue.y + button_continue.height:
                            running = False
                        elif button_exit.x <= mouse_pos[0] <= button_exit.x + button_exit.width and \
                                button_exit.y <= mouse_pos[1] <= button_exit.y + button_exit.height:
                            self.running = False
                            running = False

            self.screen.blit(self.field, (0, 0))
            for i in self.players_own + self.players_opponent:
                i.draw()
            self.screen_total_game.blit(self.screen,
                                        (0, max(min(0.5 * self.height_m - self.washer.y, 0),
                                                -1.75 * self.height_m)))
            pause_image = self.pause_image.copy()
            pause_image.blit(score_our, (325 * self.const.k_m[0], 420 * self.const.k_m[1]))
            pause_image.blit(score_opponent, (675 * self.const.k_m[0], 420 * self.const.k_m[1]))
            pause_image.blit(time_1, (422 * self.const.k_m[0], 85 * self.const.k_m[1]))
            pause_image.blit(time_2, (475 * self.const.k_m[0], 85 * self.const.k_m[1]))
            pause_image.blit(time_3, (555 * self.const.k_m[0], 85 * self.const.k_m[1]))
            pause_image.blit(time_4, (611 * self.const.k_m[0], 85 * self.const.k_m[1]))
            pause_image.blit(period, (485 * self.const.k_m[0], 36 * self.const.k_m[1]))
            pause_image.blit(team_our, (210 * self.const.k_m[0], 222 * self.const.k_m[1]))
            pause_image.blit(team_opponent, (650 * self.const.k_m[0], 222 * self.const.k_m[1]))
            button_continue.draw(pause_image, self)
            button_exit.draw(pause_image, self)
            self.screen_total_game.blit(pause_image, (
                (self.width_m - self.pause_image.size[0]) // 2, (self.height_m - self.pause_image.size[1]) // 2))
            pygame.display.flip()
            pygame.time.Clock().tick(self.fps)
