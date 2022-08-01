from random import randint
from matplotlib import pyplot

# Règles du jeu
CARTES_PERSONNAGES = ['Leblanc', 'Pervenche', 'Moutarde', 'Rose', 'Olive', 'Violet']
CARTES_ARMES = ['Poignard', 'Chandelier', 'Revolver', 'Corde', 'Matraque', 'Clef Anglaise']
CARTES_LIEUX = ['Cuisine', 'Grand Salon', 'Petit salon', 'Salle à Manger', 'Bureau', 'Bibliothèque', 'Véranda', 'Hall', 'Studio']

# Paramètres
nb_joueurs = 4
nb_parties = 1
AFFICHE_TEXTE = nb_parties == 1
AFFICHE_PROFILER = True
AFFICHE_GRAPH = not(AFFICHE_TEXTE) and True

# Constantes globales
CARTES = {'p': CARTES_PERSONNAGES, 'a': CARTES_ARMES, 'l': CARTES_LIEUX}
CARTES_TYPES = list(CARTES.keys())


## Mise en place
def choisi_tueur(cartes):
    tueur_cartes = {}
    for carte_type in CARTES_TYPES:
        cartes_noms = cartes[carte_type]
        carte_nom = cartes_noms.pop(randint(0, len(cartes_noms)-1))
        tueur_cartes[carte_type] = carte_nom

    return tueur_cartes

def distribution(cartes):
    cartes_joueurs = [{} for i in range(nb_joueurs)]
    for i in range(nb_joueurs):
        for carte_type in CARTES_TYPES:
            cartes_joueurs[i][carte_type] = []

    i = 0
    for carte_type in CARTES_TYPES:
        while cartes[carte_type] != []:
            cartes_noms = cartes[carte_type]
            carte_nom = cartes_noms.pop(randint(0, len(cartes_noms) - 1))
            cartes_joueurs[i%nb_joueurs][carte_type].append(carte_nom)
            i += 1

    return cartes_joueurs

# f = [feuille par joueur]
# feuille = { a: p: l: }
# a: { leblanc: pervenche: }
# leblanc: [ 0 1 2 ]
def initialise_feuilles(cartes_joueurs):
    feuilles = [{} for i in range(nb_joueurs)]
    for i in range(nb_joueurs):
        for carte_type in CARTES_TYPES:
            feuilles[i][carte_type] = {}
            for carte_nom in CARTES[carte_type]:
                feuilles[i][carte_type][carte_nom] = [1 if i == k else 0 for k in range(nb_joueurs)]


    for i in range(nb_joueurs):
        cartes_joueur = cartes_joueurs[i]
        for carte_type in CARTES_TYPES:
            cartes_noms = cartes_joueur[carte_type]
            for carte_nom in cartes_noms:
                for num_joueur in range(nb_joueurs):
                    feuilles[i][carte_type][carte_nom][num_joueur] = 1
                feuilles[i][carte_type][carte_nom][i] = 2

    return feuilles


## Affichage
def texte_cartes(cartes_joueur):
    texte = ""
    for type_carte in cartes_joueur.keys():
        texte += type_carte + " : " + str(cartes_joueur[type_carte]) + "\n"
    texte += "\n"

    return texte

def affiche_joueurs(cartes_joueurs):
    texte = ""
    num_joueur = 0
    for cartes_joueur in cartes_joueurs:
        texte += "## Joueur " + str(num_joueur) + "\n" + texte_cartes(cartes_joueur)
        num_joueur += 1

    print(texte)

# 0 : pas d'information
# 1 : n'a pas la carte
# 2 : a la carte
def affiche_feuilles(feuilles):
    texte = ""
    for i in range(nb_joueurs):
        #i = 0
        texte += "## Joueur " + str(i) + "\n"
        for carte_type in CARTES_TYPES:
            for carte_nom in feuilles[i][carte_type]:
                texte += str(feuilles[i][carte_type][carte_nom]) + " : " + carte_nom + "\n"

            texte += "\n"
        texte += "\n"

    print(texte)

## Coeur
#ex ligne = [0, 1, 1, 0]
def calcule_score(ligne):
    return ligne.count(2)*nb_joueurs*(-2) + ligne.count(1)

def cherche_meilleur_score(cartes_par_type):
    carte_nom_max, score_max = '', -1
    for carte_nom, ligne in cartes_par_type.items():
        score = calcule_score(ligne)
        if score > score_max:
            carte_nom_max, score_max = carte_nom, score

    return carte_nom_max

# calcure le score de chaque ligne [0, 1, 1, 1]
# sélectionne le nom de la plus grosse ligne
def choisir_quel_suspicion(feuille):
    cartes_suspectees = {}
    for carte_type in CARTES_TYPES:
        #cartes_noms = CARTES[carte_type]
        #carte_nom = cartes_noms[randint(0, len(cartes_noms) - 1)]
        carte_nom = cherche_meilleur_score(feuille[carte_type])
        cartes_suspectees[carte_type] = carte_nom

    return cartes_suspectees


