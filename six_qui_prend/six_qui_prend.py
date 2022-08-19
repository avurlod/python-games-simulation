from card import Card
from pile import Pile
from random import randint, shuffle
import numpy as np
from typing import Tuple, List


CardList = List[Card]
PileList = List[Pile]

REAL_GAME = False
DEBUG = False

if REAL_GAME:
    NB_CARDS = 104
    NB_CARDS_IN_HAND = 10
    NB_OPPONENTS = 5
    NB_PILES = 4
else:
    NB_CARDS_IN_HAND = 5
    NB_OPPONENTS = 5
    NB_PILES = 2
    NB_CARDS = NB_PILES + (NB_OPPONENTS+1) * NB_CARDS_IN_HAND + 5

def getCardNum(card: Card): return card.num
def getPileNum(pile: Pile): return getCardNum(pile.card_on_top)

def display_state_of_game(cards, cards_in_my_hand, piles):
    print('\nI can play', cards_in_my_hand)
    for pile in piles: print(pile)

def setup() -> Tuple[CardList, CardList, CardList]:
    cards = list(Card(num) for num in range(1, NB_CARDS+1))
    shuffle(cards)
    cards_in_my_hand = list(cards.pop() for _ in range(NB_CARDS_IN_HAND))
    piles = list(Pile(cards.pop()) for _ in range(NB_PILES))

    cards.sort(key= getCardNum)
    cards_in_my_hand.sort(key= getCardNum)
    piles.sort(key = getPileNum)

    return cards, cards_in_my_hand, piles

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
            choose_smallest_pile(piles).resetWithCard(card)
            piles.sort(key = getPileNum)
            continue

        # si je suis entre deux tas
        if c_1 < card.num < c_2:
            piles[n_pile-1].addCard(card)
            continue

        # si la carte est à droite de la dernière pile
        if n_pile == len(piles):
            piles[-1].addCard(card)
            continue

def play_one_turn(cards: CardList, cards_in_my_hand: CardList, piles: PileList):
    cards_played_by_opponents = list(cards.pop(randint(0, len(cards)-1)) for _ in range(NB_OPPONENTS))
    card_by_me = cards_in_my_hand.pop()

    cards_to_play = list(cards_played_by_opponents)
    cards_to_play.append(card_by_me)
    cards_to_play.sort(key=getCardNum)
    print(f"I'll play {card_by_me}, within {cards_to_play}")
    play_cards(cards_to_play, piles)


def play():
    cards, cards_in_my_hand, piles = setup()

    display_state_of_game(cards, cards_in_my_hand, piles)
    for _ in range(NB_CARDS_IN_HAND):
        play_one_turn(cards, cards_in_my_hand, piles)
        display_state_of_game(cards, cards_in_my_hand, piles)




import unittest

class TestSum(unittest.TestCase):
    def test_choose_smallest_pile(self):
        piles = list(Pile(Card(x)) for x in [8, 36, 55, 71])
        self.assertEqual(choose_smallest_pile(piles).card_on_top.num, Pile(Card(8)).card_on_top.num)

    def test_play_cards(self):
        cards = list(Card(x) for x in [1, 4, 15, 17, 29, 62])
        piles = list(Pile(Card(x)) for x in [2, 16, 27])
        play_cards(cards, piles)

        self.assertListEqual(list(pile.card_on_top.num for pile in piles), [15, 17, 62])
        self.assertListEqual(list(pile.size for pile in piles), [3, 2, 3])
        self.assertListEqual(list(pile.value for pile in piles), [4, 2, 3])

    def test_play_cards_with_six_qui_prend(self):
        cards = list(Card(x) for x in [5, 30, 35, 58, 60, 72, 77])
        piles = list(Pile(Card(x)) for x in [8, 36, 55, 71])
        play_cards(cards, piles)

        self.assertListEqual(list(pile.card_on_top.num for pile in piles), [35, 36, 60, 77])
        self.assertListEqual(list(pile.size for pile in piles), [3, 1, 3, 3])
        self.assertListEqual(list(pile.value for pile in piles), [7, 1, 11, 7])

        cards = list(Card(x) for x in [4, 15, 93, 99, 100])
        play_cards(cards, piles)

        self.assertListEqual(list(pile.card_on_top.num for pile in piles), [15, 35, 60, 100])
        self.assertListEqual(list(pile.size for pile in piles), [2, 3, 3, 1])
        self.assertListEqual(list(pile.value for pile in piles), [3, 7, 11, 3])





if __name__ == '__main__':
    # unittest.main()
    play()
