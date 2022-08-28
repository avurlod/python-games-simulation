from random import randint
from card import Card
from type.strategy import Strategy
from type.card_list import CardList
from pile import Pile
from type.pile_list import PileList
from constants import *
import numpy as np

def choose_smallest_pile(piles: PileList) -> Pile:
    return min(piles, key= lambda x:x.value)

def find_interval(card: Card, piles: PileList):
    c_1, c_2 = -np.inf, piles[0].card_on_top.num
    n_pile = -1

    # dois-je passer à la pile suivante ?
    while c_2 < card.num and n_pile < len(piles):
        n_pile += 1
        c_1 = piles[n_pile].card_on_top.num
        c_2 = np.inf if n_pile+1 == len(piles) else piles[n_pile+1].card_on_top.num

    # print(f"#{n_pile} c_1, c_2 == {c_1} {c_2}")

    return c_1, c_2, n_pile

def play_cards(cards_to_play: CardList, piles: PileList):
    points_taken_by_cards = []
    for card in cards_to_play:
        c_1, c_2, n_pile = find_interval(card, piles)

        # si la carte est à gauche de la première pile
        if -np.inf == c_1:
            points = choose_smallest_pile(piles).reset_with_card(card)
            piles.sortByNum()

        # si je suis entre deux tas
        elif c_1 < card.num < c_2: points = piles[n_pile].add_card(card)

        # si la carte est à droite de la dernière pile
        elif np.inf == c_2: points = piles[-1].add_card(card)
        
        if 0 != points: points_taken_by_cards.append((card.num, points)) 

    return points_taken_by_cards
