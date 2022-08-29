import sys
sys.path.append('.')

from bisect_mine import insort
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

    def test_find_cards_possible_between(self):
        cards = CardList(Card(x) for x in [5, 9, 10, 11, 14, 19, 20, 21, 30, 35, 58, 60, 72, 77])

        cards_result_computed = find_cards_possible_between(cards, 10, 20)

        cards_result_should_be = CardList(Card(x) for x in [11, 14, 19])

        self.assertEqual(len(cards_result_computed), len(cards_result_should_be))

        for i in range(len(cards_result_should_be)):
            with self.subTest(i=i):
                self.assertEqual(cards_result_computed[i].num, cards_result_should_be[i].num)

    def test_compute_excepted_value_of_pile_taken_with_card(self):
        cards = CardList(Card(x) for x in [1, 2, 9, 10])
        card = Card(11)
        pile = Pile(Card(3))
        for x in [7, 8]: pile.add_card(Card(x))

        nb_cards_to_put = pile.nb_cards_to_put()
        self.assertEqual(nb_cards_to_put, 2)

        cards_between = find_cards_possible_between(cards, pile.card_on_top.num, card.num)

        nb_cards_between = len(cards_between)
        self.assertEqual(nb_cards_between, 2)
        sum_cards_between_value = sum(card.get_value() for card in cards_between)
        self.assertEqual(sum_cards_between_value, 4)
        average_value = pile.value + sum_cards_between_value/nb_cards_between
        self.assertEqual(average_value, 5)

        # nb_opponents = 2
        nb_opponents = 2

        count_combinations_in = binomial(nb_cards_to_put, nb_cards_between)
        self.assertEqual(count_combinations_in, 1)
        count_combinations_out = binomial(nb_opponents - nb_cards_to_put, len(cards) - nb_cards_between)
        self.assertEqual(count_combinations_out, 1)
        count_combinations_all = binomial(nb_opponents, len(cards))
        self.assertEqual(count_combinations_all, 4*3/2)
        proba_combinations = count_combinations_in * count_combinations_out / count_combinations_all
        self.assertEqual(proba_combinations, 1/6)

        self.assertAlmostEqual(compute_excepted_value_of_pile_taken_with_card(cards, card, pile, nb_opponents), 5/6, 4)


        # nb_opponents = 3
        nb_opponents = 3

        count_combinations_in = binomial(nb_cards_to_put, nb_cards_between)
        self.assertEqual(count_combinations_in, 1)
        count_combinations_out = binomial(nb_opponents - nb_cards_to_put, len(cards) - nb_cards_between)
        self.assertEqual(count_combinations_out, 2)
        count_combinations_all = binomial(nb_opponents, len(cards))
        self.assertEqual(count_combinations_all, 4)
        proba_combinations = count_combinations_in * count_combinations_out / count_combinations_all
        self.assertEqual(proba_combinations, 1*2/4)

        self.assertAlmostEqual(compute_excepted_value_of_pile_taken_with_card(cards, card, pile, nb_opponents), 2.5, 4)


    def test_compute_excepted_value_of_pile_taken_with_card_one_opponent(self):
        cards = CardList(Card(x) for x in [1, 3, 5, 6, 8])
        pile = Pile(Card(0))
        pile.value = 3
        pile.size = NB_CARDS_MAX_FOR_PILE-1

        nb_cards_to_put = pile.nb_cards_to_put()
        self.assertEqual(nb_cards_to_put, 0)

        card = Card(2)
        with self.subTest(card=card):
            cards_between = find_cards_possible_between(cards, pile.card_on_top.num, card.num)

            nb_cards_between = len(cards_between)
            self.assertEqual(nb_cards_between, 1)
            sum_cards_between_value = sum(card.get_value() for card in cards_between)
            self.assertEqual(sum_cards_between_value, 1)
            average_value = pile.value + sum_cards_between_value/nb_cards_between
            self.assertEqual(average_value, 4)

            nb_opponents = 1

            count_combinations_in = binomial(nb_cards_to_put, nb_cards_between)
            self.assertEqual(count_combinations_in, 1)
            count_combinations_out = binomial(nb_opponents - nb_cards_to_put, len(cards) - nb_cards_between)
            self.assertEqual(count_combinations_out, 4)
            count_combinations_all = binomial(nb_opponents, len(cards))
            self.assertEqual(count_combinations_all, 5)
            proba_combinations = count_combinations_in * count_combinations_out / count_combinations_all
            self.assertEqual(proba_combinations, 4/5)

            self.assertAlmostEqual(compute_excepted_value_of_pile_taken_with_card(cards, card, pile, nb_opponents), 4*4/5, 4)

        card = Card(4)
        with self.subTest(card=card):
            cards_between = find_cards_possible_between(cards, pile.card_on_top.num, card.num)

            nb_cards_between = len(cards_between)
            self.assertEqual(nb_cards_between, 2)
            sum_cards_between_value = sum(card.get_value() for card in cards_between)
            self.assertEqual(sum_cards_between_value, 2)
            average_value = pile.value + sum_cards_between_value/nb_cards_between
            self.assertEqual(average_value, 4)

            nb_opponents = 1

            count_combinations_in = binomial(nb_cards_to_put, nb_cards_between)
            self.assertEqual(count_combinations_in, 1)
            count_combinations_out = binomial(nb_opponents - nb_cards_to_put, len(cards) - nb_cards_between)
            self.assertEqual(count_combinations_out, 3)
            count_combinations_all = binomial(nb_opponents, len(cards))
            self.assertEqual(count_combinations_all, 5)
            proba_combinations = count_combinations_in * count_combinations_out / count_combinations_all
            self.assertEqual(proba_combinations, 3/5)

            self.assertAlmostEqual(compute_excepted_value_of_pile_taken_with_card(cards, card, pile, nb_opponents), 4*3/5, 4)


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
        self.assertEqual(find_best_card_by_evaluating_piles(cards, my_cards, piles, 1).num, 17)

if __name__ == '__main__':
    unittest.main()
