from card import Card
from pile import Pile
from random import randint, shuffle
from typing import Tuple, List
from constants import *
from utils import *

CardList = List[Card]
PileList = List[Pile]

def display_state_of_game(cards, cards_in_my_hand, piles):
    print('\nI can play', cards_in_my_hand)
    for pile in piles: print(pile)

def setup() -> Tuple[CardList, CardList, CardList]:
    cards = list(Card(num) for num in range(1, NB_CARDS+1))
    shuffle(cards)
    cards_in_my_hand = list(cards.pop() for _ in range(NB_CARDS_IN_HAND))
    piles = list(Pile(cards.pop()) for _ in range(NB_PILES))

    cards.sort(key= getCardNum)
    cards_in_my_hand.sort(key= getCardNum)
    piles.sort(key = getPileNum)

    return cards, cards_in_my_hand, piles

def play_one_turn(cards: CardList, cards_in_my_hand: CardList, piles: PileList):
    cards_played_by_opponents = list(cards.pop(randint(0, len(cards)-1)) for _ in range(NB_OPPONENTS))
    card_by_me = cards_in_my_hand.pop()

    cards_to_play = list(cards_played_by_opponents)
    cards_to_play.append(card_by_me)
    cards_to_play.sort(key=getCardNum)
    print(f"I'll play {card_by_me}, within {cards_to_play}")
    play_cards(cards_to_play, piles)


def play():
    cards, cards_in_my_hand, piles = setup()

    display_state_of_game(cards, cards_in_my_hand, piles)
    for _ in range(NB_CARDS_IN_HAND):
        play_one_turn(cards, cards_in_my_hand, piles)
        display_state_of_game(cards, cards_in_my_hand, piles)


play()
