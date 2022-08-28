from card import Card
from typing import List

def getCardNum(card: Card): return card.get_num()

class CardList(List[Card]):
    def __str__(self):
        return ', '.join(list(str(card) for card in self))

    def sortByNum(self):
        self.sort(key=getCardNum)
