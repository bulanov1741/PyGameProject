import pygame
import pygame_gui
from settings import settings
from LevelChoice import Levels


class Menu:
    def __init__(self, width_m, height_m, screen, dt, data_manager, sound_path):
        self.screen_total_game = screen
        self.level = 0
        self.DataManager = data_manager
        self.sound = sound_path
        self.size = (width_m, height_m)
        self.dt = dt
        self.manager = pygame_gui.UIManager(self.size, 'theme.json')
        self.screen = pygame.Surface(self.size)
        self.running = True
        self.field = pygame.image.load('hockey_field2.jpg').convert_alpha()
        self.volume = float(self.DataManager.get_setting('volume')) / 1000.0

        self.init_music()
        self.initUI()
        self.render()

    def initUI(self):
        self.buttons_size = (self.size[0] // 5, self.size[1] // 10)
        self.x_space = 700
        self.y_space = 50
        self.start_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_space, 200), self.buttons_size),
            text='START GAME',
            manager=self.manager)
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_space, 200 + self.buttons_size[1] + self.y_space), self.buttons_size),
            text='SETTINGS',
            manager=self.manager)
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_space, 200 + 2 * self.buttons_size[1] + 2 * self.y_space),
                                      self.buttons_size),
            text='EXIT',
            manager=self.manager)

    def init_music(self):
        volume = float(self.DataManager.get_setting('volume')) / 1000.0
        self.sound.set_volume(volume)
        self.sound.play()

    def update_volume_music(self):
        self.volume = float(self.DataManager.get_setting('volume')) / 1000.0
        self.sound.set_volume(self.volume)

    def render(self):
        while self.running:
            self.screen.blit(self.field, (0, 0))
            self.screen_total_game.blit(self.screen, (0, 0))

            self.update_volume_music()

            self.manager.update(self.dt)
            self.manager.draw_ui(self.screen_total_game)

            self.events()

            pygame.display.flip()

    def check_level(self):
        return self.level

    def events(self):
        for event in pygame.event.get():
            self.manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_game_button:
                    level_page = Levels(*self.size, self.screen_total_game, self.dt, self.DataManager, self.sound)
                    self.level = level_page.check_level()
                    if self.level:
                        self.running = False
                if event.ui_element == self.settings_button:
                    settings(*self.size, self.screen_total_game, self.dt, self.DataManager)
                if event.ui_element == self.exit_button:
                    self.running = False
                    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    width_m, height_m = 800, 800
    window_surface = pygame.display.set_mode((width_m, height_m))
    clock = pygame.time.Clock()
    dt = clock.tick(60) / 1000
    Menu(width_m, height_m, window_surface, dt)
