from lib.ui.chip import Chip

class Player:

    def __init__(self, screen):
        self.screen = screen

        self.chips = [500, 500, 200, 200, 100, 100, 100, 50, 50, 50, 50, ]
        self.chips = [ Chip(screen, x) for x in self.chips ]
