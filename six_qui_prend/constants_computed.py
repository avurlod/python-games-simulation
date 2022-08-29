from random import shuffle
from card import Card
from type.card_list import CardList
from constants import NB_CARDS

CARDS_SHUFFLED = CardList(Card(num) for num in range(1, NB_CARDS+1))
shuffle(CARDS_SHUFFLED)
shuffle(CARDS_SHUFFLED)
