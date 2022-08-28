import sys
sys.path.append('.')

from card import Card
from pile import Pile
from utils_strategy import *
import unittest

class TestSum(unittest.TestCase):
    def test_count_combinations_pile_makes_me_loose_with_card_if_directly_above(self):
        cards = CardList(Card(x) for x in [1, 6, 17, 21, 32])
        card = Card(13)
        pile = Pile(Card(3))
        for x in [7, 8, 9, 10]: pile.add_card(Card(x))
        normalize_cards(cards, CardList([card]), PileList([pile]))

        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 1), 5)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 2), 10)

    def test_count_combinations_pile_makes_me_loose_with_card_if_below_pile(self):
        cards = CardList(Card(x) for x in [1, 6, 17, 21, 32])
        card = Card(5)
        pile = Pile(Card(3))
        for x in [7, 8, 9, 10]: pile.add_card(Card(x))
        normalize_cards(cards, CardList([card]), PileList([pile]))

        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 1), 0)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 2), 0)

    def test_count_combinations_pile_makes_me_loose_with_card_if_not_enough_opponents(self):
        cards = CardList(Card(x) for x in [1, 6, 17, 21, 32])
        card = Card(51)
        pile = Pile(Card(3))
        for x in [7]: pile.add_card(Card(x))
        normalize_cards(cards, CardList([card]), PileList([pile]))

        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 1), 0)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 2), 0)
        self.assertNotEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 3), 0)

    def test_count_combinations_pile_makes_me_loose_with_card_if_not_enough_space(self):
        cards = CardList(Card(x) for x in [1, 2, 4, 5, 6, 11])
        card = Card(10)
        pile = Pile(Card(3))
        for x in [7, 8]: pile.add_card(Card(x))
        normalize_cards(cards, CardList([card]), PileList([pile]))

        nb_cards_between = card.num - pile.card_on_top.num - 1
        nb_cards_to_put = NB_CARDS_MAX_FOR_PILE - pile.size - 1
        self.assertEqual(nb_cards_between, 1)
        self.assertEqual(nb_cards_to_put, 2)

        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 5), 0)

    def test_count_combinations_pile_makes_me_loose_with_card_if_one_card_to_put(self):
        cards = CardList(Card(x) for x in [1, 6, 13, 21, 32, 51])
        card = Card(20)
        pile = Pile(Card(3))
        for x in [7, 8, 9]: pile.add_card(Card(x))
        normalize_cards(cards, CardList([card]), PileList([pile]))

        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 1), 1)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 2), 1*5)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 3), 1*(5*4/2))

    def test_count_combinations_pile_makes_me_loose_with_card_if_two_cards_to_put(self):
        cards = CardList(Card(x) for x in [1, 6, 13, 17, 22, 32, 51])
        card = Card(24)
        pile = Pile(Card(3))
        for x in [7, 8]: pile.add_card(Card(x))
        normalize_cards(cards, CardList([card]), PileList([pile]))

        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 1), 0)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 2), 3)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 3), 3*4)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 4), 3*(4*3/2))


    # def test_normalize_cards_if_nums_are_correct(self):
    #     piles = PileList(Pile(Card(x)) for x in [3, 7])
    #     cards = CardList(Card(x) for x in [1, 8])
    #     my_cards = CardList(Card(x) for x in [4, 6])
    #     #2 and 5 missing

    #     all_cards = CardList(Card(x) for x in [1, 3, 4, 6, 7, 8])
    #     normalized_cards = normalize_cards(cards, my_cards, piles)

    #     for i in range(len(all_cards)):
    #         with self.subTest(i=i):
    #             self.assertEqual(all_cards[i].num, normalized_cards[i].num)

    # def test_normalize_cards_if_nums_normalized_are_correct(self):
    #     piles = PileList(Pile(Card(x)) for x in [2])
    #     cards = CardList(Card(x) for x in [1])
    #     my_cards = CardList(Card(x) for x in [4])

    #     # 3 is missing
    #     normalized_cards = normalize_cards(cards, my_cards, piles)

    #     all_cards = CardList(Card(x) for x in [1, 2, 4])
    #     all_cards[0].num_normalized = 1
    #     all_cards[1].num_normalized = 2
    #     all_cards[2].num_normalized = 3
    #     for i in range(len(all_cards)):
    #         with self.subTest(i=i):
    #             self.assertEqual(all_cards[i].num, normalized_cards[i].num)
    #             self.assertEqual(all_cards[i].num_normalized, normalized_cards[i].num_normalized)

    # def test_fake_pile_with_O_on_top(self):
    #     pile = Pile(Card(3))
    #     for x in [7, 8, 9, 10]: pile.add_card(Card(x))
    #     piles = [pile, Pile(Card(16))]

    #     self.assertEqual(fake_pile_with_O_on_top(piles).value, 1)

    # def test_find_best_card_by_evaluating_piles_with_card_below_pile(self):
    #     pile = Pile(Card(3))
    #     for x in [7, 8, 9, 10]: pile.add_card(Card(x))
    #     piles = [pile, Pile(Card(16))]

    #     cards = CardList(Card(x) for x in [1, 4, 5, 6, 12, 13, 14, 15, 17])
    #     my_cards = CardList(Card(x) for x in [2, 11])
    #     self.assertEqual(find_best_card_by_evaluating_piles(cards, my_cards, piles, 1).num, 2)

    # def test_find_best_card_by_evaluating_piles(self):
    #     pile = Pile(Card(3))
    #     for x in [7, 8, 9, 10]: pile.add_card(Card(x))
    #     piles = [pile, Pile(Card(16))]

    #     cards = CardList(Card(x) for x in [1, 4, 5, 12, 14])
    #     my_cards = CardList(Card(x) for x in [2, 6, 11, 13, 15, 17])
    #     self.assertEqual(find_best_card_by_evaluating_piles(cards, my_cards, piles, 1).num, 2)

if __name__ == '__main__':
    unittest.main()
