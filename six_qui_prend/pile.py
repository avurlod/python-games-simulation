from card import Card

NB_CARDS_MAX_FOR_PILE = 6
DEBUG = False

class Pile:
    def __init__(self, card_on_top: Card):
        self.card_on_top = card_on_top
        self.value = card_on_top.get_value()
        self.size = 1

    def __repr__(self): 
        return f"{self.card_on_top}"

    def __str__(self):
        return f"{self.card_on_top} (v={self.value}) #{self.size}"
    
    def add_card(self, card: Card):
        self.size += 1

        if self.size == NB_CARDS_MAX_FOR_PILE:
            v = self.value
            if DEBUG: print('--> SIX QUI PREND : prise de', v, 'points')
            self.reset_with_card(card)
            return v

        self.value += card.get_value()
        if DEBUG: print('-->', card, 'is put on top of', self.card_on_top, 'size =', self.size)
        self.card_on_top = card

    
    def reset_with_card(self, card: Card):
        if DEBUG: print('-->', card, 'resets the pile in place of', self.card_on_top)
        self.card_on_top = card
        self.size = 1
        self.value = card.get_value()


