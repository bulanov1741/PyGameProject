import pygame
import pygame_gui


class settings:
    def __init__(self, width_m, height_m, screen, dt, data_manager, lang):
        self.screen_total_game = screen
        self.lang = lang
        self.all_texts = {
            "ENG":["Sound", "Language", "BACK", "SAVE"],
            "RU":["Звук", "Язык", "НАЗАД", "Сохранить"]
        }
        if self.lang == 'RU':
            self.language = 'Русский'
        else:
            self.language = 'English'
        self.DataManager = data_manager
        self.size = (width_m, height_m)
        self.dt = dt
        self.manager = pygame_gui.UIManager(self.size, "theme.json")
        self.screen = pygame.Surface(self.size)
        self.running = True
        self.field = pygame.surface.Surface(self.size)
        self.field.fill('white')

        self.initUI()
        self.render()

    def initUI(self):
        self.buttons_size = (self.size[0] // 5, self.size[1] // 10)
        self.x_space = 100
        self.y_space = 50
        self.container_slider_1 = pygame_gui.elements.ui_selection_list.UIContainer(
            pygame.Rect(700, 200, 1000, 55),
            manager=self.manager)
        self.text_slider_1 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (200, 50)),
            text=self.all_texts[self.lang][0],
            container=self.container_slider_1,
            manager=self.manager
        )
        self.text_slider_2 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((700, 251), (200, 100)),
            text=self.all_texts[self.lang][1],
            manager=self.manager
        )
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_space, 200), self.buttons_size),
            text=self.all_texts[self.lang][2],
            manager=self.manager)
        self.language_menu = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((900, 251), (500, 100)),
            options_list=[("English","3"), ("Русский","3")],
            starting_option=(self.language,"3"),
            manager=self.manager)
        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_space, 200 + self.buttons_size[1] + self.y_space), self.buttons_size),
            text=self.all_texts[self.lang][3],
            manager=self.manager)
        self.slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((200, 0), (500, 50)),
            start_value=int(self.DataManager.get_setting("volume")),
            value_range=(0, 100),
            container=self.container_slider_1,
            manager=self.manager
        )


    def render(self):
        while self.running:
            self.screen.blit(self.field, (0, 0))
            self.screen_total_game.blit(self.screen, (0, 0))
            self.manager.update(self.dt)
            self.manager.draw_ui(self.screen_total_game)
            self.events()
            pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            self.manager.process_events(event)
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.back_button:
                    self.running = False
                if event.ui_element == self.save_button:
                    self.DataManager.set_setting("volume", self.slider.get_current_value())
                    self.running = False
                    if self.language_menu.selected_option[0] == 'Русский':
                        self.DataManager.set_setting("language", 'RU')
                    else:
                        self.DataManager.set_setting("language", 'ENG')
