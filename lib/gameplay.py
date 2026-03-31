import time
from lib.scene import Scene
import pygame
from lib.core.dealer import Dealer
from lib.core.player import Player
from enum import Enum, auto

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

        self.state_machine = GameplayStateMachine()
        self.states = {
            GameStates.DEALER_PLACE_CARDS: DealerPlaceCards(self.state_machine, self),
            GameStates.USER_HIT_OR_STAND: UserHitOrStand(self.state_machine, self)
        }

        self.bg_image = pygame.image.load("./assets/game/table.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (1920, 1080))

        self.hidden_card = None
        self.visible_card = None

        self.player_card_1 = None
        self.player_card_2 = None
    
    def draw_hidden_and_visible_card(self):
        self.screen.blit(self.hidden_card.rear_side, (800, 300))
        self.screen.blit(self.visible_card.front_side, (1000, 300))

    def draw_player_cards(self):
        self.screen.blit(self.player_card_1.front_side, (800, 650))
        self.screen.blit(self.player_card_2.front_side, (1000, 650))

    def run(self):
        my_font = pygame.font.SysFont('Inter', 30)
        text_surface = my_font.render("Game Here", True, (255, 255, 255))
        self.screen.blit(text_surface, (0, 0))
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
        # time.sleep(1)
        self.game_state_manager.set_state(GameStates.USER_HIT_OR_STAND)


class UserHitOrStand:
    def __init__(self, game_state_manager, gameplay: Gameplay):
        self.game_state_manager = game_state_manager
        self.gameplay = gameplay
    
    def run(self):
        pass