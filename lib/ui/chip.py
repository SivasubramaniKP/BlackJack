
import pygame
from typing import Literal


class Chip:

    def __init__(self, screen, value: Literal[5000, 1000, 500, 200, 100, 50]):
        self.value = value
        assets_location = "./assets/PNG/Chips/"

        self.chip_front = pygame.image.load(assets_location + str(value) + "_front.png")
        self.chip_side = pygame.image.load(assets_location + str(value) + "_side.png")

        self.chip_front_rect = self.chip_front.get_rect()
        self.chip_side_rect = self.chip_side.get_rect()

        self.screen = screen
    

    def render_front(self, center):
        self.chip_front_rect.center = center

        self.screen.blit(self.chip_front, self.chip_front_rect)

    def render_side(self, center):
        self.chip_side_rect.center = center

        self.screen.blit(self.chip_side, self.chip_side_rect)


