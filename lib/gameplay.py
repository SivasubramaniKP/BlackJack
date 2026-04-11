import time
import random
from scipy.stats import norm
from lib.scene import Scene
import pygame
from lib.core.dealer import Dealer
from lib.core.player import Player
from enum import Enum, auto
from lib.ui.button import Button
from lib.ui.text_board import TextBoard
from lib.ui.game_enums import *
from lib.ui.card_slider import CardSlider
from lib.ui.chip import Chip

class GameStates(Enum):
    DEALER_PLACE_CARDS = auto()
    USER_HIT_OR_STAND = auto()
    PLACE_BETS = auto()
    USER_BUST = auto()

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
        self.cur_state = GameStates.PLACE_BETS
    
    def get_state(self):
        return self.cur_state

    def set_state(self, new_state):
        self.cur_state = new_state


class Gameplay(Scene):
    def __init__(self, screen, game_state_manager):
        super().__init__(screen, game_state_manager)

        self.player = Player(screen)
        self.dealer = Dealer(screen)

        # self.hidden_card = None
        # self.visible_card = None

        # self.player_card_1 = None
        # self.player_card_2 = None


        self.cur_bet = 0


        self.state_machine = GameplayStateMachine()
        self.states = {
            GameStates.DEALER_PLACE_CARDS: DealerPlaceCards(self.state_machine, self),
            GameStates.USER_HIT_OR_STAND: UserHitOrStand(self.state_machine, self),
            GameStates.PLACE_BETS: PlaceBets(self.state_machine, self),
            GameStates.USER_BUST: UserBust(self.state_machine, self)
        }

        self.bg_image = pygame.image.load("./assets/game/table.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (1920, 1080))

    def refresh_state(self, state: GameStates):
        match state:
            case GameStates.PLACE_BETS:
                self.states[state] = PlaceBets(self.state_machine, self)
            case GameStates.USER_BUST:
                self.states[state] = UserBust(self.state_machine, self)
            case GameStates.USER_HIT_OR_STAND:
                self.states[state] = UserHitOrStand(self.state_machine, self)
            case GameStates.DEALER_PLACE_CARDS:
                self.states[state] = DealerPlaceCards(self.state_machine, self)
    
    # def draw_hidden_and_visible_card(self):
    #     self.screen.blit(self.hidden_card.rear_side, (800, 300))
    #     self.screen.blit(self.visible_card.front_side, (1000, 300))

    # def draw_player_cards(self):
    #     self.screen.blit(self.player_card_1.front_side, (800, 650))
    #     self.screen.blit(self.player_card_2.front_side, (1000, 650))

    def run(self, events):
        self.screen.blit(self.bg_image, (0, 0))
        # if self.hidden_card and self.visible_card and self.player_card_1 and self.player_card_2: 
        #     self.draw_hidden_and_visible_card()
        #     self.draw_player_cards()
        # self.dealer_card_slider.render()
        # self.player_card_slider.render()
        self.states[self.state_machine.get_state()].run(events)

class PlaceBets:

    def __init__(self, game_state_manager: GameplayStateMachine, gameplay:Gameplay):
        self.game_state_manager = game_state_manager
        self.gameplay = gameplay
        self.current_bet_text = TextBoard(self.gameplay.screen).set_background("").set_font(None).set_height(100).set_width(400).set_position((1920//2 - 200, 100)).set_text("Current Bet").prepare()
        self.current_bet = TextBoard(self.gameplay.screen).set_background("").set_font(None).set_height(100).set_width(400).set_position((1920//2 - 200, 200)).set_text("$0").prepare()
        self.current_amount = TextBoard(self.gameplay.screen).set_background("").set_font(None).set_height(100).set_width(400).set_position((1920//2 - 200, 900)).set_text("$0").prepare()
        self.cur_bet = 0
        self.bet = Button(self.gameplay.screen).set_background("").set_font(None).set_height(100).set_width(400).set_position((1920//2 - 200, 1080//2 - 50)).set_text("Bet").prepare()

    def render_coins(self):
        height_level = 800
        gap = 30

        chip_width = 64
        chip_height = 64

        n = len(self.gameplay.player.counts)
        x = (chip_width/2) + (6/2 - 1) * (gap + chip_width) + (gap/2) 
        x = 1920//2 - x

        for type in [5000, 1000, 500, 200, 100, 50]:
            chips = self.gameplay.player.chips[type]
            stack = height_level
            for chip in chips:
                chip.render_side((x, stack))
                stack -= 10
            x += chip_width + gap

    def handle_bet(self):
        if self.cur_bet != 0:
            self.gameplay.cur_bet = self.cur_bet
            self.gameplay.refresh_state(GameStates.DEALER_PLACE_CARDS)
            self.game_state_manager.set_state(GameStates.DEALER_PLACE_CARDS)
    
    def handle_event(self, events):
        player_chips = self.gameplay.player.get_all_chips()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for chip in player_chips:
                        if chip.is_mouse_over():
                            self.cur_bet += chip.value
                            self.current_bet.set_text("$" + str(self.cur_bet)).prepare()
                            self.gameplay.player.chips[chip.value].pop()
                            break
                    
                    if self.bet.is_mouse_over():
                        self.handle_bet()

        # mouse_pos = pygame.mouse.get_pos()
        # mouse_button = pygame.mouse.get_pressed()
        # for chip in player_chips:
        #     if mouse_button[0] and chip.is_mouse_over():
        #         self.cur_bet += chip.value
        #         self.current_bet.set_text("$" + str(self.cur_bet)).prepare()



    def run(self, events):
        self.current_bet_text.render()
        self.current_bet.render()
        self.current_amount.set_text("$" + str(self.gameplay.player.sum)).prepare()
        self.current_amount.render()
        self.render_coins()
        self.bet.render()
        self.handle_event(events)
        


class DealerPlaceCards:

    def __init__(self, game_state_manager: GameplayStateMachine, gameplay: Gameplay):
        self.gameplay = gameplay
        self.game_state_manager = game_state_manager
        self.dealer_card_slider = CardSlider(gameplay.screen, 300, 20)
        self.player_card_slider = CardSlider(gameplay.screen, 650, 20)

    def run(self, events):
        hidden_card,visible_card = self.gameplay.dealer.place_cards()
        hidden_card.set_hidden()
        player_card_1, player_card_2 = self.gameplay.dealer.get_player_cards()
        
        self.dealer_card_slider.add_card(hidden_card)
        self.dealer_card_slider.add_card(visible_card)

        self.player_card_slider.add_card(player_card_1)
        self.player_card_slider.add_card(player_card_2)

        self.player_card_slider.render()
        self.dealer_card_slider.render()

        text = getTextSurface(100, "Dealer Places the cards", (255, 255, 255), (300, 0))
        self.gameplay.screen.blit(text['text_surf'], text['text_rect'])
        self.gameplay.refresh_state(GameStates.USER_HIT_OR_STAND)
        self.game_state_manager.set_state(GameStates.USER_HIT_OR_STAND)


class UserHitOrStand:
    def __init__(self, game_state_manager, gameplay: Gameplay):
        self.game_state_manager = game_state_manager
        self.gameplay = gameplay
        self.screen = self.gameplay.screen
        self.hit_button = Button(self.gameplay.screen).set_background("").set_font(None).set_height(100).set_width(300).set_text("Hit").set_position((300, 475)).prepare()
        self.stand_button = Button(self.gameplay.screen).set_background("").set_font(None).set_height(100).set_width(300).set_text("Stand").set_position((1300, 475)).prepare()
        # self.bust_text_board = TextBoard(self.gameplay.screen).set_background("").set_font(None).set_height(100).set_width(500).set_text("Bust").set_position((0, 0)).prepare()
        # self.black_jack_text_board = TextBoard(self.gameplay.screen).set_background("").set_font(None).set_height(100).set_width(500).set_text("Black Jack").set_position((0, 0)).prepare()

        # mid_x = (self.gameplay.visible_card.width + 200)//2
        # mid_y = 950
        self.evaluation_board = TextBoard(self.gameplay.screen).set_background("").set_font(None).set_height(100).set_width(500).set_text("Bust").set_position((0, 0)).prepare()

        self.current_hand = TextBoard(self.screen).set_background("").set_font(None).set_height(100).set_width(500).set_text("Current hand").set_position((0, 0)).prepare()
        # self.current_hand.bg_rect.center = (mid_x, mid_y)mid_i
        # print("Text of the board", self.current_hand.text)

        self.is_evaluation_set = False
        self.MY_EVENT = pygame.USEREVENT + 1
        self.USER_BLACK_JACK = pygame.USEREVENT + 2
        self.DEALER_BLACK_JACK = pygame.USEREVENT + 3
        self.USER_WINS = pygame.USEREVENT + 4
        self.DEALER_WINS = pygame.USEREVENT + 5
        self.USER_BUST = pygame.USEREVENT + 6
        self.DEALER_BUST = pygame.USEREVENT + 7

    def count_points_in_hand(self):
        curr_hand = 0
        for card in self.gameplay.states[GameStates.DEALER_PLACE_CARDS].player_card_slider.cards:
            curr_hand += points_translator(card.rank)

            if card.rank == Rank.ACE and curr_hand > 21:
                curr_hand -= 10
        return curr_hand

    def count_dealer_points_in_hand(self):
        curr_hand = 0
        for card in self.gameplay.states[GameStates.DEALER_PLACE_CARDS].dealer_card_slider.cards:
            curr_hand += points_translator(card.rank)

            if card.rank == Rank.ACE and curr_hand > 21:
                curr_hand -= 10
        return curr_hand

    def change_current_hand_text(self, text):
        self.current_hand = self.current_hand.set_text(text).prepare()

    def current_hand_render(self, text):
        mid_x = 1920//2
        mid_y = 950

        if not text:
            text = "Current hand = " + str(self.count_points_in_hand())

        self.current_hand = self.current_hand.set_text(text).prepare()

        self.current_hand.bg_rect.center = (mid_x, mid_y)
        self.current_hand.render()

    def run(self, events):
        
        self.hit_button.render()
        self.stand_button.render()
        self.current_hand_render(None)
        pygame.draw.rect(self.screen, (255, 0, 0), self.hit_button.bg_rect, 5)
        pygame.draw.rect(self.screen, (0, 255, 0), self.stand_button.bg_rect, 5)
        # pygame.draw.rect(self.screen, (255, 0, 0), self., 2)

        self.gameplay.states[GameStates.DEALER_PLACE_CARDS].player_card_slider.render()
        self.gameplay.states[GameStates.DEALER_PLACE_CARDS].dealer_card_slider.render()

        if self.is_evaluation_set:
            self.evaluation_board.render()

        self.handle_event(events)

    def evaluate(self):
        print("INSIDE EVALUATION")
        player = self.count_points_in_hand()
        dealer = self.count_dealer_points_in_hand()
        print(player, dealer)
        if player == 21:
            pygame.event.post(pygame.event.Event(self.USER_BLACK_JACK))
            print("THREW USER BLACK JACK")
        elif dealer == 21:
            pygame.event.post(pygame.event.Event(self.DEALER_BLACK_JACK))
            print("DEALER BLACK JACK")
        elif player > 21:
            pygame.event.post(pygame.event.Event(self.USER_BUST))
            print("USER BUST")
        elif dealer > 21:
            pygame.event.post(pygame.event.Event(self.DEALER_BUST))
            print("DEALER BUST")
        elif player > dealer:
            pygame.event.post(pygame.event.Event(self.USER_WINS))
            print("DEALER WINS")
        elif dealer > player:
            pygame.event.post(pygame.event.Event(self.DEALER_WINS))
            print("USER WINS")

    def handle_stand(self):

        dealer_score = self.count_dealer_points_in_hand()
        player_score = self.count_points_in_hand()

        dist = norm(loc = 0, scale = 5)
        sample = norm.rvs(loc = 0, scale = 5)

        print("DEALER SCORE : ", dealer_score)
        print("Player score : ", player_score)
        while dealer_score < 15 + sample:
            print("15 + sample ", 15 + sample)
            self.gameplay.states[GameStates.DEALER_PLACE_CARDS].dealer_card_slider.add_card(self.gameplay.dealer.get_card())
            dealer_score = self.count_dealer_points_in_hand()
            print("DEALER SCORE : ", dealer_score)
            sample = norm.rvs(loc = 0, scale = 5)

        self.evaluate()

    def handle_user_events(self, text):
        self.evaluation_board.set_text(text).prepare()
        pygame.time.set_timer(self.MY_EVENT, 3000)
        self.is_evaluation_set = True
        self.gameplay.states[GameStates.DEALER_PLACE_CARDS].dealer_card_slider.reveal_all_cards()
        self.gameplay.player.refresh_amount()

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.hit_button.is_mouse_over():
                        self.gameplay.states[GameStates.DEALER_PLACE_CARDS].player_card_slider.add_card(self.gameplay.dealer.get_hit_cards())
                        if self.count_points_in_hand() > 21:
                            pygame.event.post(pygame.event.Event(self.USER_BUST))
                    if self.stand_button.is_mouse_over():
                        self.handle_stand()
            if event.type == self.MY_EVENT:
                pygame.time.set_timer(self.MY_EVENT, 0)
                self.gameplay.refresh_state(GameStates.PLACE_BETS)
                self.game_state_manager.set_state(GameStates.PLACE_BETS)
            if event.type == self.USER_BLACK_JACK:
                self.handle_user_events("Black Jack")
                self.gameplay.player.win(self.gameplay.cur_bet * 2)
            if event.type == self.USER_WINS or event.type == self.DEALER_BUST:
                self.handle_user_events("You Win")
                self.gameplay.player.win(self.gameplay.cur_bet * 2)
            if event.type == self.DEALER_WINS or event.type == self.DEALER_BLACK_JACK or event.type == self.USER_BUST:
                self.handle_user_events("Dealer Wins")

class UserBust:

    def __init__(self, state_machine:GameplayStateMachine, gameplay:Gameplay):
        
        self.gameplay = gameplay 
        self.game_state_machine = state_machine
        self.bust_text_board = TextBoard(self.gameplay.screen).set_background("").set_font(None).set_height(100).set_width(500).set_text("Bust").set_position((0, 0)).prepare()
        self.last = pygame.time.get_ticks()
        self.cooldown = 2000

    def run(self, events):
        pass