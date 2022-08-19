import sys

# setting path
sys.path.append('six_qui_prend')

import unittest
from card import Card

class TestSum(unittest.TestCase):
    def test_get_value(self):
        self.assertEqual(Card(82).get_value(), 1)
        self.assertEqual(Card(54).get_value(), 1)
        self.assertEqual(Card(33).get_value(), 5)
        self.assertEqual(Card(55).get_value(), 7)
        self.assertEqual(Card(95).get_value(), 2)
        self.assertEqual(Card(60).get_value(), 3)
        self.assertEqual(Card(11).get_value(), 5)

if __name__ == '__main__':
    unittest.main()
