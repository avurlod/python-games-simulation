from game import Game
import statistics
import matplotlib.pyplot as plt

from type.strategy import Strategy

SHOW_PROFILER = False
NB_GAMES = 10

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
    text = f"Avec la stratégie {strategy.name}, "
    if diff < 0:
        text += "l'adversaire est meilleur en moyenne : je fais {:.0f} points de plus que l'adv".format(-diff)
    else:
        text += "je suis meilleur en moyenne : je fais {:.0f} points de moins que l'adv".format(diff)
    text += " sur une partie de 100 points"
    print(text)
    # label = "{:.2%} +/- {:.2%} (med = {:.2%})".format(mu, 3*sigma/sqrt(len(data)), med)
    # print(label)
    # plot_data(data, label)
    
def main():
    for strategy in list(Strategy):
        compute_strategy(strategy)


if SHOW_PROFILER:
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



# todo optimiser vitesse
# todo implémenter CALCUL ESPERENCE BOUUUM
