import numpy as np

def count_arrangements(k: int, n: int) -> int: #k parmis n
    if 0 == n: return 0

    acc = 1
    for i in range(k):
        acc *= n-i

    return acc

def binomial(k, n):
    if 0 <= k <= n:
        a= 1
        b=1
        for t in range(1, min(k, n - k) + 1):
            a *= n
            b *= t
            n -= 1
        return a // b
    else:
        return 0

## 1 2 3 ... c-1 c c+1 ... c_max-1 c_max
def count_arrangements_i_cards_below_c(i: int, i_max: int, c: int, c_max: int) -> int:
    assert 0 <= i
    assert i <= i_max
    assert i < c
    assert c <= c_max

    return binomial(i, i_max) * count_arrangements(i, c-1) * count_arrangements(i_max-i, c_max-c)

def sum_of_arrangements_i_cards_below_c(i_max: int, c: int, c_max: int) -> int:
    return sum(count_arrangements_i_cards_below_c(i, i_max, c, c_max) for i in range(i_max+1))


# si je joue x_0 et que le haut du tas est c, et qu'il y a qu'une place, et que j'ai qu'un seul adversaire, dans cb de cas je suis perdant sur toutes les cartes possibles
def count_loosing_cards(x_0, c, cards_available):
    return sum(1 if c < x_1 < x_0 else 0 for x_1 in cards_available)    

# si il reste 4 cartes à jouer, quelle est la proba que je perde si le joueur joue au hasard ?
def proba_loosing_cards_one_card(x_0, c, cards_available):
    return count_loosing_cards(x_0, c, cards_available)/len(cards_available)

# si j'ai 4 cartes dans la main, et qu'il y a un tas, quelle est la proba que je prenne pour chaque carte ?
def proba_loosing_cards_multi_cards(my_cards, c, cards_available):
    return list((x_0, proba_loosing_cards_one_card(x_0, c, cards_available)) for x_0 in my_cards)

# si j'ai 4 cartes dans la main, et qu'il y a 3 tas c_1 c_2 c_3, pour chaque carte et chaque tas combien de cartes peuvent me sauver ?
def count_loosing_cards_multi_cards_multi_tops(my_cards, cards_on_top, cards_available):
    l = []
    n = len(cards_available)
    for x_0 in my_cards:
        l_x_0 = []

        s = 0
        i = 0
        c_1, c_2 = -np.inf, cards_on_top[0]
        for x_1 in cards_available:
            # print('s=',s,'==>', x_1)
            # print(c_1,c_2)

            # dois-je passer au tas suivant ?
            while c_2 < x_1 and i < len(cards_on_top):
                if c_1 < x_0 < c_2 : s = n-s
                l_x_0.append((c_1, s))
                s = 0
                c_1, c_2 = cards_on_top[i], np.inf if i == len(cards_on_top) - 1 else cards_on_top[i+1] 
                i += 1
            # print(l_x_0)
            # print(c_1,c_2)
            # # suis-je déjà trop loin ?
            # if x_0 < x_1:
            #     while i < len(cards_on_top):
            #         c_1 = cards_on_top[i]
            #         l_x_0.append((c_1, 0))
            #         i += 1
            #     break

            # si je suis à gauche du premier tas
            if x_0 < c_1 and x_0 < x_1 and i == 0: s += 1

            # si je suis entre deux tas
            if c_1 < x_1 < x_0 < c_2: s += 1

            # # si je suis à droite du dernier tas
            # if i == len(cards_on_top) - 1:
            #     c_1 = cards_on_top[i]
            #     c_2 = np.inf
            #     if c_1 < x_1 < x_0: s += 1
            # print('c_1, x_1, x_0, c_2, i, s', c_1, x_1, x_0, c_2, i, s,'\n')

        if c_1 < x_0 < c_2 : s = n-s
        l_x_0.append((c_1, s))
        l.append((x_0, l_x_0))

    return l

# si j'ai 4 cartes dans la main, et qu'il y a 2 tas c_1 c_2, quelle est la proba que je prenne pour chaque carte ?
def proba_loosing_cards_multi_cards_multi_tops(my_cards, cards_on_top, cards_available):
    l_count = count_loosing_cards_multi_cards_multi_tops(my_cards, cards_on_top, cards_available)
    l = []
    for x_0, l_x_0 in l_count:
        l.append((x_0, list((c_1, s/len(cards_available)) for c_1, s in l_x_0)))
    return l

# TOD O simuler une partie contre 1 adversaire
# TOD O structurer un tas pour connaître le poids
# TOD O calculer l'espérance de gain en jouant une carte
# TOD O élargir quand il y a + d'un seul adversaire qui joue
# TOD O simuler une partie à plusieurs joueurs
# TOD O élargir quand il y a + qu'une seule place avant de prendre le tas



import unittest

# class TestSum(unittest.TestCase):

if __name__ == '__main__':
    unittest.main()
