def compute_value(num):
    if 55 == num: return 7
    value = 1
    if num % 11 == 0:
        value += 4
    if num % 5 == 0:
        value += 1
    if num % 10 == 0:
        value += 1

    return value

class Card:
    def __init__(self, num: int):
        self.num = num
        self.value = None
        self.num_normalized = None

    def __repr__(self): 
        return f"{self.num}"

    def __str__(self): 
        return f"{self.num}"
    
    def getValue(self):
        if self.value is None:
            self.value = compute_value(self.num)

        return self.value 



import unittest

class TestSum(unittest.TestCase):
    def test_compute_value(self):
        self.assertEqual(compute_value(82), 1)
        self.assertEqual(compute_value(54), 1)
        self.assertEqual(compute_value(33), 5)
        self.assertEqual(compute_value(55), 7)
        self.assertEqual(compute_value(95), 2)
        self.assertEqual(compute_value(60), 3)
        self.assertEqual(compute_value(11), 5)

if __name__ == '__main__':
    unittest.main()
