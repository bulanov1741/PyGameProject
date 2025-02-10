import pygame


class Const:
    def __init__(self):
        # Вбрасывания
        self.face_off_centre = (935, 1630)  # Центр
        self.face_off_blue_1 = (600, 1260)  # Около синей линии
        self.face_off_blue_2 = (1265, 1260)
        self.face_off_blue_3 = (600, 1995)
        self.face_off_blue_4 = (1265, 1995)
        self.face_off_zone_1 = (600, 640)  # В зоне
        self.face_off_zone_2 = (1265, 640)
        self.face_off_zone_3 = (600, 2610)
        self.face_off_zone_4 = (1265, 2610)
        self.face_offs = [self.face_off_centre, self.face_off_blue_1, self.face_off_blue_2, self.face_off_blue_3,
                          self.face_off_blue_4, self.face_off_zone_1, self.face_off_zone_2, self.face_off_zone_3,
                          self.face_off_zone_4]

        # Границы поля
        self.min_x = 180
        self.max_x = 1685
        self.min_y = 105
        self.max_y = 3155

        # Линии
        self.icing_line_1 = 303  # Проброса / лицевые
        self.icing_line_2 = 2950
        self.blue_line_1 = (1178, 1196)
        self.blue_line_2 = (2076, 2058)
        self.centre_line = 1627

        # Ситуации
        self.font_situation = pygame.font.SysFont('Bleeker Rus (Fixed)', 120)
        self.offside_state = 0  # Предофсайдное
        self.icing_state = [0, 0]  # Предпробросное
        self.start = 1  # Предначальное

        # Счет
        self.our_score = 0
        self.opponent_score = 0
        self.font_score = pygame.font.SysFont('Transformers Movie', 60)
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

        # Последние 5 секунд
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
