from card import Card

NB_CARDS_MAX_FOR_PILE = 6
DEBUG = False

class Pile:
    def __init__(self, card_on_top: Card):
        self.card_on_top = card_on_top
        self.value = card_on_top.getValue()
        self.size = 1

    def __repr__(self): 
        return f"{self.card_on_top}"

    def __str__(self):
        return f"{self.card_on_top} (v={self.value}) #{self.size}"
    
    def addCard(self, card: Card):
        self.size += 1

        if self.size == NB_CARDS_MAX_FOR_PILE:
            v = self.value
            if DEBUG: print('--> SIX QUI PREND : prise de', v, 'points')
            self.resetWithCard(card)
            return v

        self.value += card.getValue()
        if DEBUG: print('-->', card, 'is put on top of', self.card_on_top, 'size =', self.size)
        self.card_on_top = card

    
    def resetWithCard(self, card: Card):
        if DEBUG: print('-->', card, 'resets the pile in place of', self.card_on_top)
        self.card_on_top = card
        self.size = 1
        self.value = card.getValue()




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

    def test_resetWithCard(self):
        pile = Pile(Card(4))
        pile.resetWithCard(Card(10))
        self.assertEqual(pile.value, 3)
        self.assertEqual(pile.size, 1)
        pile.resetWithCard(Card(33))
        self.assertEqual(pile.value, 5)
        self.assertEqual(pile.size, 1)


if __name__ == '__main__':
    unittest.main()
