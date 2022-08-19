from card import Card
from pile import Pile
from typing import List
import numpy as np

CardList = List[Card]
PileList = List[Pile]

def getCardNum(card: Card): return card.num
def getPileNum(pile: Pile): return getCardNum(pile.card_on_top)

def choose_smallest_pile(piles: PileList) -> Pile:
    return min(piles, key= lambda x:x.value)

def play_cards(cards_to_play: CardList, piles: PileList):
    for card in cards_to_play:
        n_pile = 0
        c_1, c_2 = -np.inf, piles[n_pile].card_on_top.num

        # dois-je passer à la pile suivante ?
        while c_2 < card.num and n_pile < len(piles):
            c_1 = piles[n_pile].card_on_top.num
            c_2 = np.inf if n_pile+1 == len(piles) else piles[n_pile+1].card_on_top.num
            n_pile += 1
        # après cette boucle, la card est juste à gauche de la pile ayant c_2

        # print(f"#{n_pile} c_1, c_2 == {c_1} {c_2}")
        # si la carte est à gauche de la première pile
        if -np.inf == c_1:
            # prend n'importe quel pile et la reset
            choose_smallest_pile(piles).reset_with_card(card)
            piles.sort(key = getPileNum)
            continue

        # si je suis entre deux tas
        if c_1 < card.num < c_2:
            piles[n_pile-1].add_card(card)
            continue

        # si la carte est à droite de la dernière pile
        if n_pile == len(piles):
            piles[-1].add_card(card)
            continue
