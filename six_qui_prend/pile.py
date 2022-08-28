from card import Card
from constants import SHOW_DETAILS_PILE_UPDATE, NB_CARDS_MAX_FOR_PILE

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
            v = self.reset_with_card(card)
            if SHOW_DETAILS_PILE_UPDATE: print('==> SIX QUI PREND : prise de', v, 'points avec le', card.num)
            return v

        self.value += card.get_value()
        if SHOW_DETAILS_PILE_UPDATE: print('-->', card, 'is put on top of', self.card_on_top, 'size =', self.size)
        self.card_on_top = card
        return 0
    
    def reset_with_card(self, card: Card) -> int:
        points_to_take = self.value
        if SHOW_DETAILS_PILE_UPDATE: print('-->', card, 'resets the pile in place of', self.card_on_top)
        self.card_on_top = card
        self.size = 1
        self.value = card.get_value()
        return points_to_take

    def nb_cards_to_put(self):
        return NB_CARDS_MAX_FOR_PILE - self.size - 1
