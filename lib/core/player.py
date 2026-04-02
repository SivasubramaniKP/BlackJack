from lib.ui.chip import Chip
from collections import Counter

class Player:

    def __init__(self, screen):
        self.screen = screen

        self.chips = [5000, 5000, 5000, 500, 500, 200, 200, 100, 100, 100, 50, 50, 50, 50, ]
        self.sum = sum(self.chips)

        self.counts = Counter(self.chips)

        self.chips = {
            500: [ Chip(screen, 500) for _ in range(self.counts[500]) ],
            200: [ Chip(screen, 200) for _ in range(self.counts[200]) ],
            100: [ Chip(screen, 100) for _ in range(self.counts[100]) ],
            50: [ Chip(screen, 50) for _ in range(self.counts[50]) ],
            1000: [ Chip(screen, 1000) for _ in range(self.counts[1000]) ],
            5000: [ Chip(screen, 5000) for _ in range(self.counts[5000]) ],
        }

    def get_all_chips(self):
        res = []
        for type in self.chips:
            res.extend(self.chips[type])

        return res
