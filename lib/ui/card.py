from enum import Enum, auto
from typing import Literal
from lib.ui.game_enums import Suite, Rank, RearColor
import pygame

class Card:

    def __init__(self,
        suite: Suite,
        rank: Rank,
        rear_color: RearColor = RearColor.BLUE,
        variant: Literal[1, 2, 3, 4, 5] = 2
    ):
        self.suite = suite
        self.rank = rank

        front_side_file_location = "./assets/PNG/Cards/card" + str(suite.value) + str(rank.value) + ".png"
        rear_side_file_location = "./assets/PNG/Cards/cardBack_" + rear_color.value + str(variant) + ".png"
        
        self.front_side = pygame.image.load(front_side_file_location)
        self.rear_side = pygame.image.load(rear_side_file_location)


       
    def __str__(self):
        return str(self.suite.value) + " " + str(self.rank.value) + "\n"