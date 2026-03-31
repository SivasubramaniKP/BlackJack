from enum import Enum, auto

class Suite(Enum):
    HEART = "Hearts"
    DIAMONDS = "Diamonds"
    SPADE = "Spades"
    CLUBS = "Clubs"

class Rank(Enum):
    ACE = 'A'
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'


class RearColor(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'

def points_translator(rank: Rank):
    if rank in [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN]:
        return rank.value
    if rank in [Rank.JACK, Rank.QUEEN, Rank.KING]:
        return 10
    return 11