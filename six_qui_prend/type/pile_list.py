from pile import Pile
from typing import List

def getPileNum(pile: Pile): return pile.card_on_top.num

class PileList(List[Pile]):
    def __str__(self):
        return f"Piles: {' --- '.join(list(str(pile) for pile in self))}"

    def sortByNum(self):
        self.sort(key=getPileNum)

    def show_nums(self):
        return ', '.join(list(str(pile.card_on_top.num) for pile in self))

    def show_normalized_nums(self):
        return ', '.join(list(str(pile.card_on_top.num_normalized) for pile in self))
