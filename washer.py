import pygame
import math


class Washer:
    def __init__(self, x, y, radius, borders, speed=0, angle=0):
        self.b_w, self.b_h = borders
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = angle
        # self.angle = math.radians(angle)  # угол в радианах из градусов
        self.dx = self.speed * math.cos(self.angle)  # Компоненты скорости по оси X
        self.dy = self.speed * math.sin(self.angle)  # Компоненты скорости по оси Y

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
        if self.x - self.radius <= 0 or self.x + self.radius >= self.b_w:
            self.dx = -self.dx  # Инвертируем скорость по оси X

        # Столкновение с верхней или нижней границей (по оси Y)
        if self.y - self.radius <= 0 or self.y + self.radius >= self.b_h:
            self.dy = -self.dy  # Инвертируем скорость по оси Y

        # Обновляем угол после инверсии
        self.angle = math.atan2(self.dy, self.dx)  # угол между вектором (dx, dy) и осью x

    def draw(self, screen):
        pygame.draw.circle(screen, 'black', (int(self.x), int(self.y)), self.radius)


# проверка
def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
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
                washer = Washer(x, y, 20, (width, height), 10 ** 3, 120)
                clicked = True

        if clicked:
            screen.fill('black')
            washer.move(dt)
            washer.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
