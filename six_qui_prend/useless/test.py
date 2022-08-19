import unittest

from bac_a_sable import *

class TestSum(unittest.TestCase):
    def test_binomial(self):
        self.assertEqual(binomial(0, 3), 1)
        self.assertEqual(binomial(1, 2), 2)
        self.assertEqual(binomial(2, 2), 1)
        self.assertEqual(binomial(1, 3), 3)
        self.assertEqual(binomial(2, 4), 6)

    def test_count_arrangements(self):
        self.assertEqual(count_arrangements(1, 1), 1)
        self.assertEqual(count_arrangements(0, 4), 1)
        self.assertEqual(count_arrangements(1, 4), 4)
        self.assertEqual(count_arrangements(4, 4), 4*3*2*1)
        self.assertEqual(count_arrangements(2, 5), 5*4)

    def test_count_arrangements_i_cards_below_c(self):
        self.assertEqual(count_arrangements_i_cards_below_c(0, 2, 3, 6), 3*2)
        self.assertEqual(count_arrangements_i_cards_below_c(1, 2, 3, 6), 2*3 + 3*2)
        self.assertEqual(count_arrangements_i_cards_below_c(2, 2, 3, 6), 2*1)
        self.assertEqual(count_arrangements_i_cards_below_c(1, 1, 5, 20), 4)
        self.assertEqual(count_arrangements_i_cards_below_c(0, 2, 5, 20), 15*14)
        self.assertEqual(count_arrangements_i_cards_below_c(1, 2, 5, 20), 4*15 + 15*4)
        self.assertEqual(count_arrangements_i_cards_below_c(2, 2, 5, 20), 4*3)
        self.assertEqual(count_arrangements_i_cards_below_c(2, 3, 5, 20), 4*3*15 + 4*15*3 + 4*3*15)

    def test_sum_of_arrangements(self):
        c, c_max = 3, 6
        for i_max in range(c):
            with self.subTest(i_max=i_max):
                self.assertEqual(sum_of_arrangements_i_cards_below_c(i_max, c, c_max), count_arrangements(i_max, c_max-1))

    def test_count_loosing_cards(self):
        cards_available = [1, 4, 5, 6, 7, 9, 10]
        self.assertEqual(count_loosing_cards(2, 3, cards_available), 0)
        self.assertEqual(count_loosing_cards(9, 3, cards_available), 4)

    def test_proba_loosing_cards_one_card(self):
        cards_available = [1, 4, 5, 6, 7, 9, 10]
        self.assertEqual(proba_loosing_cards_one_card(2, 3, cards_available), 0)
        self.assertEqual(proba_loosing_cards_one_card(9, 3, cards_available), 4/7)

    def test_proba_loosing_cards_multi_cards(self):
        cards_available = [1, 4, 5, 6, 7, 9, 10]
        self.assertListEqual(proba_loosing_cards_multi_cards([2, 9], 3, cards_available), [(2, 0), (9, 4/7)])

    def test_count_loosing_cards_multi_cards_multi_tops(self):
        cards_available = [1, 4, 5, 7, 9, 10]
        n = len(cards_available)
        cards_on_top = [3, 6]
        cards_in_my_hand = [2, 8]
        self.assertListEqual(count_loosing_cards_multi_cards_multi_tops(cards_in_my_hand, cards_on_top, cards_available), [(2, [(-np.inf, n-1), (3, 0), (6, 0)]), (8, [(-np.inf, 0), (3, 0), (6, n-1)])])


        cards_available = [1, 4, 5, 7, 9, 10]
        n = len(cards_available)
        cards_on_top = [2, 6]
        cards_in_my_hand = [3, 8]
        self.assertListEqual(count_loosing_cards_multi_cards_multi_tops(cards_in_my_hand, cards_on_top, cards_available), [(3, [(-np.inf, 0), (2, n), (6, 0)]), (8, [(-np.inf, 0), (2, 0), (6, n-1)])])


        cards_available = [1, 4, 5, 7, 9, 10, 11, 12, 15, 19, 51, 52, 62]
        n = len(cards_available)
        cards_on_top = [6, 16, 27]
        cards_in_my_hand = [14, 35]
        self.assertListEqual(count_loosing_cards_multi_cards_multi_tops(cards_in_my_hand, cards_on_top, cards_available), [(14, [(-np.inf, 0), (6, n-5), (16, 0), (27, 0)]), (35, [(-np.inf, 0), (6, 0), (16, 0), (27, n)])])

    def test_proba_loosing_cards_multi_cards_multi_tops(self):
        cards_available = [1, 4, 5, 7, 9, 10]
        n = len(cards_available)
        cards_on_top = [3, 6]
        cards_in_my_hand = [2, 8]
        self.assertListEqual(proba_loosing_cards_multi_cards_multi_tops(cards_in_my_hand, cards_on_top, cards_available), [(2, [(-np.inf, (n-1)/n), (3, 0), (6, 0)]), (8, [(-np.inf, 0), (3, 0), (6, (n-1)/n)])])


        cards_available = [1, 4, 5, 7, 9, 10, 11, 12, 15, 19, 51, 52, 62]
        n = len(cards_available)
        cards_on_top = [6, 16, 27]
        cards_in_my_hand = [14, 35]
        self.assertListEqual(proba_loosing_cards_multi_cards_multi_tops(cards_in_my_hand, cards_on_top, cards_available), [(14, [(-np.inf, 0), (6, (n-5)/n), (16, 0), (27, 0)]), (35, [(-np.inf, 0), (6, 0), (16, 0), (27, 1)])])


if __name__ == '__main__':
    unittest.main()
