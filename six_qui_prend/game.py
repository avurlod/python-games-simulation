from pickletools import read_uint1
from constants import NB_OPPONENTS, NB_ROUNDS_BY_GAME
from round import Round
from score_list import ScoreList
from type.strategy import STRATEGY_DEFAULT, Strategy

class Game:
    def __init__(self, strategy: Strategy = STRATEGY_DEFAULT):
        self.scores : ScoreList = []
        self.strategy = strategy

    def __str__(self):
        return str(self.scores)

    def play(self, ):
        for _ in range(NB_ROUNDS_BY_GAME):
            round = Round()
            round.play(self.strategy)
            self.scores.append(round.score)
            del round

    def end_metric(self):
        self.play()

        s_mine = sum(score.mine for score in self.scores)
        if 0 == NB_OPPONENTS: return s_mine

        s_opponents = sum(score.opponents for score in self.scores)

        return s_mine/(s_mine + s_opponents/NB_OPPONENTS)


if __name__ == '__main__':
    game = Game()
    game.play()
