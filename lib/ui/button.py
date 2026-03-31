import pygame
import time
import math
from lib.ui.text_board import TextBoard

class Button(TextBoard):

    # def __init__(self, screen):
    #     self.screen = screen

    def __init__(self, screen):
        super().__init__(screen)
    
    # def set_text(self, text):
    #     self.text = text
    #     return self

    # def set_position(self, top_left):
    #     self.top_left = top_left
    #     return self
    
    # def set_font(self, font):
    #     self.font = font
    #     self.font_size = 50
    #     self.font = pygame.font.Font("./assets/font/Precious.ttf", self.font_size)
    #     return self
    
    # def set_background(self, bg):
    #     self.bg = bg
    #     # self.bg_image = pygame.image.load(self.bg)
    #     # self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
    #     return self
    
    # def set_height(self, height):
    #     self.height = height
    #     return self
    
    # def set_width(self, width):
    #     self.width = width
    #     return self
    
    def is_mouse_over(self):
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(self.top_left[0], self.top_left[1], self.width, self.height)
        if button_rect.collidepoint(mouse_pos):
            # print("mouse is over")
            return True
        return False

    def draw_underline(self):
        t = time.time()
        self.animation_clock += 0.01

        dx = abs(math.sin(self.animation_clock)) * (self.text_rect.width/2)

        line_1_start_coords = (self.text_rect.midbottom[0], self.text_rect.midbottom[1] + 5)
        line_1_end_coords = (line_1_start_coords[0] + dx, self.text_rect.bottomleft[1] + 5)
        
        line_2_start_coords = (self.text_rect.midbottom[0], self.text_rect.midbottom[1] + 5)
        line_2_end_coords =  (line_1_start_coords[0] - dx, self.text_rect.bottomleft[1] + 5)

        color = (181, 0, 178) 
        pygame.draw.line(self.screen, color, line_1_start_coords, line_1_end_coords, 5)
        pygame.draw.line(self.screen, color, line_2_start_coords, line_2_end_coords, 5)

    def handle_mouse_over_animation(self):
        # self.animation_clock = 0
        if self.is_mouse_over():
            self.draw_underline()
        else:
            self.animation_clock = 0
        self.prepare()

    def prepare(self):

        self.animation_clock = 0
        self.bg_image = pygame.Surface((self.width, self.height))
        color = (255, 247, 205) 
        self.bg_image.fill(color)
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.topleft = self.top_left

        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()

        self.text_rect.center = self.bg_rect.center

        return self

    def render(self):
        
        self.screen.blit(self.bg_image, self.bg_rect)
        self.screen.blit(self.text_surface, self.text_rect)

        self.handle_mouse_over_animation()
        # print(self.text_rect)
        # self.is_mouse_over(rect=bg_rect)
        # pygame.draw.rect(self.screen, (255, 0, 0), self.bg_rect, 2)
        # pygame.draw.rect(self.screen, (255, 0, 0), self.text_rect, 2)
    