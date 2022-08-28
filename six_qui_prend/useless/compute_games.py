
def compute_games(nb_games: int):
    scores_by_me = []
    scores_opponents = []
    for _ in range(nb_games):
        game = Game()
        game.play()

        for score in game.scores:
            scores_by_me.append(score.mine)
            if NB_OPPONENTS > 0:
                scores_opponents.append(score.opponents/NB_OPPONENTS)

        # s_mine, s_opponents = 0, 0
        # for score in game.scores:
        #     s_mine += score.mine
        #     if NB_OPPONENTS > 0:
        #         s_opponents += score.opponents
        # scores_by_me.append(s_mine/NB_ROUNDS_BY_GAME)
        # if NB_OPPONENTS > 0: scores_opponents.append(s_opponents/NB_OPPONENTS/NB_ROUNDS_BY_GAME)


    # print(scores_by_me.count(0))
    # print(scores_opponents.count(0))
    data_list = [scores_by_me]
    if NB_OPPONENTS > 0: data_list.append(scores_opponents)
    

    return data_list
