from enum import Enum, auto

# STRATEGY_LIST = ["random", "last", "first", "count cards farthest from direct take"]

class Strategy(Enum):
    RANDOM = auto()
    LAST = auto()
    FIRST = auto()
    MINIMIZE_EXCEPTED_VALUE = auto()

STRATEGY_DEFAULT = Strategy.MINIMIZE_EXCEPTED_VALUE

# si my_cards = [3, 10, 11, 12]
# => faire en sorte de jouer 10 seulement s'il restera de la place après pour 11 et 12
# ==> jouer 11 que si de la place pour 12 aussi 
