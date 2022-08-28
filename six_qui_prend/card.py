class Card:
    def __init__(self, num: int):
        self.num = num
        self.value = None
        self.num_normalized = None

    def __repr__(self): 
        return f"{self.num}"

    def __str__(self): 
        return f"{self.num}"
    
    def __compute_value(self):
        if 55 == self.num: return 7

        value = 1
        if self.num % 11 == 0:
            value += 4
        if self.num % 5 == 0:
            value += 1
        if self.num % 10 == 0:
            value += 1

        return value

    def get_value(self):
        if self.value is None:
            self.value = self.__compute_value()

        return self.value 

    def get_num(self) -> int:
        return self.num if self.num_normalized is None else self.num_normalized

