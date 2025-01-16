import pygame
import pygame_gui


class Menu:
    def __init__(self, width_m, height_m, screen, dt):
        self.screen_total_game = screen
        self.dt = dt
        self.manager = pygame_gui.UIManager((width_m, height_m))
        self.screen = pygame.Surface((width_m, height_m))
        self.screen.fill(pygame.Color('#000000'))
        self.running = True

        self.initUI()
        self.render()

    def initUI(self):
        self.start_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                                         text='START GAME',
                                                         manager=self.manager)

    def render(self):
        while self.running:
            self.manager.update(self.dt)
            self.manager.draw_ui(self.screen_total_game)
            self.events()
            pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            self.manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_game_button:
                    self.running = False


if __name__ == "__main__":
    pygame.init()
    width_m, height_m = 800, 800
    window_surface = pygame.display.set_mode((width_m, height_m))
    clock = pygame.time.Clock()
    dt = clock.tick(60) / 1000
    Menu(width_m, height_m, window_surface, dt)