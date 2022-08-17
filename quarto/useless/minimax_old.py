import numpy as np
from quarto import utils as u

def minimax(position, depth, alpha = -np.inf, beta = np.inf, maximizing_player = True):
    eval = u.evaluate_position(position, maximizing_player)
    # print(depth, '---', 'EVAL', eval, maximizing_player, '\n')
    if depth == 0 or u.is_game_over(eval):
        # if u.is_game_over(eval):
            # print('QUARTO !!', position)
        return eval, [position]

    position.generate_children()
    if maximizing_player:
        eval_max, child_best, lineage_best = -np.inf, None, []
        for child in position.children:
            # print(depth, '---', 'child', child)
            eval, lineage = minimax(child, depth - 1, alpha, beta, False)
            if eval_max < eval:
                eval_max, child_best, lineage_best = eval, child, lineage
                # print('lineage_best', lineage_best)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        lineage_best.append(position)
        return eval_max, lineage_best

    else:
        eval_min, child_best, lineage_best = np.inf, None, []
        for child in position.children:
            # print(depth, '------', 'child', child)
            eval, lineage = minimax(child, depth - 1, alpha, beta, True)
            if eval < eval_min:
                eval_min, child_best, lineage_best = eval, child, lineage
                # print('lineage_best', lineage_best)
            beta = min(beta, eval)
            if beta <= alpha:
                break

        lineage_best.append(position)
        return eval_min, lineage_best
