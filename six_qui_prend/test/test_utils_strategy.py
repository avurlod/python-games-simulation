import sys
sys.path.append('.')

from card import Card
from pile import Pile
from utils_strategy import *
import unittest

class TestSum(unittest.TestCase):
    def test_choose_card_wisely_first_and_last(self):
        cards = CardList(Card(x) for x in [5, 30, 35, 58, 60, 72, 77])
        my_cards = CardList(Card(x) for x in [3, 4, 12, 15, 66])
        piles = PileList(Pile(Card(x)) for x in [8, 21])

        self.assertEqual(choose_card_wisely(cards, my_cards, piles, Strategy.FIRST).num, 3)
        self.assertEqual(choose_card_wisely(cards, my_cards, piles, Strategy.LAST).num, 66)

    def test_choose_card_wisely_first_and_last_with_normalization(self):
        cards = CardList(Card(x) for x in [5, 30, 35, 58, 60, 72, 77])
        my_cards = CardList(Card(x) for x in [3, 4, 12, 15, 66])
        piles = PileList(Pile(Card(x)) for x in [8, 21])
        normalize_cards(cards, my_cards, piles)

        self.assertEqual(choose_card_wisely(cards, my_cards, piles, Strategy.FIRST).num, 3)
        self.assertEqual(choose_card_wisely(cards, my_cards, piles, Strategy.LAST).num, 66)

    def test_insort(self):
        all_cards = CardList()
        cards1 = CardList(Card(x) for x in [12, 4])
        cards2 = CardList(Card(x) for x in [9])
        piles1 = PileList(Pile(Card(x)) for x in [3, 10])
        cards3 = CardList(Card(x) for x in [7, 14, 15])
        piles2 = PileList(Pile(Card(x)) for x in [11, 71])
        for card in cards1: insort(all_cards, card, key=getCardNum)
        for card in cards2: insort(all_cards, card, key=getCardNum)
        for pile in piles1: insort(all_cards, pile.card_on_top, key=getCardNum)
        for card in cards3: insort(all_cards, card, key=getCardNum)
        for pile in piles2: insort(all_cards, pile.card_on_top, key=getCardNum)

        all_cards_result = CardList(Card(x) for x in [3, 4, 7, 9, 10, 11, 12, 14, 15, 71])

        for i in range(len(all_cards_result)):
            with self.subTest(i=i):
                self.assertEqual(all_cards[i].num, all_cards_result[i].num)

    def test_normalize_cards_if_nums_are_correct(self):
        piles = PileList(Pile(Card(x)) for x in [3, 7])
        cards = CardList(Card(x) for x in [1, 8])
        my_cards = CardList(Card(x) for x in [4, 6])
        #2 and 5 missing

        all_cards = CardList(Card(x) for x in [1, 3, 4, 6, 7, 8])
        normalized_cards = normalize_cards(cards, my_cards, piles)

        for i in range(len(all_cards)):
            with self.subTest(i=i):
                self.assertEqual(all_cards[i].num, normalized_cards[i].num)

    def test_normalize_cards_if_nums_normalized_are_correct(self):
        piles = PileList(Pile(Card(x)) for x in [2])
        cards = CardList(Card(x) for x in [1])
        my_cards = CardList(Card(x) for x in [4])

        # 3 is missing
        normalized_cards = normalize_cards(cards, my_cards, piles)

        all_cards = CardList(Card(x) for x in [1, 2, 4])
        all_cards[0].num_normalized = 1
        all_cards[1].num_normalized = 2
        all_cards[2].num_normalized = 3
        for i in range(len(all_cards)):
            with self.subTest(i=i):
                self.assertEqual(all_cards[i].num, normalized_cards[i].num)
                self.assertEqual(all_cards[i].num_normalized, normalized_cards[i].num_normalized)

    def test_fake_pile_with_O_on_top(self):
        pile = Pile(Card(3))
        for x in [7, 8, 9, 10]: pile.add_card(Card(x))
        piles = [pile, Pile(Card(16))]

        self.assertEqual(fake_pile_with_O_on_top(piles).value, 1)

    def test_find_best_card_by_evaluating_piles_with_card_below_pile(self):
        pile = Pile(Card(3))
        for x in [7, 8, 9, 10]: pile.add_card(Card(x))
        piles = [pile, Pile(Card(16))]

        cards = CardList(Card(x) for x in [1, 4, 5, 6, 12, 13, 14, 15, 17])
        my_cards = CardList(Card(x) for x in [2, 11])
        self.assertEqual(find_best_card_by_evaluating_piles(cards, my_cards, piles, 1).num, 2)

    def test_find_best_card_by_evaluating_piles(self):
        pile = Pile(Card(3))
        for x in [7, 8, 9, 10]: pile.add_card(Card(x))
        piles = [pile, Pile(Card(16))]

        cards = CardList(Card(x) for x in [1, 4, 5, 12, 14])
        my_cards = CardList(Card(x) for x in [2, 6, 11, 13, 15, 17])
        self.assertEqual(find_best_card_by_evaluating_piles(cards, my_cards, piles, 1).num, 2)

if __name__ == '__main__':
    unittest.main()
