import random as rd

# Utils
def copy_board_and_set_piece(case, position):
    board = [line.copy() for line in position.board]
    i, j = case
    board[i][j] = position.piece
    return board

def remaining_cases_pieces(board):
    cases, pieces = [], list(range(16))
    for i in range(4):
        for j in range(4):
            if None == board[i][j]:
                cases.append((i,j))
            else:
                pieces.remove(board[i][j])
    rd.shuffle(cases)
    rd.shuffle(pieces)

    return cases, pieces

# TODO faire un double arbre pour limiter les calculs inutiles 
# Position
class Position:
    def __init__(self, b:list, c: tuple, p:int = None):
        self.board = b
        self.case_last_played = c
        self.children = None #self.generate_children()
        self.eval = None
        if p is None:
            cases, pieces = remaining_cases_pieces(self.board)
            p = pieces[rd.randint(0, len(pieces)-1)]
        self.piece = p

    def __repr__(self): 
        return f"Adv played on {self.case_last_played} and gave {self.piece} to play on\n{self.board}\n"

    def __str__(self): 
        return f"Adv played on {self.case_last_played} and gave {self.piece} to play on\n{self.board}\n"

        # return f"{self.piece} to play on {self.board}" #\n\nChildren position to play :\n{self.children}"
    
    def generate_children(self):
        positions = []
        cases, pieces = remaining_cases_pieces(self.board)
        pieces.remove(self.piece)
        for case in cases:
            board = copy_board_and_set_piece(case, self)
            for piece in pieces:
                positions.append(Position(board, case, piece))

        self.children = positions


## Test
# BOARD_SAMPLE_4 = [[1, 4, None, None], [2, 3, 7, 15], [14, 10, 5, None], [12, 9, 11, None]]
# position = Position(BOARD_SAMPLE_4, 5)
# print(position)
# position.generate_children()
# print(position)
