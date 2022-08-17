from itertools import count
import numpy as np
import random as rd

BOARD_EMPTY = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
BOARD_SAMPLE_2 = [[1, 4, 8, None], [2, 3, 7, 15], [14, 10, 5, 13], [12, 9, 11, None]]
BOARD_SAMPLE_3 = [[1, 4, 8, None], [2, 3, 7, 15], [14, 10, 5, None], [12, 9, 11, None]]
BOARD_SAMPLE_4 = [[1, 4, None, None], [2, 3, 7, 15], [14, 10, 5, None], [12, 9, 11, None]]
BOARD_SAMPLE_6 = [[1, 4, None, None], [None, 3, None, 15], [14, 10, 5, None], [12, 9, 11, None]]
BOARD_SAMPLE_7 = [[1, 4, None, None], [None, None, None, 15], [14, 10, 5, None], [12, 9, 11, None]]
BOARD_WON = [[1, 2, 3, None], [None, 13, 7, None], [14, 10, 5, None], [12, 9, 11, 6]]


#grand, rond, blanc, pointé

BOARD_TO_PLAY = BOARD_SAMPLE_3

EMPTY_CASE_DISPLAYING = ' '

DISPLAY_BOARD = False
DISPLAY_TREE = True

def display_board_converted(board):
    arr_board = []
    for i in range(4):
        arr_board.append([])
        for j in range(4):
            if board[i][j] is None:
                arr_board[i].append(EMPTY_CASE_DISPLAYING)
            else:
                arr_board[i].append(format(board[i][j],'b').zfill(4))
    return '\n '.join(map(str, arr_board))

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


def compute_player_number(level):
    return (level//2)%2

def compute_player_name(player_number):
    return 'Philo' if 0 == player_number else 'Elza' 

def remaining_cases_pieces(board = BOARD_EMPTY):
    cases, pieces = [], list(range(16))
    for i in range(4):
        for j in range(4):
            if None == board[i][j]:
                cases.append((i,j))
            else:
                pieces.remove(board[i][j])
    
    return cases, pieces

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
    # if is_quarto_diag(board, i, j): return True
    # if is_quarto_half_square(board, i, j) or is_quarto_rotated_square(board): return True
    # if is_quarto_big_square(board): return True

    return False




# Objectif : trouver la pièce que doit donner J0 pour gagner à coup sûr
def compute_what_piece_to_give(board):
    cases, pieces = remaining_cases_pieces(board)
    winning_pieces = []
    counter_sum = 0
    for piece in pieces:
        eval, counter = eval_board_with_given_piece(board, cases, 0, 1, piece, pieces)
        counter_sum += counter
        if eval:
            winning_pieces.append(piece)

    return winning_pieces, counter_sum

# Objectif : trouver la case où que doit jouer J0 pour gagner à coup sûr
def compute_where_to_play(board, piece = None):
    cases, pieces = remaining_cases_pieces(board)
    if piece is None:
        piece = pieces[0]
    winning_cases = []
    counter_sum = 0
    for case in cases:
        eval, counter = eval_board_when_played_on_case(board, case, cases, 0, 0, piece, pieces)
        counter_sum += counter
        if eval:
            winning_cases.append(case)

    return winning_cases, counter_sum



def all_with_counter(iterable):
    counter_sum = 0
    for element, counter in iterable:
        counter_sum += counter
        if not element:
            return False, counter_sum
    return True, counter_sum

def any_with_counter(iterable):
    counter_sum = 0
    for element, counter in iterable:
        counter_sum += counter
        if element:
            return True, counter_sum
    return False, counter_sum


# retourne True si dans cette situation le J0 est gagnant
def eval_board_with_given_piece(board, cases, counter, level, piece, pieces):
    player_number = compute_player_number(level)
    if DISPLAY_TREE: print(f"{player_number} {'---' * level} Don {piece}")
    
    # if the player who is to give a piece is me, any piece that would bring me victory suits me
    if 0 == player_number:
        return all_with_counter(eval_board_when_played_on_case(board, case, cases, counter, level+1, piece, pieces) for case in cases)
    return any_with_counter(eval_board_when_played_on_case(board, case, cases, counter, level+1, piece, pieces) for case in cases)


# retourne True si dans cette situation le J0 est gagnant
def eval_board_when_played_on_case(board, case, cases, counter, level, piece, pieces):
    player_number = compute_player_number(level)
    new_board = [line.copy() for line in board]
    i, j = case
    new_board[i][j] = piece
    eval, new_counter = is_quarto_eval_board(new_board, case), counter + 1
    if DISPLAY_TREE: print(f"{player_number} {'---' * level}- Joue {case}")
    if eval:
        if DISPLAY_TREE: print(f"{player_number} {'---' * level}---> {'Quarto ! :)' if 0 == player_number else 'XXX'}")
        return 0 == player_number, 1
    else:
        if 1 == len(pieces): return None, new_counter

        remaining_cases = list(cases)
        remaining_cases.remove(case)
        rd.shuffle(remaining_cases)
        remaining_pieces = list(pieces)
        remaining_pieces.remove(piece)
        rd.shuffle(remaining_pieces)
        # if the player who is to give a piece is me, any piece that would bring me victory suits me
        if 0 == player_number:
            return any_with_counter(eval_board_with_given_piece(new_board, remaining_cases, new_counter, level+1, piece, remaining_pieces) for piece in remaining_pieces)
        # if the player who is to give a piece is MY OPPONENT, any would bring me victory suits me
        return all_with_counter(eval_board_with_given_piece(new_board, remaining_cases, new_counter, level+1, piece, remaining_pieces) for piece in remaining_pieces)
        
def translate_url_to_board(texte):
    board = [list(list(range(4))) for i in range(4)]
    liste = texte.split("&")
    for v in liste:
        pre_case, piece = v[1:].split("=")
        i = int(pre_case)//4
        j = int(pre_case)%4
        board[i][j] = None if '-1' == piece else int(piece)
    return board

# BOARD_VS_IA = [[4, 8, 12, 7], [None, 6, 1, None], [10, 14, 11, 5], [None, 3, None, 9]]
# # noir = 8
# # rond = 4
# # petit = 2
# # pointé = 1

# texte = "B0=-1&B1=-1&B2=2&B3=-1&B4=1&B5=-1&B6=6&B7=9&B8=-1&B9=4&B10=3&B11=-1&B12=12&B13=8&B14=13&B15=7"
# board = translate_url_to_board(texte)
# print(board,"\n")
# # board = BOARD_SAMPLE_7
# piece_to_play = 11

def main():
    piece_to_play = None
    board = BOARD_TO_PLAY

    if piece_to_play is None:
        res = compute_what_piece_to_give(board)
        print('compute_what_piece_to_give\n', res,'\n\n')
    else:
        res = compute_where_to_play(board, piece_to_play)
        print('compute_where_to_play\n', res)

    if DISPLAY_BOARD: print(display_board(board))
    
main()
