from constants import DEBUG
from game import Game
import statistics
import matplotlib.pyplot as plt

from type.strategy import Strategy

SHOW_PROFILER = True
NB_GAMES = 1000

def plot_data(data: list, label: str):
    plt.close()
    plt.hist(data, bins=list(x/30 for x in range(31)), label=label)

    plt.xlabel("% mon score / (mon score + score_adv moyen)")
    plt.ylabel("Nombre de parties")
    plt.legend()
    plt.show()

def compute_games(nb_games: int, strategy: Strategy):
    return [Game(strategy).end_metric() for _ in range(nb_games)]

def compute_strategy(strategy: Strategy):
    data = compute_games(NB_GAMES, strategy)
    mu = statistics.mean(data)
    
    # sigma = statistics.stdev(data)
    # med = statistics.median(data)

    diff = (1-2*mu)*100
    text = "{:^5.0f} avec la stratégie {}".format(diff, strategy.name)
    if DEBUG:
        if diff < 0:
            text += " -> l'adversaire est meilleur en moyenne : je fais {:.0f} points de plus que l'adv".format(-diff)
        else:
            text += " -> je suis meilleur en moyenne : je fais {:.0f} points de moins que l'adv".format(diff)
        text += " sur une partie de 100 points"
    print(text)
    # label = "{:.2%} +/- {:.2%} (med = {:.2%})".format(mu, 3*sigma/sqrt(len(data)), med)
    # print(label)
    # plot_data(data, label)
    
def main():
    print(f"\nSur {NB_GAMES} parties :\n")
    for strategy in list(Strategy):
        compute_strategy(strategy)
    print()


if SHOW_PROFILER:
    if __name__ == '__main__':
        import cProfile, pstats
        profiler = cProfile.Profile()
        profiler.enable()
        main()
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime')
        stats.print_stats(15)
        stats = pstats.Stats(profiler).sort_stats('tottime')
        stats.print_stats(10)
else:
    main()


# todo choisi de manière maligne pour préparer le coup d'après qaund j'ai plusieurs cartes qui s'enchainent 
