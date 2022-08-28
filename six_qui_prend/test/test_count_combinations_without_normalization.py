import sys
sys.path.append('.')

from card import Card
from pile import Pile
from utils_strategy import *
import unittest

class TestSum(unittest.TestCase):
    def test_count_combinations_pile_makes_me_loose_with_card_if_directly_above(self):
        cards = CardList(Card(x) for x in [1, 2, 4, 5, 6])
        card = Card(11)
        pile = Pile(Card(3))
        for x in [7, 8, 9, 10]: pile.add_card(Card(x))

        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 1), 5)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 2), 10)

    def test_count_combinations_pile_makes_me_loose_with_card_if_below_pile(self):
        cards = CardList(Card(x) for x in [1, 4, 5, 6, 11])
        card = Card(2)
        pile = Pile(Card(3))
        for x in [7, 8, 9, 10]: pile.add_card(Card(x))

        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 1), 0)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 2), 0)

    def test_count_combinations_pile_makes_me_loose_with_card_if_not_enough_opponents(self):
        cards = CardList(Card(x) for x in [1, 2, 4, 5, 6, 11])
        card = Card(12)
        pile = Pile(Card(3))
        for x in [7, 8]: pile.add_card(Card(x))

        nb_cards_to_put = NB_CARDS_MAX_FOR_PILE - pile.size - 1
        self.assertEqual(nb_cards_to_put, 2)
        self.assertTrue(1 < nb_cards_to_put)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 1), 0)
        self.assertNotEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 2), 0)

    def test_count_combinations_pile_makes_me_loose_with_card_if_not_enough_space(self):
        cards = CardList(Card(x) for x in [1, 2, 4, 5, 6, 11])
        card = Card(10)
        pile = Pile(Card(3))
        for x in [7, 8]: pile.add_card(Card(x))

        nb_cards_between = card.num - pile.card_on_top.num - 1
        nb_cards_to_put = NB_CARDS_MAX_FOR_PILE - pile.size - 1
        self.assertEqual(nb_cards_between, 1)
        self.assertEqual(nb_cards_to_put, 2)

        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 5), 0)

    def test_count_combinations_pile_makes_me_loose_with_card_if_one_card_to_put(self):
        cards = CardList(Card(x) for x in [1, 2, 4, 5, 6, 10])
        card = Card(11)
        pile = Pile(Card(3))
        for x in [7, 8, 9]: pile.add_card(Card(x))


        nb_cards_to_put = NB_CARDS_MAX_FOR_PILE - pile.size - 1
        nb_cards_between = card.num - pile.card_on_top.num - 1
        self.assertEqual(nb_cards_to_put, 1)
        self.assertEqual(nb_cards_between, 1)
        self.assertEqual(binomial(nb_cards_to_put, nb_cards_between), 1)
        self.assertEqual(binomial(1 - nb_cards_to_put, len(cards) - nb_cards_between), 1)

        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 1), 1)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 2), 1*5)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 3), 1*(5*4/2))

    def test_count_combinations_pile_makes_me_loose_with_card_if_two_cards_to_put(self):
        cards = CardList(Card(x) for x in [1, 2, 4, 5, 6, 9, 10])
        card = Card(11)
        pile = Pile(Card(3))
        for x in [7, 8]: pile.add_card(Card(x))

        nb_cards_to_put = NB_CARDS_MAX_FOR_PILE - pile.size - 1
        nb_cards_between = card.num - pile.card_on_top.num - 1
        self.assertEqual(nb_cards_to_put, 2)
        self.assertEqual(nb_cards_between, 2)
        self.assertEqual(binomial(nb_cards_to_put, nb_cards_between), 1)
        self.assertEqual(binomial(2 - nb_cards_to_put, len(cards) - nb_cards_between), 1)
        self.assertEqual(binomial(3 - nb_cards_to_put, len(cards) - nb_cards_between), 5)

        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 1), 0)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 2), 1)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 3), 5)
        self.assertEqual(count_combinations_pile_makes_me_loose_with_card(cards, card, pile, 4), 5*4/2)

if __name__ == '__main__':
    unittest.main()