# ex : J1 montre à J2 qu'il a Pervenche
def ajoute_resultat_suspicion_quand_devoilement(feuilles, num_j_qui_suspecte, num_j_qui_montre, carte_type, carte_nom):
    for i in range(nb_joueurs):
        feuilles[num_j_qui_suspecte][carte_type][carte_nom][i] = 2 if i == num_j_qui_montre else 1


    # TODO ajouter si J3 sait que J2 n'a pas ni la Cuisine ni le Poignard, c'est qu'il a montré Pervenche

# ex : J1 a demandé Pervenche Poignard Cuisine et personne ne dévoile de cartes
def ajoute_resultat_suspicion_quand_non_devoilement(feuilles, num_j_qui_suspecte, cartes_suspectees):
    for num_joueur in range(nb_joueurs):
        for num_joueur_suspecte in range(nb_joueurs):
            #tout le monde sait que "TOUS sauf le joueur qui suspecte" n'ont pas les cartes suspectes
            if num_joueur_suspecte != num_j_qui_suspecte:
                for carte_type, carte_nom in cartes_suspectees.items():
                    feuilles[num_joueur][carte_type][carte_nom][num_joueur_suspecte] = 1



def suspicion(num_joueur, cartes_suspectees, cartes_joueurs, feuilles):
    if AFFICHE_TEXTE:
        print('Suspicion de J' + str(num_joueur) + ':', cartes_suspectees)

    for i in range(1, nb_joueurs):
        num_j_suspecte = (num_joueur + i)%nb_joueurs

        cartes_en_commun = {}
        for carte_type, carte_nom in cartes_suspectees.items():
            if (1 == cartes_joueurs[num_j_suspecte][carte_type].count(carte_nom)):
                cartes_en_commun[carte_type] = carte_nom

        if len(cartes_en_commun) > 0:
            if AFFICHE_TEXTE:
                print('--> J' + str(num_j_suspecte) + ' a', cartes_en_commun, '\n')
            carte_type = list(cartes_en_commun.keys())[0]
            carte_nom = cartes_en_commun[carte_type]
            ajoute_resultat_suspicion_quand_devoilement(feuilles, num_joueur, num_j_suspecte, carte_type, carte_nom)
            break

    if len(cartes_en_commun) == 0:
        ajoute_resultat_suspicion_quand_non_devoilement(feuilles, num_joueur, cartes_suspectees)
        if AFFICHE_TEXTE:
            print('--> PAS DE DEVOILEMENT\n')
        return True

    return False


## Jeu
def mise_en_place():
    # Distribution des cartes
    cartes = {carte_type: CARTES[carte_type].copy() for carte_type in CARTES_TYPES}
    cartes_tueur = choisi_tueur(cartes)
    cartes_joueurs = distribution(cartes)

    feuilles = initialise_feuilles(cartes_joueurs)

    # Affichage des cartes
    if AFFICHE_TEXTE:
        print('## Tueur', cartes_tueur, "\n")
        affiche_joueurs(cartes_joueurs)

    return cartes_tueur, cartes_joueurs, feuilles

def calcule_coupable_connu(feuille):
    coupable = {}
    for carte_type in CARTES_TYPES:
        for carte_nom, ligne in feuille[carte_type].items():
            if ligne == [1]*nb_joueurs:
                coupable[carte_type] = carte_nom

    return coupable

## Let's play !
def joue_une_partie():
    cartes_tueur, cartes_joueurs, feuilles = mise_en_place()

    if AFFICHE_TEXTE:
        print('-- Début du jeu --')

    i = 0
    stop = False
    while i < nb_joueurs*40 and not(stop):
        num_joueur = i%nb_joueurs
        # TODO Générer les cartes à suspecter
        feuille_joueur = feuilles[num_joueur]
        cartes_suspectees = choisir_quel_suspicion(feuille_joueur)
        suspicion(num_joueur, cartes_suspectees, cartes_joueurs, feuilles)
        coupable_connu = calcule_coupable_connu(feuille_joueur)
        stop = len(coupable_connu) == len(CARTES)

        i += 1

    if AFFICHE_TEXTE:
        affiche_feuilles(feuilles)
        print('Coupable connu au tour', i//nb_joueurs, 'par Joueur', num_joueur, coupable_connu)

    return i

def main():
    scores = []
    for k in range(nb_parties):
        i = joue_une_partie()
        scores.append(1 + i//nb_joueurs)

    pyplot.close()
    points, limits, rectangles = pyplot.hist(scores, density=True, bins=10)
    # print("% de chances de victoire au 9ème essai :",points[8])
    # print("% de chances de victoire au 12ème essai :",points[11])
    if AFFICHE_GRAPH:
        pyplot.show()

if AFFICHE_PROFILER:
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
