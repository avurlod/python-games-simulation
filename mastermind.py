from random import randint
from collections import Counter
from matplotlib import pyplot
from loadbar import LoadBar
from numpy import array
import cProfile
#import snakeviz


showProfiler = False

nbColums = 6
nbColors = 8
nbMax = 12
iMax = 1
insideText = True and iMax <= 5 and not(showProfiler)
showMatrixPossibilities = insideText and True
showGraph = True and (not(insideText) and iMax > 1)
customSolution = [] #[7,4,6,3,1,4]

#from itertools import product
def product(*args, repeat=1):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]

    return result

def generateRandomCombination(combinations):
    return combinations[randint(0, len(combinations)-1)]

def initializeCombinations():
    return product(range(1,nbColors+1,1), repeat=nbColums)

def nextAttempt(combinations, nb):
    #return generateRandomCombination(combinations)

    if nb == 1:
        return [1,1,2,2,3,3]
    elif nb == 2:
        return [1,1,4,4,5,5]
    elif nb == 3:
        return [1,1,6,6,7,7]
    elif nb == 4:
        return [1,1,8,8,7,7]
        return [1,1,6,6,8,8]

    # elif nb == 5:
    #     return [2,4,5,1,6,7]
    # elif nb == 6:
    #     return [3,4,1,6,7,4]
    # elif nb == 7:
    #     return [4,3,1,6,4,7]
    # elif nb == 8:
    #     return [3,4,4,1,7,6]

    else:
        return generateRandomCombination(combinations)

def countInCommonPlaced(a1,a2):
    sum = 0
    for j in range(nbColums):
        if a1[j] == a2[j]:
            sum += 1

    return sum
    #return sum(1 for j in range(nbColums) if a1[j] == a2[j])

def listsOfZeros():
    return [0 for i in range(nbColors)],[0 for i in range(nbColors)]

def countInCommon(a1,a2):
    colors1, colors2 = listsOfZeros()

    for j in range(nbColums):
        colors1[a1[j]-1] += 1
        colors2[a2[j]-1] += 1

    return sum(min(colors1[i], colors2[i]) for i in range(nbColors))

def computeResult(attempt, solution):
    placed = 0
    a = attempt[:]
    s = solution[:]

    for j in range(nbColums-1, -1, -1):
        if (a[j] == s[j]):
            placed += 1
            a[j] = 0
            s[j] = 0

    return placed, countInCommon(a,s) - placed

def testCombinations(combinations, lastAttempt, lastPlaced, lastMisplaced):
    newCombinations = []
    for c in combinations:
        if lastPlaced != countInCommonPlaced(lastAttempt, c):
            continue

        if lastPlaced + lastMisplaced == countInCommon(c, lastAttempt):
            newCombinations.append(c)

    return newCombinations

def possibilitiesMatrix(combinations):
    matrix = []
    for i in range(nbColors):
        matrix.append([])
        for j in range(nbColums):
            matrix[i].append(1)

    for c in combinations:
        for j in range(nbColums):
            matrix[c[j]-1][j] = 0

    for i in range(nbColors):
        for j in range(nbColums):
            matrix[i][j] = (1+i)*(1 - matrix[i][j])

    return matrix

def playGame(combinations):
    solution = generateRandomCombination(combinations) if customSolution == [] else customSolution

    if insideText:
        print("Solution",solution,"\n----\n")

    attempt = nextAttempt(combinations, 1)

    nb=0
    possibilitesAtFive = None
    success = False
    while not(success) and nb < nbMax:
        nb += 1
        # generate the result
        placed, misplaced = computeResult(attempt, solution)

        if insideText:
            print(format(len(combinations),'-6d'),"possibles. Essai n°" + format(nb,'02d') + ":",attempt,"-> ",placed,";",misplaced)

        if nb == 5:
            possibilitesAtFive = len(combinations)
        if (placed == nbColums):
            break

        # test witch combinations are compatibles with previous result
        combinations = testCombinations(combinations, attempt, placed, misplaced)

        if showMatrixPossibilities:
            print(array(possibilitiesMatrix(combinations)))

        # generate next attempt
        attempt = nextAttempt(combinations, nb+1)

    if insideText:
        if nb >= nbMax:
            print("\nDéfaite ... :/\n")
        else:
            print("\nVICTOIREEEE :D ->",nb,"essais\n")

    if placed != nbColums:
        nb = nbMax + 1

    return nb, possibilitesAtFive


def main():
    i = 0
    i0 = max(1, iMax // 10)
    scores = []
    possibilitesAtFives = []
    combinations = initializeCombinations()
    bar = LoadBar(max=iMax, show_time=True)
    bar.start()
    while i < iMax:
        i += 1
        if insideText:
            print("\nPartie n°"+str(i)+" !")
        nb, possibilitesAtFive = playGame(combinations[:])
        scores.append(nb)
        possibilitesAtFives.append(possibilitesAtFive)
        if 0 == i%i0:
            bar.update(step=i)
    bar.end()

    if possibilitesAtFives != [None]:
        print(min(possibilitesAtFives),"-",max(possibilitesAtFives),":",sum(possibilitesAtFives)/len(possibilitesAtFives),"essais restants en moyenne après 4 coups")
    #print(Counter(scores))
    pyplot.close()
    points, limits, rectangles = pyplot.hist(scores, density=True, cumulative=True, range = (0, 13), bins = 13)
    print("% de chances de victoire au 9ème essai :",points[8])
    print("% de chances de victoire au 12ème essai :",points[11])
    if showGraph:
        pyplot.show()

if showProfiler:
    if __name__ == '__main__':
        import cProfile, pstats
        profiler = cProfile.Profile()
        profiler.enable()
        main()
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('tottime')
        stats.print_stats(10)
else:
    main()
