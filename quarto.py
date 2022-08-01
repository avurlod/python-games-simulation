from pydoc import plain
import random as rd
import numpy as np

# Source strat : https://teemoweb.blogspot.com/2012/09/decouvrir-le-jeu-quarto-et-les-astuces.html
# Simulateur de jeu : http://quarto.is-great.org/fr/choix-case.php?N=6&P=10&B0=9&B1=3&B2=-1&B3=12&B4=2&B5=0&B6=4&B7=-1&B8=7&B9=8&B10=6&B11=-1&B12=11&B13=15&B14=13&B15=-1
# Règle ++ : http://www.robinpinault.com/2014/01/31/quatro-quand-votre-adversaire-vous-offre-la-victoire/
# Image : http://1.bp.blogspot.com/-JFiQwzBBbs0/T9KHNY_R6rI/AAAAAAAAAnU/E4rTkqMAwxg/s1600/quarto.jpg

NIVEAU_ORDINATEUR = 4
NOMBRE_PARTIES = 1
FAUSSE_PARTIE = False

DEBUG = 1 == NOMBRE_PARTIES
AFFICHE_TENTATIVE = False
AFFICHE_ITERATIONS = DEBUG and True
AFFICHE_PIECES_RESTANTES = True
AFFICHE_PLATEAU = DEBUG
AFFICHE_VICTOIRE = DEBUG
AFFICHAGE_CASE_VIDE = '    '

## TODO ULTIME => génerer une compétition entre 10 niveaux 1, 10 niveaux 2 ... (64 participants) et voir le classement final ---> hypothèse : les plus gros niveaux devraient arriver premiers  
### Résultat
## Niveau 1
# Pourcentage de parties nulles (4/1000): 0.400000%
# Partie gagnée en moyenne au tour : 8.54
# min 4

## Niveau 2
# Pourcentage de parties nulles (3/1000): 0.300000%
# Partie gagnée en moyenne au tour : 8.5
# min 4

## Niveau 3
# Pourcentage de parties nulles (40/1000): 4.000000%
# Partie gagnée en moyenne au tour : 10.91
# min 7

## Niveau 4
# Pourcentage de parties nulles (150/1000): 15.000000%
# Partie gagnée en moyenne au tour : 10.4
# min 6

### Fonctions d'affichages 
def nom_joueur(numero_joueur):
    return 'Philomène' if 0 == numero_joueur else 'Noémie' 

def nom_carac(numero_carac):
    if 0 == numero_carac:
        return 'la taille'
    elif 1 == numero_carac:
        return 'la forme'
    elif 2 == numero_carac:
        return 'la couleur'
    elif 3 == numero_carac:
        return 'le remplissage'

def afficher_plateau(plateau):
    arr_plateau = np.where(np.array(plateau) == None, AFFICHAGE_CASE_VIDE, np.array(plateau))
    return '\n '.join(map(str, arr_plateau))


### Fonctions auxiliaires 
def mettre_en_place():
    cases, pieces, plateau = [], [], []

    for i in range(4):
        plateau.append([])
        for j in range(4):
            plateau[i].append(None)
            pieces.append(format(4*i+j,'b').zfill(4))
            cases.append((i,j))

    return cases, pieces, plateau

def generer_cases_pieces_restantes(plateau):
    cases = []
    pieces = [format(4*i+j,'b').zfill(4) for i in range(4) for j in range(4)]

    for i in range(4):
        for j in range(4):
            if None == plateau[i][j]:
                cases.append((i,j))
            else:
                pieces.remove(plateau[i][j])

    return cases, pieces

def jouer_une_piece(case, cases_restantes, piece, pieces_restantes, plateau):
    i, j = case
    plateau[i][j] = piece
    cases_restantes.remove(case)
    pieces_restantes.remove(piece)

def mettre_en_place_fausse_partie():
    plateau = [[None, '0110', None, '1011'], [None, None, None, '0100'], [None, None, '1110', '1111'], ['1100', None, '0101', '1001']] 
    plateau = [['0000', None, None, None], [None, '0001', None, None], [None, None, '0010', None], [None, None, None, None]] 
    cases, pieces = generer_cases_pieces_restantes(plateau)

    return cases, pieces, plateau


### Fonctions coeur
def pieces_coincides_en_carac(p1, p2, carac):
    return p1 is not None and p2 is not None and p1[carac] == p2[carac]

def est_un_quarto(case, piece, plateau):
    i_piece, j_piece = case

    ## ici on teste les 4 différentes caractéristiques (taille, forme, couleur, remplissage)
    for carac in range(4): 
        if all(j_piece == j or pieces_coincides_en_carac(piece, plateau[i_piece][j], carac) for j in range(4)):
            return True, carac, 'ligne', i_piece

        if all(i_piece == i or pieces_coincides_en_carac(piece, plateau[i][j_piece], carac) for i in range(4)):
            return True, carac, 'colonne', j_piece
        
        # TODO virer les fausses diag, mettre que les 2 bonnes
        if all(pieces_coincides_en_carac(piece, plateau[(i_piece+k+1)%4][(j_piece+k+1)%4], carac) for k in range(3)):
            return True, carac, 'diagonale', 1

        # TODO verif moyen carré
        # TODO verif carré tourné
        # TODO verif grand axe
        # TODO verif grand carré tourné
    return False, None, None, None


