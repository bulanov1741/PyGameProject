import pygame
import pygame_gui
import sys

class Levels:
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

        self.initUI()
        self.render()

    def initUI(self):
        self.buttons_size = (self.size[0] // 5, self.size[1] // 10)
        self.x_space = 700
        self.y_space = 50
        self.level_1_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_space, 200), self.buttons_size),
            text='LEVEL 1',
            manager=self.manager)
        self.level_2_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_space, 200 + self.buttons_size[1] + self.y_space), self.buttons_size),
            text='LEVEL 2',
            manager=self.manager)
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_space, 200 + 2 * (self.buttons_size[1] + self.y_space)), self.buttons_size),
            text='Back',
            manager=self.manager)

    def check_level(self):
        return self.level

    def render(self):
        while self.running:
            self.screen.blit(self.field, (0, 0))
            self.screen_total_game.blit(self.screen, (0, 0))
            self.manager.update(self.dt)
            self.manager.draw_ui(self.screen_total_game)
            self.events()
            pygame.display.flip()

    def choice_level(self, level):
        self.level = level
        self.sound.stop()
        del self.sound
        self.running = False

    def events(self):
        for event in pygame.event.get():
            self.manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.back_button:
                    self.level = 0
                    self.running = False
                if event.ui_element == self.level_1_button:
                    self.choice_level(1)
                if event.ui_element == self.level_2_button:
                    self.choice_level(2)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()