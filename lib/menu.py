import math
import random
import time

from lib.scene import Scene
from lib.ui.button import Button
from lib.ui.card import Card
from lib.ui.game_enums import *
import pygame

class Menu(Scene):
    def __init__(self, screen, game_state_manager):
        super().__init__(screen, game_state_manager)
        self.my_font = pygame.font.Font("./assets/font/Precious.ttf", 100)
        self.text_surface = self.my_font.render("Black Jack", True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.topleft = (400, 200)

        self.text_backdrop = pygame.image.load("./assets/menu/text_background.png")
        self.scaled_image = pygame.transform.scale(self.text_backdrop, (self.text_rect.width + 300, self.text_rect.height + 750))
        self.backdrop_rect = self.scaled_image.get_rect()
        self.backdrop_rect.topleft = (self.text_rect.topleft[0] - 100, self.text_rect.topleft[1] - 350)

        self.bg = pygame.image.load("./assets/menu/background.png")

        self.button = Button(self.screen).set_background("./assets/menu/text_background.png").set_height(100).set_width(400).set_position((500, 500)).set_text("Play").set_font("").prepare()
        self.exit_button = Button(self.screen).set_background("./assets/menu/text_background.png").set_height(100).set_width(400).set_position((500, 650)).set_text("Exit").set_font("").prepare()
        self.button_rect = pygame.Rect(500, 500, 400, 100)

        self.card = Card(Suite.HEART, Rank.QUEEN, RearColor.RED, 2)

    def run(self):
        self.background_render()
        self.text_render()
        self.handle_input()
        self.button_render()


    def handle_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.button.is_mouse_over():
                        self.game_state_manager.set_state("gameplay")
        
        if self.button.is_mouse_over():
            self.button.handle_mouse_over_animation()
    
    def background_render(self):

        self.screen.blit(self.bg, (0, 0))
    
    def text_render(self):

        t = time.time() * 1.5  # Speed of the float
        dx = math.sin(t) * 4
        dy = math.sin(2 * t) * 4

        shaky_rect = self.text_rect.move(50 + dx, 35 + dy)

        self.screen.blit(self.scaled_image, self.backdrop_rect)
        self.screen.blit(self.text_surface, shaky_rect)

        self.screen.blit(self.card.rear_side, (0, 0))
        # pygame.draw.rect(self.screen, (255, 0, 0), text_rect, 2)
        # pygame.draw.rect(self.screen, (255, 0, 0), backdrop_rect, 2)

    def button_render(self):
        self.button.render()
        self.exit_button.render()
                    
        