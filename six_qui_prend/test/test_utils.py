import sys

# setting path
sys.path.append('six_qui_prend')

import unittest
from pile import Pile
from card import Card
from utils import *

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
    unittest.main()
