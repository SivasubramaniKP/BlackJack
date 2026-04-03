import pygame
from lib.game_state_machine import StateMachine
from lib.menu import Menu
from lib.gameplay import Gameplay
from lib.core.deck import Deck
from lib.ui.game_enums import *

HEIGHT = 1080
WIDTH = 1920


class Game:

    def __init__(self): 
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.state_machine = StateMachine("menu")
        self.clock = pygame.time.Clock()
        self.running = True

        deck = Deck(rear_color=RearColor.RED, card_rear_variant=2)

        self.all_sprites = pygame.sprite.Group()

        self.states = {
            "menu": Menu(self.screen, self.state_machine),
            "gameplay": Gameplay(self.screen, self.state_machine)
        }
        
    def run(self):
        while self.running:
            self.screen.fill("gray10")
            self.clock.tick(144)
            self.events()
            # self.update()
            self.states[self.state_machine.get_state()].run()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.event.post(event)

    def update(self):
        # Update all sprites in the group
        self.all_sprites.update()

    def draw(self):
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
    
if __name__ == "__main__":
    game = Game()
    game.run()