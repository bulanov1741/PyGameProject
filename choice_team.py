import pygame
import screeninfo


class Choice_Team:
    def __init__(self, width, height, screen, lang):
        self.width, self.height = width, height
        self.h_elem = max(40, self.height // 20)
        self.screen = pygame.Surface((self.width, self.h_elem * 18))
        self.total_screen = screen
        self.running = True
        self.font = pygame.font.SysFont('comicsans', 30)
        self.scrolling = 0
        self.choice_team = ''
        self.lang = lang
        self.all_texts = {
            "ENG": ['Choose the team', 'SAVE'],
            "RU": ['Выбор команды', 'СОХРАНИТЬ']
        }

        # Считываем результаты из файла teams.csv
        with open('teams.csv', "r", encoding="utf_8_sig") as file:
            self.teams = [i.strip().split(';') for i in file.readlines()[1:]]

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if pygame.mouse.get_pos()[1] > self.height - self.h_elem: # Сохранить
                        if self.choice_team != '':
                            self.running = False
                    elif pygame.mouse.get_pos()[1] > self.h_elem: # Выбор
                        self.choice_team = self.teams[pygame.mouse.get_pos()[1] // self.h_elem + self.scrolling + 18 * (
                                    pygame.mouse.get_pos()[0] > self.width // 2) - 1][0]
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    self.scrolling = max(0, self.scrolling - 1)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 and self.height // self.h_elem - 2 < 18:
                    self.scrolling = min(17 - (self.height // self.h_elem - 2), self.scrolling + 1)

            mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + self.scrolling * self.h_elem)
            for i in range(19):
                if self.choice_team == self.teams[i][0]:
                    pygame.draw.rect(self.screen, (150, 150, 150), (0, i * self.h_elem, self.width // 2, self.h_elem * (i + 1)))
                elif self.choice_team == self.teams[i + 18][0]:
                    pygame.draw.rect(self.screen, (150, 150, 150),
                                     (self.width // 2, i * self.h_elem, self.width, self.h_elem * (i + 1)))
                elif mouse_pos[1] // self.h_elem == i + 1:
                    if mouse_pos[0] > self.width // 2:
                        pygame.draw.rect(self.screen, (100, 100, 100),
                                         (self.width // 2, i * self.h_elem, self.width, self.h_elem * (i + 1)))
                    else:
                        pygame.draw.rect(self.screen, (100, 100, 100), (0, i * self.h_elem, self.width // 2, self.h_elem * (i + 1)))
                else:
                    pygame.draw.rect(self.screen, 'black', (0, i * self.h_elem, self.width, self.h_elem * (i + 1)))
                pygame.draw.line(self.screen, 'white', (0, self.h_elem * i), (width, self.h_elem * i))

                name_1 = self.font.render(str(self.teams[i - 1][6 * (self.lang == 'ENG')]), False, 'white')
                name_2 = self.font.render(str(self.teams[i - 1 + 18][6 * (self.lang == 'ENG')]), False, 'white')
                name_1_rect = name_1.get_rect(center=(width // 4, self.h_elem * (i - 1) + (self.h_elem // 2)))
                name_2_rect = name_2.get_rect(center=(width // 4 * 3, self.h_elem * (i - 1) + (self.h_elem // 2)))
                self.screen.blit(name_1, name_1_rect)
                self.screen.blit(name_2, name_2_rect)
            pygame.draw.line(self.screen, 'white', (width // 2, 0), (width // 2, self.h_elem * 18))
            self.total_screen.blit(self.screen, (0, -1 * self.scrolling * self.h_elem + self.h_elem))
            # Выбор команды
            pygame.draw.rect(self.total_screen, (150, 150, 150), (0, 0, self.width, self.h_elem))
            name = self.font.render(self.all_texts[self.lang][0], False, 'white')
            name_rect = name.get_rect(center=(self.width // 2, (self.h_elem // 2)))
            self.total_screen.blit(name, name_rect)
            # Сохранить
            pygame.draw.rect(self.total_screen, (150, 150, 150),
                             (0, self.height - self.h_elem, self.width, self.height))
            name = self.font.render(self.all_texts[self.lang][1], False, 'white')
            name_rect = name.get_rect(center=(self.width // 2, self.height - (self.h_elem // 2)))
            self.total_screen.blit(name, name_rect)
            pygame.display.flip()


def main():
    pygame.init()
    width = screeninfo.get_monitors()[0].width
    height = screeninfo.get_monitors()[0].height
    screen = pygame.display.set_mode((width, height))
    Choice_Team(width, height, screen)


if __name__ == "__main__":
    main()
