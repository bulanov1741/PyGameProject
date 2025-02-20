import pygame


class Const:
    def __init__(self, width, height, lang, club_our):
        # Размеры монитора
        self.width_m, self.height_m = width, height
        self.k_m = self.width_m / 1920, self.height_m / 1200

        # Названия команд
        self.club_our, self.club_opponent = club_our + 'Красная Армия' * (club_our == ''), 'Авто'
        with open('teams.csv', "r", encoding="utf_8_sig") as file:
            a = file.readlines()[1:]
            b = [i.strip().split(';')[0] for i in a]
            self.club_our_abbreviation = a[b.index(self.club_our)].split(';')[5]
            self.club_opponent_abbreviation = a[b.index(self.club_opponent)].split(';')[5]
            if lang == 'ENG':
                self.club_our = a[b.index(self.club_our)].split(';')[6]
                self.club_opponent = a[b.index(self.club_opponent)].split(';')[6]

        # Вбрасывания
        self.face_off_centre = (935 * self.k_m[0], 1630 * self.k_m[1])  # Центр
        self.face_off_blue_1 = (600 * self.k_m[0], 1260 * self.k_m[1])  # Около синей линии
        self.face_off_blue_2 = (1265 * self.k_m[0], 1260 * self.k_m[1])
        self.face_off_blue_3 = (600 * self.k_m[0], 1995 * self.k_m[1])
        self.face_off_blue_4 = (1265 * self.k_m[0], 1995 * self.k_m[1])
        self.face_off_zone_1 = (600 * self.k_m[0], 640 * self.k_m[1])  # В зоне
        self.face_off_zone_2 = (1265 * self.k_m[0], 640 * self.k_m[1])
        self.face_off_zone_3 = (600 * self.k_m[0], 2610 * self.k_m[1])
        self.face_off_zone_4 = (1265 * self.k_m[0], 2610 * self.k_m[1])
        self.face_offs = [self.face_off_centre, self.face_off_blue_1, self.face_off_blue_2, self.face_off_blue_3,
                          self.face_off_blue_4, self.face_off_zone_1, self.face_off_zone_2, self.face_off_zone_3,
                          self.face_off_zone_4]

        # Границы поля
        self.min_x = 180 * self.k_m[0]
        self.max_x = 1685 * self.k_m[0]
        self.min_y = 105 * self.k_m[1]
        self.max_y = 3155 * self.k_m[1]

        # Линии
        self.icing_line_1 = 303 * self.k_m[1] # Проброса / лицевые
        self.icing_line_2 = 2950 * self.k_m[1]
        self.blue_line_1 = (1178 * self.k_m[1], 1196 * self.k_m[1])
        self.blue_line_2 = (2076 * self.k_m[1], 2058 * self.k_m[1])
        self.centre_line = 1627 * self.k_m[1]

        # Ситуации
        self.font_situation = pygame.font.SysFont('Bleeker Rus (Fixed)', 120)
        self.offside_state = 0  # Предофсайдное
        self.icing_state = [0, 0]  # Предпробросное
        self.start = 1  # Предначальное

        # Счет
        self.our_score = 0
        self.opponent_score = 0
        self.font_score = pygame.font.SysFont('Transformers Movie', 60)
        self.font_score_club = pygame.font.SysFont('Transformers Movie', 50)
        self.period = 1
        self.time_minute = 3000  # Каждая минута мс

        # Статистика за период
        self.font_statistic_score = pygame.font.SysFont('Transformers Movie', 120)
        self.font_statistic_period = pygame.font.SysFont('Transformers Movie', 70)
        self.shots = [0, 0]
        self.shots_on_goal = [0, 0]
        self.offsides = [0, 0]
        self.icings = [0, 0]
        self.face_offs_counts = [0, 0]
        self.penalty = [0, 0]
        self.powerplay_goals = [0, 0]
        self.shorthanded_goals = [0, 0]

        # Последние 5 секунд (для повторов)
        self.a1_replay = [(0, 0)] * 350
        self.a2_replay = [(0, 0)] * 350
        self.a3_replay = [(0, 0)] * 350
        self.a4_replay = [(0, 0)] * 350
        self.a5_replay = [(0, 0)] * 350
        self.goalkeeper1_replay = [(0, 0)] * 350
        self.b1_replay = [(0, 0)] * 350
        self.b2_replay = [(0, 0)] * 350
        self.b3_replay = [(0, 0)] * 350
        self.b4_replay = [(0, 0)] * 350
        self.b5_replay = [(0, 0)] * 350
        self.goalkeeper2_replay = [(0, 0)] * 350
        self.washer_replay = [(0, 0)] * 350
        self.all_replay = [self.a1_replay, self.a2_replay, self.a3_replay, self.a4_replay, self.a5_replay,
                           self.goalkeeper1_replay, self.b1_replay, self.b2_replay, self.b3_replay,
                           self.b4_replay, self.b5_replay, self.goalkeeper2_replay, self.washer_replay]

        # Переход между повторами
        self.image_1 = pygame.image.load('animation/image (1).png').convert_alpha()
        self.image_2 = pygame.image.load('animation/image (2).png').convert_alpha()
        self.image_3 = pygame.image.load('animation/image (3).png').convert_alpha()
        self.image_4 = pygame.image.load('animation/image (4).png').convert_alpha()
        self.image_5 = pygame.image.load('animation/image (5).png').convert_alpha()
        self.image_6 = pygame.image.load('animation/image (6).png').convert_alpha()
        self.image_7 = pygame.image.load('animation/image (7).png').convert_alpha()
        self.image_8 = pygame.image.load('animation/image (8).png').convert_alpha()
        self.image_9 = pygame.image.load('animation/image (9).png').convert_alpha()
        self.image_10 = pygame.image.load('animation/image (10).png').convert_alpha()
        self.image_11 = pygame.image.load('animation/image (11).png').convert_alpha()
        self.anim_transition = [self.image_1, self.image_2, self.image_3, self.image_4, self.image_5, self.image_6,
                                self.image_7, self.image_8, self.image_9, self.image_10, self.image_11]
        for i in range(11):
            self.anim_transition[i] = pygame.transform.scale(self.anim_transition[i], (self.width_m, self.height_m))

        # Пауза
        self.font_pause_score = pygame.font.SysFont('Transformers Movie', 150)
        self.font_pause_name = pygame.font.SysFont('Transformers Movie', 50)
        self.font_pause_time = pygame.font.SysFont('Transformers Movie', 90)
        self.font_pause_period = pygame.font.SysFont('Transformers Movie', 40)

        # Строки
        self.all_texts = {
            "ENG": ['THE PUCK OUTSIDE THE PLAYING AREA', 'OFFSIDE', 'ICING', 'GOOOOOOOAL', 'CONTINUE', 'EXIT'],
            "RU": ['ШАЙБА ЗА ПРЕДЕЛАМИ ИГРОВОЙ ПЛОЩАДКИ', 'ВНЕ ИГРЫ', 'ПРОБРОС', 'ГОООООООЛ', 'ПРОДОЛЖИТЬ', 'ВЫХОД']
        }

