import sys
sys.path.append('.')

from card import Card
from pile import Pile
from utils import *
import unittest

class TestSum(unittest.TestCase):
    def test_choose_smallest_pile(self):
        piles = PileList(Pile(Card(x)) for x in [8, 36, 55, 71])
        self.assertEqual(choose_smallest_pile(piles).card_on_top.num, Pile(Card(8)).card_on_top.num)

    def test_find_interval(self):
        piles = PileList(Pile(Card(x)) for x in [2, 16, 27])

        c_1, c_2, n_pile = find_interval(Card(1), piles)
        self.assertEqual(c_1, -np.inf)
        self.assertEqual(c_2, 2)
        self.assertEqual(n_pile, -1)

        c_1, c_2, n_pile = find_interval(Card(6), piles)
        self.assertEqual(c_1, 2)
        self.assertEqual(c_2, 16)
        self.assertEqual(n_pile, 0)

        c_1, c_2, n_pile = find_interval(Card(17), piles)
        self.assertEqual(c_1, 16)
        self.assertEqual(c_2, 27)
        self.assertEqual(n_pile, 1)

        c_1, c_2, n_pile = find_interval(Card(51), piles)
        self.assertEqual(c_1, 27)
        self.assertEqual(c_2, np.inf)
        self.assertEqual(n_pile, 2)

    def test_play_cards_very_simple(self):
        cards = CardList(Card(x) for x in [4])
        piles = PileList(Pile(Card(x)) for x in [1, 11])
        play_cards(cards, piles)

        self.assertListEqual(list(pile.card_on_top.num for pile in piles), [4, 11])
        self.assertListEqual(list(pile.size for pile in piles), [2, 1])
        self.assertListEqual(list(pile.value for pile in piles), [2, 5])

    def test_play_cards_simple(self):
        cards = CardList(Card(x) for x in [1, 4, 15])
        piles = PileList(Pile(Card(x)) for x in [2, 11])
        play_cards(cards, piles)

        self.assertListEqual(list(pile.card_on_top.num for pile in piles), [4, 15])
        self.assertListEqual(list(pile.size for pile in piles), [2, 2])
        self.assertListEqual(list(pile.value for pile in piles), [2, 7])

    def test_play_cards(self):
        cards = CardList(Card(x) for x in [1, 4, 15, 17, 29, 62])
        piles = PileList(Pile(Card(x)) for x in [2, 16, 27])
        play_cards(cards, piles)

        self.assertListEqual(list(pile.card_on_top.num for pile in piles), [15, 17, 62])
        self.assertListEqual(list(pile.size for pile in piles), [3, 2, 3])
        self.assertListEqual(list(pile.value for pile in piles), [4, 2, 3])

    def test_play_cards_with_six_qui_prend(self):
        cards = CardList(Card(x) for x in [5, 30, 35, 58, 60, 72, 77])
        piles = PileList(Pile(Card(x)) for x in [8, 36, 55, 71])
        play_cards(cards, piles)

        self.assertListEqual(list(pile.card_on_top.num for pile in piles), [35, 36, 60, 77])
        self.assertListEqual(list(pile.size for pile in piles), [3, 1, 3, 3])
        self.assertListEqual(list(pile.value for pile in piles), [7, 1, 11, 7])

        cards = CardList(Card(x) for x in [4, 15, 93, 99, 100])
        play_cards(cards, piles)

        self.assertListEqual(list(pile.card_on_top.num for pile in piles), [15, 35, 60, 100])
        self.assertListEqual(list(pile.size for pile in piles), [2, 3, 3, 1])
        self.assertListEqual(list(pile.value for pile in piles), [3, 7, 11, 3])

    def test_points_retrieved_by_play_cards_when_add(self):
        cards = CardList(Card(x) for x in [8])
        piles = PileList(Pile(Card(x)) for x in [5])
        points = play_cards(cards, piles)
        self.assertListEqual(points, [])

    def test_points_retrieved_by_play_cards_when_reset(self):
        cards = CardList(Card(x) for x in [5])
        piles = PileList(Pile(Card(x)) for x in [8])
        points_taken_by_cards = play_cards(cards, piles)

        points_taken_by_cards_valid = [(5, 1)]
        self.assertEqual(len(points_taken_by_cards), len(points_taken_by_cards_valid))
        for i in range(len(points_taken_by_cards_valid)):
            self.assertTupleEqual(points_taken_by_cards[i], points_taken_by_cards_valid[i])

if __name__ == '__main__':
    unittest.main()
