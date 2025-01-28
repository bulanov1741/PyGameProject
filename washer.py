import pygame
import math


class Washer:
    def __init__(self, x, y, radius, borders, main, speed=0, angle=0):
        self.b_w, self.b_h = borders
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = angle
        # self.angle = math.radians(angle)  # угол в радианах из градусов
        self.dx = self.speed * math.cos(self.angle)  # Компоненты скорости по оси X
        self.dy = self.speed * math.sin(self.angle)  # Компоненты скорости по оси Y

        self.main = main  # Класс с игрой

    def move(self, dt):
        self.x += self.dx * dt  # dt = clock.tick(fps) / 1000 - сколько времени прошло с последнего рендера кадра (16 мс)
        self.y += self.dy * dt
        self.bounce()
        self.loss_speed()

    def loss_speed(self):
        self.speed = self.speed * (1 - (0.1 / (1000 / 16)))  # скорость уменьшается на 10% в секудну
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)

    def strike(self, speed, angle):
        self.speed = speed
        self.angle = angle
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)

    def bounce(self):
        # Столкновение с левой или правой границей (по оси X)
        if self.x - self.radius <= 180 or self.x + self.radius >= self.b_w:
            self.dx = -self.dx  # Инвертируем скорость по оси X

        # Столкновение с верхней или нижней границей (по оси Y)
        if self.y - self.radius <= 105 or self.y + self.radius >= self.b_h:
            self.dy = -self.dy  # Инвертируем скорость по оси Y

        # Столкновения с воротами
        if 866 <= self.x <= 990 and (
                303 - self.radius <= self.y == 303 + self.radius or 2951 - self.radius <= self.y <= 2951 + self.radius):
            self.goal()

        else:
            if 863 <= self.x <= 1002 and (
                    236 - self.radius <= self.y == 236 + self.radius or 3018 - self.radius <= self.y <= 3018 + self.radius):
                self.dy = -self.dy

            if (236 <= self.y <= 303 or 2951 <= self.y <= 3018) and (
                    863 - self.radius <= self.x <= 863 + self.radius or 1002 - self.radius <= self.x <= 1002 + self.radius):
                self.dx = -self.dx

        # Столкновение с игроками
        for i in self.main.players_own + self.main.players_opponent:
            if i != self.main.chosen_player and i != self.main.owning_washer:
                if i.y <= self.y <= i.y + 100 and (
                        self.x - self.radius <= i.x <= self.x + self.radius or self.x - self.radius <= i.x + 100 <= self.x + self.radius):
                    self.dx = -self.dx
                    break
                if i.x <= self.x <= i.x + 100 and (
                        self.y - self.radius <= i.y <= self.y + self.radius or self.y - self.radius <= i.y + 100 <= self.y + self.radius):
                    self.dy = -self.dy
                    break

        # Обновляем угол после инверсии
        self.angle = math.atan2(self.dy, self.dx)  # угол между вектором (dx, dy) и осью x

    def draw(self, screen):
        pygame.draw.circle(screen, 'black', (int(self.x), int(self.y)), self.radius)

    def goal(self):
        print('GOOOOOAL')


# проверка
def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    screen.fill('white')
    clock = pygame.time.Clock()
    clicked = False
    running = True

    while running:
        dt = clock.tick(60) / 1000  # dt в секундах
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                washer = Washer(x, y, 20, (width, height), 10 ** 3, float(math.radians(310)))
                clicked = True

        if clicked:
            screen.fill('white')
            washer.move(dt)
            washer.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
