from card import Card

class Pile:
    def __init__(self, card_on_top: Card):
        self.card_on_top = card_on_top
        self.value = card_on_top.getValue()
        self.size = 1

    def __repr__(self): 
        return f"{self.card_on_top}"

    def __str__(self):
        return f"{self.card_on_top} is on top. Value is {self.value}"
    
    def addCard(self, card: Card):
        print('-->', card, 'is put on top of', self.card_on_top)
        self.card_on_top = card
        self.size += 1
        self.value += card.getValue()




import unittest

class TestSum(unittest.TestCase):
    def test_pile_init(self):
        pile = Pile(Card(4))
        self.assertEqual(pile.value, 1)

    def test_addCard(self):
        pile = Pile(Card(4))
        pile.addCard(Card(10))
        self.assertEqual(pile.value, 4)
        self.assertEqual(pile.size, 2)
        pile.addCard(Card(33))
        self.assertEqual(pile.value, 9)
        self.assertEqual(pile.size, 3)


if __name__ == '__main__':
    unittest.main()
