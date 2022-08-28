from card import Card
from constants import DEBUG, NB_CARDS_IN_HAND, NB_CARDS, NB_OPPONENTS, NB_PILES
from pile import Pile
from random import shuffle
from score import Score
from type.card_list import CardList
from type.pile_list import PileList
from type.strategy import STRATEGY_DEFAULT, Strategy
from typing import Tuple
from utils import play_cards
from utils_strategy import *

class Round:
    def __init__(self):
        cards, my_cards, piles = self.__setup()
        self.my_cards = my_cards
        self.cards = cards
        self.piles = piles
        self.score = Score()

    # def __str__(self):
    #     text = f"I can play {self.my_cards}\n"
    #     for pile in self.piles: text += str(pile)
    #     return text + str(self.score)

    def __setup(self) -> Tuple[CardList, CardList, PileList]:
        cards = CardList(Card(num) for num in range(1, NB_CARDS+1))
        shuffle(cards)
        shuffle(cards)
        my_cards = CardList(cards.pop() for _ in range(NB_CARDS_IN_HAND))
        piles = PileList(Pile(cards.pop()) for _ in range(NB_PILES))

        my_cards.sortByNum()
        piles.sortByNum()

        return cards, my_cards, piles

    def update_score_after_turn(self, points_taken_by_cards, num_by_me: int):
        for (num, points) in points_taken_by_cards:
            if num == num_by_me:
                self.score.mine += points
                if DEBUG: print("*** J'ai pris", points, "points avec le", num)
            else: self.score.opponents += points

    def play_one_turn(self, strategy: Strategy = STRATEGY_DEFAULT):
        card_by_me = choose_card_wisely(self.cards, self.my_cards, self.piles, strategy)

        cards_played_by_opponents = CardList(self.cards.pop() for _ in range(NB_OPPONENTS))
        cards_to_play = CardList(cards_played_by_opponents)
        cards_to_play.append(card_by_me)
        cards_to_play.sortByNum()
        if DEBUG: print(f"Remaining cards are: {self.my_cards}")
        if DEBUG: print(self.piles)
        if DEBUG: print(f"I'll play {card_by_me}, within {cards_to_play}")
        self.update_score_after_turn(play_cards(cards_to_play, self.piles), card_by_me.num)
        print()

    def play(self, strategy: Strategy = STRATEGY_DEFAULT):
        if DEBUG: print(f"My cards are: {self.my_cards}\n\n")
        for _ in range(NB_CARDS_IN_HAND):
            self.play_one_turn(strategy)
        if DEBUG: print(f"Final score:\n{self.score}")


if __name__ == '__main__':
    Round().play()
