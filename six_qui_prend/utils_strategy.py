from operator import attrgetter
from random import randint
from bisect_mine import insort
from card import Card
from constants import NB_CARDS_MAX_FOR_PILE, NB_OPPONENTS
from pile import Pile
from type.strategy import Strategy
from type.card_list import CardList, getCardNum
from type.pile_list import PileList, getPileNum
from utils import choose_smallest_pile, find_interval
import numpy as np

def binomial(k, n):
    if 0 <= k <= n:
        a= 1
        b=1
        for t in range(1, min(k, n - k) + 1):
            a *= n
            b *= t
            n -= 1
        return a // b
    else:
        return 0

def count_combinations_pile_makes_me_loose_with_card(cards: CardList, card: Card, pile: Pile, nb_opponents: int = NB_OPPONENTS):
    # print(card.get_num())
    # print(pile.card_on_top.get_num())
    # none if card is below pile
    if card.get_num() < pile.card_on_top.get_num(): return 0

    # none if not enough opponents between pile and card
    nb_cards_to_put = pile.nb_cards_to_put()
    if nb_opponents < nb_cards_to_put: return 0

    # none if not enough space between pile and card
    nb_cards_between = card.get_num() - pile.card_on_top.get_num() - 1
    if nb_cards_between < nb_cards_to_put: return 0

    # print(nb_cards_to_put, nb_cards_between)
    # print(nb_opponents - nb_cards_to_put, len(cards) - nb_cards_between)
    return binomial(nb_cards_to_put, nb_cards_between) * binomial(nb_opponents - nb_cards_to_put, len(cards) - nb_cards_between)

def fake_pile_with_O_on_top(piles: PileList):
    pile = Pile(Card(0))
    pile.value = choose_smallest_pile(piles).value
    pile.size = NB_CARDS_MAX_FOR_PILE-1
    return pile

def normalize_cards(cards: CardList, my_cards: CardList, piles: PileList):
    all_cards = CardList()
    for card in my_cards: insort(all_cards, card, key=getCardNum)
    for card in cards: insort(all_cards, card, key=getCardNum)
    for pile in piles: insort(all_cards, pile.card_on_top, key=getCardNum)

    for card in all_cards: card.num_normalized = all_cards.index(card)+1
    print('NORMALISATION')
    print(cards)
    print(my_cards)
    print(piles.show_nums())
    print(all_cards)
    print(all_cards.show_normalized_nums())
    return all_cards

def eval_pile(pile: Pile):
    return pile.value + pile.nb_cards_to_put()

def find_best_card_by_evaluating_piles(cards: CardList, my_cards: CardList, piles: PileList, nb_opponents: int = NB_OPPONENTS) -> Card:
    best_card = my_cards[0]
    best_eval = np.inf
    total_combinaisons = binomial(nb_opponents, len(cards))
    fake_lowest_pile = fake_pile_with_O_on_top(piles)
    for card in my_cards:
        #TODO faire la normalisation des cartes pour faire les calculs !!!!
        _, _, n_pile = find_interval(card, piles)
        if 1 == fake_lowest_pile.value and -1 == n_pile: return card
        pile = piles[n_pile] if n_pile != -1 else fake_lowest_pile

        normalize_cards(cards, CardList([card]), piles)
        eval = eval_pile(pile) * count_combinations_pile_makes_me_loose_with_card(cards, card, pile, nb_opponents)
        print(f"{card} est perdant avec {eval}/{total_combinaisons} combinaison(s)")

        if 0 == eval: return card
        if eval < best_eval: best_card, best_eval = card, eval
    
    return best_card


def choose_card_index_wisely(cards: CardList, my_cards: CardList, piles: PileList, strategy: Strategy) -> int:
    if Strategy.RANDOM == strategy:
        return randint(0, len(my_cards)-1)
    if Strategy.FIRST == strategy:
        return 0
    if Strategy.LAST == strategy:
        return -1
    if Strategy.COUNT_FARTHEST_FROM_DIRECT_TAKE == strategy:
        # normalize_cards(cards, my_cards, piles)
        i = my_cards.index(find_best_card_by_evaluating_piles(cards, my_cards, piles))
        # normalize_cards(cards, my_cards, piles)
        return i

def choose_card_wisely(cards: CardList, my_cards: CardList, piles: PileList, strategy: Strategy) -> Card:
    return my_cards.pop(choose_card_index_wisely(cards, my_cards, piles, strategy))
