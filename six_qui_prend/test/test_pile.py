import sys
sys.path.append('.')

from card import Card
from pile import Pile
import unittest


class TestSum(unittest.TestCase):
    def test_pile_init(self):
        pile = Pile(Card(4))
        self.assertEqual(pile.value, 1)

    def test_add_card(self):
        pile = Pile(Card(4))
        pile.add_card(Card(10))
        self.assertEqual(pile.value, 4)
        self.assertEqual(pile.size, 2)
        pile.add_card(Card(33))
        self.assertEqual(pile.value, 9)
        self.assertEqual(pile.size, 3)

    def test_reset_with_card(self):
        pile = Pile(Card(4))
        pile.reset_with_card(Card(10))
        self.assertEqual(pile.value, 3)
        self.assertEqual(pile.size, 1)
        pile.reset_with_card(Card(33))
        self.assertEqual(pile.value, 5)
        self.assertEqual(pile.size, 1)


if __name__ == '__main__':
    unittest.main()
