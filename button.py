import pygame


class Button:
    def __init__(self, x, y, width, height, text='', color=(0, 0, 0), hover_color=(50, 70, 90)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont('Arial', 50)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        self.width, self.height = self.text_rect.size

    def draw(self, screen, main):
        # Проверяем, находится ли мышь над кнопкой
        mouse_pos = (pygame.mouse.get_pos()[0] - (main.width_m - main.pause_image.size[0]) // 2, \
                     pygame.mouse.get_pos()[1] - (main.height_m - main.pause_image.size[1]) // 2)
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # Отображаем текст на кнопке
        screen.blit(self.text_surface, self.text_rect)

class Icon(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)