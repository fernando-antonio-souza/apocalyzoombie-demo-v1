import pygame
from code.consts import WIDTH, HEIGHT, COLOR_WHITE
from code.menu import Menu
from code.level import Level


class Game:

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.menu = Menu(self.window)

    def show_end_screen(self, message, color):
        font_big = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 24)
        text = font_big.render(message, True, color)
        tip = font_small.render("Press SPACE to continue", True, COLOR_WHITE)
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    wait = False
            self.window.fill((0, 0, 0))
            self.window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 40))
            self.window.blit(tip, (WIDTH // 2 - tip.get_width() // 2, HEIGHT // 2 + 20))
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def run(self):
        while True:
            self.menu.run_menu()
            level = Level(self.window)
            result = level.run()
            if result == "win":
                self.show_end_screen("YOU WIN!", (0, 255, 0))
            elif result == "lose":
                self.show_end_screen("GAME OVER", (255, 0, 0))
