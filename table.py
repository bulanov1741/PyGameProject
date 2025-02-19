# проверка
import pygame
import screeninfo


class Table:
    def __init__(self, width, height, screen):
        self.width, self.height = width, height
        self.screen = pygame.Surface((self.width, 40 * 39))
        self.total_screen = screen
        self.running = True
        self.font = pygame.font.SysFont('comicsans', 30)
        self.scrolling = 0

        # Считываем результаты из файла teams.csv
        with open('teams.csv', "r", encoding="utf_8_sig") as file:
            self.teams = sorted([i.strip().split(';') for i in file.readlines()[1:]], key=lambda x: x[4])

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    self.scrolling = max(0, self.scrolling - 1)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 and self.height // 40 - 2 < 39:
                    self.scrolling = min(39 - (self.height // 40), self.scrolling + 1)

            mouse_pos = pygame.mouse.get_pos()[1] + self.scrolling * 40
            for i in range(39):

                if i == 0:
                    pygame.draw.rect(self.screen, (150, 150, 150), (0, i * 40, self.width, 40 * (i + 1)))
                    number = self.font.render(str('№'), False, 'white')
                    name = self.font.render("Club", False, 'white')
                    games = self.font.render("GP", False, 'white')
                    victories = self.font.render("W", False, 'white')
                    defeats = self.font.render("L", False, 'white')
                    pts = self.font.render("PTS", False, 'white')
                else:
                    if mouse_pos // 40 == i:
                        pygame.draw.rect(self.screen, (100, 100, 100), (0, i * 40, self.width, 40 * (i + 1)))
                    else:
                        pygame.draw.rect(self.screen, 'black', (0, i * 40, self.width, 40 * (i + 1)))
                    pygame.draw.line(self.screen, 'white', (0, 40 * i), (width, 40 * i))

                    number = self.font.render(str(i), False, 'white')
                    name = self.font.render(str(self.teams[i - 1][0]), False, 'white')
                    games = self.font.render(str(self.teams[i - 1][1]), False, 'white')
                    victories = self.font.render(str(self.teams[i - 1][2]), False, 'white')
                    defeats = self.font.render(str(self.teams[i - 1][3]), False, 'white')
                    pts = self.font.render(str(self.teams[i - 1][4]), False, 'white')
                number_rect = number.get_rect(center=(width // 40, 40 * i + 20))
                name_rect = name.get_rect(center=(width // 40 * 11, 40 * i + 20))
                games_rect = games.get_rect(center=(width // 20 * 13, 40 * i + 20))
                victories_rect = victories.get_rect(center=(width // 20 * 15, 40 * i + 20))
                defeats_rect = defeats.get_rect(center=(width // 20 * 17, 40 * i + 20))
                pts_rect = pts.get_rect(center=(width // 20 * 19, 40 * i + 20))
                self.screen.blit(number, number_rect)
                self.screen.blit(name, name_rect)
                self.screen.blit(games, games_rect)
                self.screen.blit(victories, victories_rect)
                self.screen.blit(defeats, defeats_rect)
                self.screen.blit(pts, pts_rect)


            x = width // 20
            pygame.draw.line(self.screen, 'white', (x, 0), (x, 40 * 39))
            pygame.draw.line(self.screen, 'white', (12 * x, 0), (12 * x, 40 * 39))
            pygame.draw.line(self.screen, 'white', (14 * x, 0), (14 * x, 40 * 39))
            pygame.draw.line(self.screen, 'white', (16 * x, 0), (16 * x, 40 * 39))
            pygame.draw.line(self.screen, 'white', (18 * x, 0), (18 * x, 40 * 39))

            self.total_screen.blit(self.screen, (0, -1 * self.scrolling * 40))
            pygame.display.flip()





def main():
    pygame.init()
    width = screeninfo.get_monitors()[0].width
    height = screeninfo.get_monitors()[0].height
    screen = pygame.display.set_mode((width, height))
    Table(width, height, screen)






if __name__ == "__main__":
    main()
