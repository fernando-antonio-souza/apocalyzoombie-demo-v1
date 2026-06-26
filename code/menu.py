import pygame
from code.consts import WIDTH, HEIGHT, COLOR_WHITE, COLOR_YELLOW, COLOR_BLACK, MENU_OPTIONS

class Menu:


    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load(r"./assets/background/background_menu.png").convert_alpha()
        self.rect = self.surf.get_rect(left= 0, top= 0)
        self.clock = pygame.time.Clock()
        self.selected_option = 0

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("./assets/sounds/menu_music.mp3")
            pygame.mixer.music.play(-1)

    # Roda a tela do menu
    def run_menu(self):
        


        FPS = 60

        while True:
            
            # Cria a imagem de background do menu
            resize_image = pygame.transform.scale(self.surf, (WIDTH, HEIGHT))
            self.window.blit(resize_image, (0, 0))

            # Cria o titulo do jogo no menu
            title_font = pygame.font.SysFont("Arial", 24)
            title_text = title_font.render("APOCALYZOOMBIE", True, (COLOR_BLACK))
            title_rect = title_text.get_rect(center= (WIDTH // 2, HEIGHT // 4))
            self.window.blit(title_text, title_rect)

            # Cria o texto das opções do menu
            menu_options_font = pygame.font.SysFont("Arial", 14)

            for i, option in enumerate(MENU_OPTIONS):
                color = COLOR_YELLOW if i == self.selected_option else COLOR_WHITE
                text = menu_options_font.render(option, True, color)
                text_rect = text.get_rect(center= (WIDTH // 2, HEIGHT // 2 + i * 30))
                self.window.blit(text, text_rect)

            controls_font = pygame.font.SysFont("Arial", 12)
            controls = [
                "MOVER:  SETAS DIRECIONAIS",
                "ATIRAR:  SPACE",
            ]
            for j, line in enumerate(controls):
                ctrl_text = controls_font.render(line, True, COLOR_WHITE)
                ctrl_rect = ctrl_text.get_rect(center=(WIDTH // 2, HEIGHT - 50 + j * 18))
                self.window.blit(ctrl_text, ctrl_rect)

            self.clock.tick(FPS)

            pygame.display.flip()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(MENU_OPTIONS)

                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(MENU_OPTIONS)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:
                            return
                        elif self.selected_option == 1:
                            pygame.quit()
                            quit()
