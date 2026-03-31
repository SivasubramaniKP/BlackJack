from lib.scene import Scene
import pygame
from lib.core.dealer import Dealer
from lib.core.player import Player


class GameplayStateMachine:

    def __init__(self):
        self.cur_state = "dealerPlaceCards"
    
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
        # self.states = {
        #     "dealerPlaceCards": DealerPlaceCards(screen, self.state_machine),
        #     "userHitOrStand": UserHitOrStand(screen, self.state_machine)
        # }

        self.bg_image = pygame.image.load("./assets/game/table.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (1920, 1080))

    def run(self):
        my_font = pygame.font.SysFont('Inter', 30)
        text_surface = my_font.render("Game Here", True, (255, 255, 255))
        self.screen.blit(text_surface, (0, 0))
        self.screen.blit(self.bg_image, (0, 0))
        self.state_machine.get_state().run()


# class DealerPlaceCards(Gameplay):

#     def __init__(self, screen, game_state_manager: GameplayStateMachine):
#         super().__init__(screen, game_state_manager)

#     def run(self):
#         self.dealer.place_cards()
#         self.game_state_manager.set_state()


# class UserHitOrStand(Gameplay):

#     def __init__(self, screen, game_state_manager):
#         super().__init__(screen, game_state_manager)
    
#     def run(self):
#         pass