### Fonctions IA
def choisir_ou_jouer(cases, piece_a_jouer, pieces_restantes, plateau):
    ## Niveau 2 : si possibilité de gagner en un coup, jouer ce coup
    if 2 <= NIVEAU_ORDINATEUR:
        for case in cases:
            tentative = est_un_quarto(case, piece_a_jouer, plateau)
            if tentative[0]:
                return case, None

    ## Niveau 4 : choisir où jouer, de sorte que dans le choix de la pièce que je vais donner, je puisse en donner une qui ne fait pas gagner mon adversaire au prochain tour
    if 4 <= NIVEAU_ORDINATEUR:
        pieces_a_tester = pieces_restantes.copy()
        if piece_a_jouer in pieces_a_tester: pieces_a_tester.remove(piece_a_jouer)

        for case_a_jouer in cases:
            for piece_de_adversaire in pieces_a_tester:
                # on simule le plateau potentiel qu'aurait l'adversaire si on joue à la case
                cases_de_adversaire = cases.copy()
                cases_de_adversaire.remove(case_a_jouer)
                i, j = case_a_jouer
                plateau_de_adversaire = [ligne.copy() for ligne in plateau]
                plateau_de_adversaire[i][j] = piece_a_jouer

                if AFFICHE_TENTATIVE: print('TENTATIVE Jouer', piece_a_jouer, 'sur', case_a_jouer, 'et don de', piece_de_adversaire)
                if all(est_un_quarto(case, piece_de_adversaire, plateau_de_adversaire)[0] is False for case in cases_de_adversaire):
                    return case_a_jouer, piece_de_adversaire
        if AFFICHE_ITERATIONS: print('<!>  N\'importe quelle case jouée donne la victoire au prochain tour, peu importe la pièce donné')
        
    ## Niveau 1 : case aléatoire 
    return cases[rd.randint(0, len(cases)-1)], None

def choisir_piece_adversaire(cases, pieces, plateau):
    ## TODO Niveau 5 : choisir une piece qui permet la victoire dans un maximum de cas (le mieux étant peu importe où l'adversaire la place, et peu importe la pièce qu'il te donne)
    ## Niveau 3 : ne pas donner une pièce qui est gagnante à l'adversaire
    if 3 <= NIVEAU_ORDINATEUR:
        for piece in pieces:
            if all(est_un_quarto(case, piece, plateau)[0] is False for case in cases):
                return piece
        if AFFICHE_ITERATIONS: print('<!> N\'importe quel pièce donne la victoire au prochain tour')

    ## Niveau 1 : pièce aléatoire 
    return pieces[rd.randint(0, len(pieces)-1)]


### Fonctions de jeu
def jouer_une_partie():
    cases_restantes, pieces_restantes, plateau = mettre_en_place_fausse_partie() if FAUSSE_PARTIE else mettre_en_place()
    rd.shuffle(cases_restantes)
    rd.shuffle(pieces_restantes)

    victoire = False
    numero_tour = 1 + 16 - len(cases_restantes)
    numero_joueur = 0
    piece_prochain_tour = None
    if AFFICHE_ITERATIONS: print('\n')
    while not(victoire) and numero_tour <= 16:
        if AFFICHE_PIECES_RESTANTES: print('Pièces restantes :', pieces_restantes)
        piece = choisir_piece_adversaire(cases_restantes, pieces_restantes, plateau) if piece_prochain_tour is None else piece_prochain_tour

        if AFFICHE_ITERATIONS: print('\n## Tour', numero_tour)
        case, piece_prochain_tour = choisir_ou_jouer(cases_restantes, piece, pieces_restantes, plateau)
        jouer_une_piece(case, cases_restantes, piece, pieces_restantes, plateau)
        if AFFICHE_ITERATIONS: print('', afficher_plateau(plateau), '\n-->', nom_joueur(numero_joueur), 'joue :', piece ,'sur la case ', case)
        victoire, numero_point_commun, type_alignement, indice_alignement = est_un_quarto(case, piece, plateau)

        if not victoire:
            numero_joueur = 1 - numero_joueur
            numero_tour += 1

    if AFFICHE_PLATEAU and not AFFICHE_ITERATIONS: print('\nEtat du plateau à la fin :\n', afficher_plateau(plateau), '\n')
    if victoire:
        if AFFICHE_VICTOIRE: print('\n=> Victoire de', nom_joueur(numero_joueur), 'au bout de', numero_tour, 'tours sur la', str(indice_alignement+1) + 'e', type_alignement, 'avec comme point commun', nom_carac(numero_point_commun), '(n°' + str(numero_point_commun+1) + ')\n')

        return numero_tour
    
    if AFFICHE_VICTOIRE: print('Match nul.')
    return None

def main():
    if 1 >= NOMBRE_PARTIES:
        jouer_une_partie()
    else:
        numeros_tour_victoire, nb_parties_nulles = [], 0
        for numero_partie in range(NOMBRE_PARTIES):
            numero_tour = jouer_une_partie()
            if numero_tour is None:
                nb_parties_nulles += 1
            else:
                numeros_tour_victoire.append(numero_tour)

        if FAUSSE_PARTIE: print('numeros_tour_victoire', numeros_tour_victoire)
        print('Pourcentage de parties nulles (' + str(nb_parties_nulles) + '/' + str(NOMBRE_PARTIES) + '):', format(nb_parties_nulles/NOMBRE_PARTIES, '%'))
        print('Partie gagnée en moyenne au tour :', round(sum(numeros_tour_victoire)/len(numeros_tour_victoire),2))
        print('Numéro du tour de victoire minimale:', min(numeros_tour_victoire))

main()
