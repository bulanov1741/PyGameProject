class Const:
    def __init__(self):
        # Взбрасывания
        self.face_off_centre = (935, 1630) # Центр
        self.face_off_blue_1 = (600, 1260) # Около синей линии
        self.face_off_blue_2 = (1265, 1260)
        self.face_off_blue_3 = (600, 1995)
        self.face_off_blue_4 = (1265, 1995)
        self.face_off_zone_1 = (600, 640) # В зоне
        self.face_off_zone_2 = (1265, 640)
        self.face_off_zone_3 = (600, 2610)
        self.face_off_zone_4 = (1265, 2610)

        # Границы поля
        self.min_x = 180
        self.max_x = 1685
        self.min_y = 105
        self.max_y = 3155

        # Линии
        self.icing_line_1 = 303 # Проброса / лицевые
        self.icing_line_2 = 2950
        self.blue_line_1 = (1178, 1196)
        self.blue_line_2 = (2076, 2058)
        self.centre_line = 1627

        # Ситуации
        self.offside_state = 0 # Предофсайдное
        self.icing_state = 0 # Предпробросное



