import random
from lib.core.deck import Deck
from lib.ui.game_enums import *
from lib.ui.card import Card
class Dealer:

    def __init__(self, screen):
        self.screen = screen
        self.deck = Deck(RearColor.BLUE, 2)
        self.cur_sum = 0

        self.hidden_card: Card = None
        self.visible_card: Card = None
        self.user_card_1: Card = None
        self.user_card_2: Card = None

    def get_card(self):
        card = random.choice(self.deck.Cards)
        self.deck.Cards.remove(card)
        return card

    def place_cards(self):

        self.hidden_card, self.visible_card = self.get_card(), self.get_card()
        self.cur_sum = points_translator(self.hidden_card) + points_translator(self.visible_card)
        # BLIT THE CARD TO THE SCREEN

    def get_player_cards(self):

        return [self.get_card(), self.get_card()]
    
    def get_hit_cards(self):

        return self.get_card()

    def hit_or_stand(self):
        if self.cur_sum < 15:
            return "HIT"
        else:
            return "STAND"


