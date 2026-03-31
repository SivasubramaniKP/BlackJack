import time
from lib.scene import Scene
import pygame
from lib.core.dealer import Dealer
from lib.core.player import Player
from enum import Enum, auto
from lib.ui.button import Button
from lib.ui.text_board import TextBoard
from lib.ui.game_enums import *
class GameStates(Enum):
    DEALER_PLACE_CARDS = auto()
    USER_HIT_OR_STAND = auto()

def getTextSurface(font_size = 20, text= "hello", color=(255, 255, 255), position=(0, 0)):
    text_surf = pygame.font.Font("./assets/font/Precious.ttf", font_size).render(text, True, color)
    text_rect = text_surf.get_rect()
    text_rect.topleft = position

    return {
        "text_surf": text_surf,
        "text_rect": text_rect
    }

class GameplayStateMachine:

    def __init__(self):
        self.cur_state = GameStates.DEALER_PLACE_CARDS
    
    def get_state(self):
        return self.cur_state

    def set_state(self, new_state):
        self.cur_state = new_state

class Gameplay(Scene):
    def __init__(self, screen, game_state_manager):
        super().__init__(screen, game_state_manager)

        self.player = Player(screen, 1000)
        self.dealer = Dealer(screen)

        self.hidden_card = None
        self.visible_card = None

        self.player_card_1 = None
        self.player_card_2 = None

        self.state_machine = GameplayStateMachine()
        self.states = {
            GameStates.DEALER_PLACE_CARDS: DealerPlaceCards(self.state_machine, self),
            GameStates.USER_HIT_OR_STAND: UserHitOrStand(self.state_machine, self)
        }

        self.bg_image = pygame.image.load("./assets/game/table.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (1920, 1080))

    
    def draw_hidden_and_visible_card(self):
        self.screen.blit(self.hidden_card.rear_side, (800, 300))
        self.screen.blit(self.visible_card.front_side, (1000, 300))

    def draw_player_cards(self):
        self.screen.blit(self.player_card_1.front_side, (800, 650))
        self.screen.blit(self.player_card_2.front_side, (1000, 650))

    def run(self):
        self.screen.blit(self.bg_image, (0, 0))
        if self.hidden_card and self.visible_card and self.player_card_1 and self.player_card_2: 
            self.draw_hidden_and_visible_card()
            self.draw_player_cards()
        self.states[self.state_machine.get_state()].run()


class DealerPlaceCards:

    def __init__(self, game_state_manager: GameplayStateMachine, gameplay: Gameplay):
        self.gameplay = gameplay
        self.game_state_manager = game_state_manager

    def run(self):
        self.gameplay.hidden_card, self.gameplay.visible_card = self.gameplay.dealer.place_cards()
        self.gameplay.player_card_1, self.gameplay.player_card_2 = self.gameplay.dealer.get_player_cards()

        text = getTextSurface(100, "Dealer Places the cards", (255, 255, 255), (300, 0))
        self.gameplay.screen.blit(text['text_surf'], text['text_rect'])
        self.game_state_manager.set_state(GameStates.USER_HIT_OR_STAND)


class UserHitOrStand:
    def __init__(self, game_state_manager, gameplay: Gameplay):
        self.game_state_manager = game_state_manager
        self.gameplay = gameplay
        self.screen = self.gameplay.screen
        self.hit_button = Button(self.gameplay.screen).set_background("").set_font(None).set_height(100).set_width(300).set_text("Hit").set_position((300, 475)).prepare()
        self.stand_button = Button(self.gameplay.screen).set_background("").set_font(None).set_height(100).set_width(300).set_text("Stand").set_position((1300, 475)).prepare()

        # mid_x = (self.gameplay.visible_card.width + 200)//2
        # mid_y = 950

        self.current_hand = TextBoard(self.screen).set_background("").set_font(None).set_height(100).set_width(500).set_text("Current hand").set_position((0, 0)).prepare()
        # self.current_hand.bg_rect.center = (mid_x, mid_y)mid_i
        # print("Text of the board", self.current_hand.text)
    
    def count_points_in_hand(self):
        current_hand = points_translator(self.gameplay.player_card_1.rank) + points_translator(self.gameplay.player_card_2.rank)
        if current_hand == 21:
            return "Black Jack"
        if current_hand > 21:
            if self.gameplay.player_card_1.rank == Rank.ACE or self.gameplay.player_card_2.rank == Rank.ACE:
                return current_hand - 10
        return current_hand

    def change_current_hand_text(self, text):
        self.current_hand = self.current_hand.set_text(text).prepare()

    def current_hand_render(self, text):
        mid_x = (1000 + self.gameplay.visible_card.width + 800)//2
        mid_y = 950

        if not text:
            text = "Current hand = " + str(self.count_points_in_hand())

        self.current_hand = self.current_hand.set_text(text).prepare()

        self.current_hand.bg_rect.center = (mid_x, mid_y)
        self.current_hand.render()

    def run(self):
        self.hit_button.render()
        self.stand_button.render()
        self.current_hand_render(None)
        self.handle_event()
        pygame.draw.rect(self.screen, (255, 0, 0), self.hit_button.bg_rect, 5)
        pygame.draw.rect(self.screen, (0, 255, 0), self.stand_button.bg_rect, 5)
        # pygame.draw.rect(self.screen, (255, 0, 0), self., 2)

    def handle_event(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.hit_button.is_mouse_over():
                        self.current_hand_render("Hit button is pressed")
                        print("PRESSING HIT BUTTON")
    
        
        if self.hit_button.is_mouse_over():
            pass