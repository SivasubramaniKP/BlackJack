from lib.ui.card import Card
from lib.ui.game_enums import *
from typing import Literal

class Deck():

    def __init__(self, rear_color: RearColor, card_rear_variant: Literal[1, 2, 3, 4, 5]):

        self.Cards = []

        for suite in Suite:
            for rank in Rank:
                self.Cards.append(Card(suite, rank, rear_color, card_rear_variant))

