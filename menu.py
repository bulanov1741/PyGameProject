import pygame
import pygame_gui


class Menu:
    def __init__(self, width_m, height_m, window_surface, status):
        self.window_surface = window_surface
        self.status = status
        self.manager = pygame_gui.UIManager((width_m, height_m))
        self.background = pygame.Surface((width_m, height_m))
        self.background.fill(pygame.Color('#000000'))

        self.initUI()

    def initUI(self):
        self.start_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                                         text='START GAME',
                                                         manager=self.manager)

    def render(self, dt):
        self.manager.update(dt)
        self.manager.draw_ui(self.window_surface)

    def events(self, event):
        self.manager.process_events(event)
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_game_button:
                    self.status[0] = 1


if __name__ == "__main__":
    pygame.init()
    width_m, height_m = 800, 800
    window_surface = pygame.display.set_mode((width_m, height_m))
    menu = Menu(width_m, height_m, window_surface, [0])
    clock = pygame.time.Clock()
    is_running = True
    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            menu.events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == menu.start_game_button:
                    print('Start!')
            if event.type == pygame.QUIT:
                is_running = False
        window_surface.blit(menu.background, (0, 0))
        menu.render(time_delta)
        pygame.display.update()
