from constants import NB_OPPONENTS

class Score:
    def __init__(self):
        self.mine = 0
        self.opponents = 0

    def __repr__(self): 
        return f"{self.mine}"

    def __str__(self): 
        return "My score : {}\nOpponent : {:n}\n".format(self.mine, self.opponents/NB_OPPONENTS)
