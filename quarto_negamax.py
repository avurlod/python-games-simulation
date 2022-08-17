from cgi import print_arguments
import numpy as np
from quarto import utils as u
from quarto.position import Position
from quarto.display_tree import text_of_tree

def negamax(position, depth, alpha = -np.inf, beta = np.inf, first_player = True):
    eval = u.evaluate_position(position) 
    if depth == 0 or u.is_game_over(eval):
        return eval, [position]

    position.generate_children()
    eval_max, lineage_best = -np.inf, []
    for child in position.children:
        eval, lineage = negamax(child, depth - 1, -beta, -alpha, not(first_player))
        if eval_max < -eval:
            eval_max, lineage_best = -eval, lineage

        alpha = max(alpha, eval_max)
        if beta <= alpha:
            break

    lineage_best.append(position)
    return eval_max, lineage_best

# Test
BOARD_FORCED_VICTORY = [[None, 4, None, 8], [None, None, None, 15], [14, 10, 5, None], [12, 9, None, None]]
BOARD_SAMPLE_5 = [[14, 4, None, None], [2, 3, None, 15], [1, 10, 5, None], [12, 9, 11, None]]
BOARD_WON = [[1, 2, 3, None], [None, 13, 7, None], [14, 10, 5, None], [12, 9, 11, 6]]
BOARD_SAMPLE_3 = [[1, 4, 8, None], [2, 3, None, 15], [14, 10, 5, 13], [12, 9, 11, None]]

current_position = Position(BOARD_SAMPLE_3, (0,1))

# initial call
# I am player 1
# I am given a piece
# I am the maximising player
# I want to know which case play and witch piece to give, to maximize my winning possibilities
# print(u.display_board(current_position.board))
eval, lineage = negamax(current_position, 2)
print(current_position.children)
# print('lineage', lineage)
# for p in lineage:
#     print(p)

# print('Score de la position actuelle', eval)
best_position = lineage[-1]
# print('Meilleur coup à jouer :', best_position.case_last_played, '\nEt donner la piece', best_position.piece)
print(text_of_tree(current_position))
