def compute_player_number(level):
    return (level//2)%2

def compute_player_name(player_number):
    return 'Philo' if 0 == player_number else 'Elza' 

def display_board(board):
    text = ''
    for k in range(4):
        arr_board = []
        for i in range(4):
            arr_board.append([])
            for j in range(4):
                if board[i][j] is None:
                    arr_board[i].append(9)
                else:
                    arr_board[i].append(board[i][j]%2**(k+1)//(2**k))

        text += '\n'.join(map(str, arr_board)) + '\n\n'
    return text


def is_quarto(pieces: list) -> bool:
    p1, p2, p3, p4 = pieces
    if (p1 & p2 & p3 & p4 != 0) or ((p1 ^ 15) & (p2 ^ 15) & (p3 ^ 15) & (p4 ^ 15) != 0): return True

    return False

def is_quarto_lambda_pieces(func) -> bool:
    pieces = []
    for k in range(4):
        piece = func(k)
        if piece is None:
            return False
        pieces.append(piece)

    return is_quarto(pieces)

def is_quarto_line(board, i_piece):
    return is_quarto_lambda_pieces(lambda k: board[i_piece][k])

def is_quarto_column(board, j_piece):
    return is_quarto_lambda_pieces(lambda k: board[k][j_piece])

def is_quarto_diag(board, i_piece, j_piece):
    if i_piece == j_piece and is_quarto_lambda_pieces(lambda k: board[(i_piece+k+1)%4][(j_piece+k+1)%4]): return True
    if i_piece + j_piece == 3 and is_quarto_lambda_pieces(lambda k: board[(i_piece-(k+1))%4][(j_piece+k+1)%4]): return True
    
    return False

def is_quarto_half_square(board, i_piece, j_piece):
    if i_piece < 3 and j_piece < 3 and is_quarto_lambda_pieces(lambda k: board[i_piece+k%2][j_piece+k//2]): return True #haut-gauche
    if i_piece < 3 and j_piece > 0 and is_quarto_lambda_pieces(lambda k: board[i_piece+k%2][j_piece-k//2]): return True #haut-droite
    if i_piece > 0 and j_piece < 3 and is_quarto_lambda_pieces(lambda k: board[i_piece-k%2][j_piece+k//2]): return True #bas-gauche
    if i_piece > 0 and j_piece > 0 and is_quarto_lambda_pieces(lambda k: board[i_piece-k%2][j_piece-k//2]): return True #bas-droite

def is_quarto_parmis_combinations(board, combinations):
    any(is_quarto_lambda_pieces(lambda k: board[combinaison[k][0]][combinaison[k][1]]) for combinaison in combinations)

combinations_carres_tournes = [[(0,1), (1,0), (1,2), (2,1)], [(0, 2), (1, 1), (1, 3), (2, 2)], [(1, 2), (2, 1), (2, 3), (3, 2)], [(1, 1), (2, 0), (2, 2), (3, 1)]]
def is_quarto_rotated_square(board):
    return is_quarto_parmis_combinations(board, combinations_carres_tournes)

combinations_grands_carres = [[(0, 0), (2, 0), (0, 2), (2, 2)], [(0, 1), (2, 1), (0, 3), (2, 3)], [(1, 0), (3, 0), (1, 2), (3, 2)], [(1, 1), (3, 1), (1, 3), (3, 3)]]
def is_quarto_big_square(board):
    return is_quarto_parmis_combinations(board, combinations_grands_carres)

def is_quarto_eval_board(board, case):
    i, j = case
    if is_quarto_line(board, i) or is_quarto_column(board, j): return True
    if is_quarto_diag(board, i, j): return True
    # if is_quarto_half_square(board, i, j): return True
    # if is_quarto_rotated_square(board): return True
    # if is_quarto_big_square(board): return True

    return False

def is_game_over(eval) -> bool:
    return 0 != eval

def evaluate_position(position):
    eval = is_quarto_eval_board(position.board, position.case_last_played) * 1
    position.eval = eval
    
    return eval
