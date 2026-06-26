import pygame
from code.consts import WIDTH, HEIGHT



class Background:

    def __init__(self, window):
        self.window = window
        self.layers = [
            pygame.transform.scale(
                pygame.image.load(f"./assets/background/level1BG{i}.png").convert_alpha(),
                (WIDTH, HEIGHT)
            )
            for i in range(4)
        ]

        self.speeds = [0.1, 0.3, 0.5, 0.7, 1.0]


    def draw(self, camera_x=0):
        for i, layer in enumerate(self.layers):
            offset = (-camera_x * self.speeds[i]) % WIDTH
            self.window.blit(layer, (offset, 0))
            self.window.blit(layer, (offset - WIDTH, 0))

