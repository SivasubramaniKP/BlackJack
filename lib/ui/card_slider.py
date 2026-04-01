from lib.ui.card import Card
from typing import List

CARD_HEIGHT = 190
CARD_WIDTH = 140

class CardSlider:

    def __init__(self, screen, y_axis, gap = 20):
        self.screen = screen
        self.y_axis = y_axis
        self.cards: List[Card] = []
        self.n = 0
        self.gap = gap
        # self.starting_x = starting_x
    
    def add_card(self, card:Card):
        self.cards.append(card)
        self.n += 1
    
    def render(self):

        if self.n % 2 == 0:
            x = (CARD_WIDTH/2) + (self.n/2 - 1)*(self.gap + CARD_WIDTH) + (self.gap/2)
            x = 1920/2 - x
            print(self.n)

            for card in self.cards:
                card.card_rect.center = (x, self.y_axis)
                if card.visible:
                    self.screen.blit(card.front_side, card.card_rect)
                else:
                    self.screen.blit(card.rear_side, card.card_rect)

                x = x + CARD_WIDTH + self.gap
            
        else:
            x = CARD_WIDTH + (self.n//2 * self.gap) + (self.n//2 - 1) * CARD_WIDTH
            x = 1920/2 - x
            print("if n is odd X = ", x)

            for card in self.cards:
                card.card_rect.center = (x, self.y_axis)
                if card.visible:
                    self.screen.blit(card.front_side, card.card_rect)
                else:
                    self.screen.blit(card.rear_side, card.card_rect)

                x = x + CARD_WIDTH + self.gap



