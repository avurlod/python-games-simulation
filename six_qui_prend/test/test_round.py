import sys
sys.path.append('.')

from constants import *
from round import Round
import unittest


class TestSum(unittest.TestCase):
    def setUp(self) -> None:
        self.round = Round()

    def test_nb_of_cards_when_setup(self):
        self.assertEqual(len(self.round.my_cards), NB_CARDS_IN_HAND)

    def test_nb_of_cards_after_play_one_turn(self):
        self.round.play_one_turn()
        self.assertEqual(len(self.round.my_cards), NB_CARDS_IN_HAND-1)

    def test_update_score_after_turn_when_no_change(self):
        self.round.update_score_after_turn([], 37)
        self.assertEqual(self.round.score.mine, 0)
        self.assertEqual(self.round.score.opponents, 0)

    def test_update_score_after_turn_when_change_only_opponents(self):
        points_taken_by_cards = [(11, 1), (12, 3)]
        self.round.update_score_after_turn(points_taken_by_cards, 99)
        self.assertEqual(self.round.score.mine, 0)
        self.assertEqual(self.round.score.opponents, 4)

    def test_update_score_after_turn_when_change_only_mine(self):
        points_taken_by_cards = [(14, 1)]
        self.round.update_score_after_turn(points_taken_by_cards, 14)
        self.assertEqual(self.round.score.mine, 1)
        self.assertEqual(self.round.score.opponents, 0)

    def test_update_score_after_turn_when_change_for_both(self):
        points_taken_by_cards = [(1, 7), (4, 6), (12, 3)]
        self.round.update_score_after_turn(points_taken_by_cards, 12)
        self.assertEqual(self.round.score.mine, 3)
        self.assertEqual(self.round.score.opponents, 13)

    def test_update_score_after_turn_when_no_change_after_turn(self):
        points_taken_by_cards = [(1, 7), (4, 6), (12, 3)]
        self.round.update_score_after_turn(points_taken_by_cards, 12)
        self.assertEqual(self.round.score.mine, 3)
        self.assertEqual(self.round.score.opponents, 13)

        self.round.update_score_after_turn([], 73)
        self.assertEqual(self.round.score.mine, 3)
        self.assertEqual(self.round.score.opponents, 13)

if __name__ == '__main__':
    unittest.main()
