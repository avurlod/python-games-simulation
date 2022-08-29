from bisect_mine import bisect
from card import Card
from constants import DEBUG, NB_CARDS_MAX_FOR_PILE, NB_OPPONENTS
from numpy import inf
from pile import Pile
from random import randint
from type.card_list import CardList, getCardNum
from type.pile_list import PileList
from type.strategy import Strategy
from utils import choose_smallest_pile, find_interval

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

def find_cards_possible_between(cards: CardList, min: int, max: int):
    i_min = bisect(cards, min, key=getCardNum)
    i_max = bisect(cards, max-1, key=getCardNum)

    return cards[i_min:i_max]

def compute_excepted_value_of_pile_taken_with_card(cards: CardList, card: Card, pile: Pile, nb_opponents: int = NB_OPPONENTS):
    # none if card is below pile
    if card.num < pile.card_on_top.num: return 0

    nb_cards_to_put = pile.nb_cards_to_put()
    # none if not enough opponents between pile and card
    if nb_opponents < nb_cards_to_put: return 0

    cards_between = find_cards_possible_between(cards, pile.card_on_top.num, card.num)

    nb_cards_between = len(cards_between)
    # none if not enough space between pile and card
    if nb_cards_between < nb_cards_to_put: return 0

    sum_cards_between_value = sum(card.get_value() for card in cards_between)
    average_value = pile.value if 0 == nb_cards_between else pile.value + sum_cards_between_value/nb_cards_between

    count_combinations_in = binomial(nb_cards_to_put, nb_cards_between)
    count_combinations_out = binomial(nb_opponents - nb_cards_to_put, len(cards) - nb_cards_between)
    count_combinations_all = binomial(nb_opponents, len(cards))
    proba_combinations = count_combinations_in * count_combinations_out / count_combinations_all

    return average_value * proba_combinations

def fake_pile_with_O_on_top(piles: PileList):
    pile = Pile(Card(0))
    pile.value = choose_smallest_pile(piles).value
    pile.size = NB_CARDS_MAX_FOR_PILE-1
    return pile

def eval_pile(pile: Pile):
    return pile.value + pile.nb_cards_to_put()

def find_best_card_by_evaluating_piles(cards: CardList, my_cards: CardList, piles: PileList, nb_opponents: int = NB_OPPONENTS) -> Card:
    best_card = my_cards[0]
    best_eval = inf
    fake_lowest_pile = fake_pile_with_O_on_top(piles)
    for card in my_cards:
        _, _, n_pile = find_interval(card, piles)
        pile = piles[n_pile] if n_pile != -1 else fake_lowest_pile

        eval = compute_excepted_value_of_pile_taken_with_card(cards, card, pile, nb_opponents)
        if DEBUG: print("Espérance de {:>3.2f} avec {:<2} sur la pile {}".format(eval, card.num, pile.card_on_top.num))

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
    if Strategy.MINIMIZE_EXCEPTED_VALUE == strategy:
        return my_cards.index(find_best_card_by_evaluating_piles(cards, my_cards, piles))

def choose_card_wisely(cards: CardList, my_cards: CardList, piles: PileList, strategy: Strategy) -> Card:
    return my_cards.pop(choose_card_index_wisely(cards, my_cards, piles, strategy))
