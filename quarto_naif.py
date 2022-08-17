import random as rd
import numpy as np

# Source strat : https://teemoweb.blogspot.com/2012/09/decouvrir-le-jeu-quarto-et-les-astuces.html
# Simulateur de jeu : http://quarto.is-great.org/fr/choix-case.php?N=6&P=10&B0=9&B1=3&B2=-1&B3=12&B4=2&B5=0&B6=4&B7=-1&B8=7&B9=8&B10=6&B11=-1&B12=11&B13=15&B14=13&B15=-1
# Règle ++ : http://www.robinpinault.com/2014/01/31/quatro-quand-votre-adversaire-vous-offre-la-victoire/
# Image : http://1.bp.blogspot.com/-JFiQwzBBbs0/T9KHNY_R6rI/AAAAAAAAAnU/E4rTkqMAwxg/s1600/quarto.jpg

#TODO compter le nombre de calculs fait dans la tête (de tentative imaginée dans la tête) ((pour se rendre compte de la difficulté de faire le calcul))
NOMBRE_NIVEAUX = 5
NOMBRE_PARTIES = 1

NIVEAU_ORDINATEUR = 4
FAUSSE_PARTIE = False

AFFICHER_PROFILER = False
DEBUG = 1 == NOMBRE_PARTIES
AFFICHE_TENTATIVE = False
AFFICHE_ITERATIONS = DEBUG and True
AFFICHE_PIECES_RESTANTES = DEBUG and False
AFFICHE_PLATEAU = DEBUG
AFFICHE_VICTOIRE = DEBUG
AFFICHAGE_CASE_VIDE = '    '


### Résultat
## Niveau 0
# Pourcentage de parties nulles (4/1000): 0.400000%
# Partie gagnée en moyenne au tour : 8.54
# min 4

## Niveau 1
# Pourcentage de parties nulles (3/1000): 0.300000%
# Partie gagnée en moyenne au tour : 8.5
# min 4

## Niveau 2
# Pourcentage de parties nulles (40/1000): 4.000000%
# Partie gagnée en moyenne au tour : 10.91
# min 7

## Niveau 3
# Pourcentage de parties nulles (150/1000): 15.000000%
# Partie gagnée en moyenne au tour : 10.4
# min 6

### Tournois
## Se lit "Quand le niveau 3 jour contre un Niveau 2 et commence, son Net Victory Score (NVS) est de 72"
## NVS = (#victoires - #defaites)/#parties

## Resultats ligne/colonne/diag nb = 50
# Résultat pour 0 : [  -6.  -64. -100. -100.]
# Résultat pour 1 : [  80.    0.  -84. -100.]
# Résultat pour 2 : [100.  84.   4. -84.]
# Résultat pour 3 : [100. 100.  72.  32.]

## Resultats ligne/colonne/diag/carre_moyen nb = 500
# Résultat pour 0 : [  -6.  -80.  -96. -100.]
# Résultat pour 1 : [ 79.   6. -83. -99.]
# Résultat pour 2 : [ 99.  82.  -3. -75.]
# Résultat pour 3 : [98. 99. 77. -5.]

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

def mettre_en_place_fausse_partie(): #grand, rond, blanc, pointé
    plateau_partie_random = [[None, '0110', None, '1011'], [None, '0000', None, '0100'], [None, None, '1110', '1111'], ['1100', None, '0101', '1001']] 
    plateau_diag = [['0000', None, None, None], [None, '0001', None, None], [None, None, '0010', None], [None, None, None, None]] 
    plateau_diag_inversee = [[None, None, None, '0010'], [None, None, None, None], [None, '0001', None, None],['0000', None, None, None]]
    plateau_moyen_carre_bas_gauche = [['0000', '0101', None, None], [None, '0001', None, None], [None, None, None, None], [None, None, None, None]] 
    plateau_moyen_carre_bas_droite = [['0000', '0101', None, None], ['0001', None, None, None], [None, None, None, None], [None, None, None, None]] 
    plateau_moyen_carre_tourne = [[None, None, None, None], [None, None, '0101', None], [None, '0001', None, '0000'], [None, None, None, None]] 
    plateau_piege_en_2 = [[None, '0110', None, '1111'], ['1100', '1110', '0100', None], [None, '0011', None, None], [None, None, None, '1001']] 

    plateau = plateau_piege_en_2
    cases, pieces = generer_cases_pieces_restantes(plateau)

    return cases, pieces, plateau


### Fonctions coeur
def pieces_coincides_en_carac(p1, p2, carac):
    return p2 is not None and p1[carac] == p2[carac]

def est_un_quarto_ligne_colonne(carac, i_piece, j_piece, piece, plateau):
    if all(j_piece == j or pieces_coincides_en_carac(piece, plateau[i_piece][j], carac) for j in range(4)):
        return carac

    if all(i_piece == i or pieces_coincides_en_carac(piece, plateau[i][j_piece], carac) for i in range(4)):
        return carac

def est_un_quarto_diagonale(carac, i_piece, j_piece, piece, plateau):
    if i_piece == j_piece:
        if all(pieces_coincides_en_carac(piece, plateau[(i_piece+k+1)%4][(j_piece+k+1)%4], carac) for k in range(3)):
            return carac
    if i_piece + j_piece == 3:
        if all(pieces_coincides_en_carac(piece, plateau[(i_piece-(k+1))%4][(j_piece+k+1)%4], carac) for k in range(3)):
            return carac

def est_un_quarto_moyen_carre(carac, i_piece, j_piece, piece, plateau):
    if i_piece < 3 and j_piece < 3:
        if all(pieces_coincides_en_carac(piece, plateau[i_piece+k%2][j_piece+k//2], carac) for k in range(1,4)):
            return carac #haut-gauche
    if i_piece < 3 and j_piece > 0:
        if all(pieces_coincides_en_carac(piece, plateau[i_piece+k%2][j_piece-k//2], carac) for k in range(1,4)):
            return carac #haut-droite
    if i_piece > 0 and j_piece < 3:
        if all(pieces_coincides_en_carac(piece, plateau[i_piece-k%2][j_piece+k//2], carac) for k in range(1,4)):
            return carac #bas-gauche
    if i_piece > 0 and j_piece > 0:
        if all(pieces_coincides_en_carac(piece, plateau[i_piece-k%2][j_piece-k//2], carac) for k in range(1,4)):
            return carac #bas-droite

# Moins efficace ..
# combinaisons_moyens_carres = [[(0, 0), (1, 0), (0, 1), (1, 1)], [(0, 1), (1, 1), (0, 2), (1, 2)], [(0, 2), (1, 2), (0, 3), (1, 3)], [(1, 0), (2, 0), (1, 1), (2, 1)], [(1, 1), (2, 1), (1, 2), (2, 2)], [(1, 2), (2, 2), (1, 3), (2, 3)], [(2, 0), (3, 0), (2, 1), (3, 1)], [(2, 1), (3, 1), (2, 2), (3, 2)], [(2, 2), (3, 2), (2, 3), (3, 3)]]
# def est_un_quarto_moyen_carre_2(carac, i_piece, j_piece, piece, plateau):
#     return est_un_quarto_parmis_combinaisons(carac, combinaisons_moyens_carres, i_piece, j_piece, 'moyen carré', piece, plateau)

def est_un_quarto_parmis_combinaisons(carac, combinaisons, i_piece, j_piece, piece, plateau):
    for combinaison in combinaisons:
        if (i_piece, j_piece) in combinaison:
            if all(i_piece==i and j_piece==j or pieces_coincides_en_carac(piece, plateau[i][j], carac) for i,j in combinaison):
                return carac

combinaisons_carres_tournes = [[(0,1), (1,0), (1,2), (2,1)], [(0, 2), (1, 1), (1, 3), (2, 2)], [(1, 2), (2, 1), (2, 3), (3, 2)], [(1, 1), (2, 0), (2, 2), (3, 1)]]
def est_un_quarto_carre_tourne(carac, i_piece, j_piece, piece, plateau):
    return est_un_quarto_parmis_combinaisons(carac, combinaisons_carres_tournes, i_piece, j_piece, piece, plateau)

combinaisons_grands_carres = [[(0, 0), (2, 0), (0, 2), (2, 2)], [(0, 1), (2, 1), (0, 3), (2, 3)], [(1, 0), (3, 0), (1, 2), (3, 2)], [(1, 1), (3, 1), (1, 3), (3, 3)]]
def est_un_quarto_grand_carre(carac, i_piece, j_piece, piece, plateau):
    return est_un_quarto_parmis_combinaisons(carac, combinaisons_grands_carres, i_piece, j_piece, piece, plateau)

def est_un_quarto(case, piece, plateau):
    i_piece, j_piece = case

    ## ici on teste les 4 différentes caractéristiques (taille, forme, couleur, remplissage)
    for carac in range(4): 
        res = est_un_quarto_ligne_colonne(carac, i_piece, j_piece, piece, plateau)
        if res is not None:
            return res

        # res = est_un_quarto_diagonale(carac, i_piece, j_piece, piece, plateau)
        # if res is not None:
        #     return res

        # res = est_un_quarto_moyen_carre(carac, i_piece, j_piece, piece, plateau)
        # if res is not None:
        #     return res

        # res = est_un_quarto_carre_tourne(carac, i_piece, j_piece, piece, plateau)
        # if res is not None:
        #     return res

        # res = est_un_quarto_grand_carre(carac, i_piece, j_piece, piece, plateau)
        # if res is not None:
        #     return res

        # TODO verif grand carré tourné
    return None

def expliquer_victoire(case, carac, piece, plateau):
    i_piece, j_piece = case

    if all(j_piece == j or pieces_coincides_en_carac(piece, plateau[i_piece][j], carac) for j in range(4)):
        return str(i_piece+1) + 'e ligne'

    if all(i_piece == i or pieces_coincides_en_carac(piece, plateau[i][j_piece], carac) for i in range(4)):
        return str(j_piece+1) + 'e colonne'

    if i_piece == j_piece:
        if all(pieces_coincides_en_carac(piece, plateau[(i_piece+k+1)%4][(j_piece+k+1)%4], carac) for k in range(3)):
            return 'diagonale'
    if i_piece + j_piece == 3:
        if all(pieces_coincides_en_carac(piece, plateau[(i_piece-(k+1))%4][(j_piece+k+1)%4], carac) for k in range(3)):
            return 'diagonale inversee'

    if i_piece < 3 and j_piece < 3:
        if all(pieces_coincides_en_carac(piece, plateau[i_piece+k%2][j_piece+k//2], carac) for k in range(1,4)):
            return f"moyen carré {str(i_piece)},{str(j_piece)} x {str(i_piece+1)},{str(j_piece+1)}" #haut-gauche
    if i_piece < 3 and j_piece > 0:
        if all(pieces_coincides_en_carac(piece, plateau[i_piece+k%2][j_piece-k//2], carac) for k in range(1,4)):
            return f"moyen carré {str(i_piece)},{str(j_piece-1)} x {str(i_piece+1)},{str(j_piece)}" #haut-droite
    if i_piece > 0 and j_piece < 3:
        if all(pieces_coincides_en_carac(piece, plateau[i_piece-k%2][j_piece+k//2], carac) for k in range(1,4)):
            return f"moyen carré {str(i_piece-1)},{str(j_piece)} x {str(i_piece)},{str(j_piece+1)}" #bas-gauche
    if i_piece > 0 and j_piece > 0:
        if all(pieces_coincides_en_carac(piece, plateau[i_piece-k%2][j_piece-k//2], carac) for k in range(1,4)):
            return f"moyen carré {str(i_piece-1)},{str(j_piece-1)} x {str(i_piece)},{str(j_piece)}" #bas-droite
    
    if est_un_quarto_carre_tourne(carac, i_piece, j_piece, piece, plateau):
        return 'carré tourné'

    if est_un_quarto_grand_carre(carac, i_piece, j_piece, piece, plateau):
        return 'grand carré'

    return 'PAS DE VICTOIRE FINALEMENT'

def generer_simulation_cases_plateau(case_a_jouer, cases, piece_a_jouer, plateau):
    # on simule le plateau potentiel qu'aurait l'adversaire si on joue à la case
    cases_de_adversaire = cases.copy()
    cases_de_adversaire.remove(case_a_jouer)
    i, j = case_a_jouer
    plateau_de_adversaire = [ligne.copy() for ligne in plateau]
    plateau_de_adversaire[i][j] = piece_a_jouer

    return cases_de_adversaire, plateau_de_adversaire

### Fonctions IA
def choisir_ou_jouer(cases, niveau_joueur, piece_a_jouer, pieces, plateau):
    if len(pieces) <= 14:
        ## Niveau 1 : choisir une case qui me fait gagner MAINTENANT
        if 1 <= niveau_joueur:
            res = choisir_ou_jouer_niveau_1(cases, piece_a_jouer, pieces, plateau)
            if res is not None:
                return res

        if 4 <= niveau_joueur and len(pieces) <= 7:
            ## Niveau 4 : choisir une case & piece qui me fait gagner peu importe la case & piece de l'adversaire
            res = choisir_ou_jouer_niveau_4(cases, piece_a_jouer, pieces, plateau)
            if res is not None:
                return res

        ## Niveau 3 : choisir une case & piece qui NE FAIT PAS gagner l'adversaire (avec un choix de case judicieux)
        if 3 == niveau_joueur:
            res = choisir_ou_jouer_niveau_3(cases, piece_a_jouer, pieces, plateau)
            if res is not None:
                return res

    piece_adversaire = choisir_piece_adversaire(cases, niveau_joueur, pieces, plateau)
    ## Niveau 0 : case aléatoire 
    case = cases[rd.randint(0, len(cases)-1)]

    return case, piece_adversaire

def choisir_ou_jouer_niveau_1(cases, piece_a_jouer, pieces_restantes, plateau):
    if len(pieces_restantes) <= 13:
        for case in cases:
            tentative = est_un_quarto(case, piece_a_jouer, plateau)
            if tentative is not None:
                return case, None

def choisir_ou_jouer_niveau_3(cases, piece_a_jouer, pieces_restantes, plateau):
    for case_a_jouer in cases:
        for piece_de_adversaire in pieces_restantes:
            cases_de_adversaire, plateau_de_adversaire = generer_simulation_cases_plateau(case_a_jouer, cases, piece_a_jouer, plateau)
            if AFFICHE_TENTATIVE: print('TENTATIVE Jouer', piece_a_jouer, 'sur', case_a_jouer, 'et don de', piece_de_adversaire)
            if all(est_un_quarto(case, piece_de_adversaire, plateau_de_adversaire) is None for case in cases_de_adversaire):
                return case_a_jouer, piece_de_adversaire
    if AFFICHE_ITERATIONS: print('<!>  N\'importe quelle case jouée donne la victoire au prochain tour, peu importe la pièce donné')
        
def choisir_ou_jouer_niveau_4(cases, piece_a_jouer, pieces_restantes, plateau):
    for case_a_jouer in cases:
        # print('Supposons que j\'ai joué sur', case_a_jouer)
        for piece_de_adversaire in pieces_restantes:
            # print('Testons si je donne', piece_de_adversaire)
            cases_de_adversaire, plateau_de_adversaire = generer_simulation_cases_plateau(case_a_jouer, cases, piece_a_jouer, plateau)
            
            # L'objectif est que, dans aucun cas de case et de pièce par l'adversaire, je n'ai pas de possibilité de gagner
            non_victoire_dans_2_possible = False
            for case_jouee_par_adversaire in cases_de_adversaire:
                # print('Supposons que mon adversaire joue sur', case_jouee_par_adversaire)
                if est_un_quarto(case_jouee_par_adversaire, piece_de_adversaire, plateau_de_adversaire) is not None:
                    non_victoire_dans_2_possible = True
                    if DEBUG: print('Si je joue', case_a_jouer, 'et que je donne', piece_de_adversaire, ' -> il pourra jouer', case_jouee_par_adversaire, '=> DEFAITE pour moi')

                    break

                # Dès qu'une case joué par l'adversaire ou une pièce donné m'empêche de finir, je passe à la suivante 
                pieces_restantes_dans_2 = pieces_restantes.copy()
                pieces_restantes_dans_2.remove(piece_de_adversaire)
                for piece_que_je_jouerai in pieces_restantes_dans_2:
                    # print('Voyons si, après ce choix de case et de pièce par l\'adversaire j\'arrive à gagner')
                    cases_restantes_dans_2, plateau_dans_2 = generer_simulation_cases_plateau(case_jouee_par_adversaire, cases_de_adversaire, piece_de_adversaire, plateau_de_adversaire)
                    # print('Le plateau ressemblerait à:\n', afficher_plateau(plateau_dans_2),'\n\n')
                    if all(est_un_quarto(case, piece_que_je_jouerai, plateau_dans_2) is None for case in cases_restantes_dans_2):
                        if DEBUG: print('Si je joue', case_a_jouer, 'et que je donne', piece_de_adversaire, ' -> il pourra jouer', case_jouee_par_adversaire, 'et me donner', piece_que_je_jouerai, '=> et je gagnerai pas')
                        non_victoire_dans_2_possible = True
                        break
                        # dans cas, mon adversaire peut me donner une pièce qui m'empechera de gagner
                        # donc je peux abandonner cette hypothèse 
                    # print('Si on me donne', piece_que_je_jouerai, 'je peux gagner avec')
                if non_victoire_dans_2_possible:
                    break
                    # pour l'hyp de case_jouee_par_adversaire, toutes les pièces sont gagnantes

            if non_victoire_dans_2_possible is False:
                if DEBUG: print('Si je joue', case_a_jouer, 'et que je donne', piece_de_adversaire, ' ==> je gagnerai peu importe la case jouée et la pièce donnée par l\'adversaire !!')

                return case_a_jouer, piece_de_adversaire

def choisir_piece_adversaire(cases, niveau_joueur, pieces, plateau):
    # TODO trouver pk il donne des pieces qui la victoire
    ## Niveau 2 : ne pas donner une pièce qui est gagnante à l'adversaire
    if 2 <= niveau_joueur and len(pieces) <= 14:
        for piece in pieces:
            if all(est_un_quarto(case, piece, plateau) is None for case in cases):
                return piece
        if AFFICHE_ITERATIONS: print('<!> N\'importe quel pièce donne la victoire au prochain tour')

    ## Niveau 0 : pièce aléatoire 
    return pieces[rd.randint(0, len(pieces)-1)]


### Fonctions de jeu
def jouer_une_partie(niveaux_joueurs = [NIVEAU_ORDINATEUR, NIVEAU_ORDINATEUR]):
    cases_restantes, pieces_restantes, plateau = mettre_en_place_fausse_partie() if FAUSSE_PARTIE else mettre_en_place()
    rd.shuffle(cases_restantes)
    rd.shuffle(pieces_restantes)

    victoire = False
    numero_tour = 1 + 16 - len(cases_restantes)
    numero_joueur = 0
    # celui qui commence à jouer c'est celui qui place la pièce
    piece_prochain_tour = choisir_piece_adversaire(cases_restantes, niveaux_joueurs[1], pieces_restantes, plateau)
    if FAUSSE_PARTIE and AFFICHE_ITERATIONS: print('Tableau initial\n', afficher_plateau(plateau))
    if AFFICHE_ITERATIONS: print(f"{nom_joueur(0)} (niveau {niveaux_joueurs[0]}) affronte {nom_joueur(1)} (niveau {niveaux_joueurs[1]})")
    if AFFICHE_ITERATIONS: print('-->', nom_joueur(1), 'donne', piece_prochain_tour)


    while not(victoire) and numero_tour <= 16:
        if AFFICHE_PIECES_RESTANTES: print('Pièces restantes :', pieces_restantes)
        if AFFICHE_ITERATIONS: print('\n## Tour', numero_tour)

        piece = piece_prochain_tour
        pieces_restantes.remove(piece)

        niveau_joueur = niveaux_joueurs[numero_joueur%2]
        case, piece_prochain_tour = choisir_ou_jouer(cases_restantes, niveau_joueur, piece, pieces_restantes, plateau)
        jouer_une_piece(case, cases_restantes, piece, pieces_restantes, plateau)

        if AFFICHE_ITERATIONS: print('-->', nom_joueur(numero_joueur), 'joue :', piece ,'sur la case ', case, 'et donne', piece_prochain_tour)
        if AFFICHE_ITERATIONS and AFFICHE_PLATEAU: print('', afficher_plateau(plateau))
        
        resultat = est_un_quarto(case, piece, plateau) 
        victoire = resultat is not None
        if not victoire:
            numero_joueur = 1 - numero_joueur
            numero_tour += 1
        else:
            numero_point_commun = resultat
            type_alignement = expliquer_victoire(case, numero_point_commun, piece, plateau)

    if AFFICHE_PLATEAU and not AFFICHE_ITERATIONS: print('\nEtat du plateau à la fin :\n', afficher_plateau(plateau), '\n')
    if victoire:
        if AFFICHE_VICTOIRE:
            print('\n=> Victoire de', nom_joueur(numero_joueur), 'au bout de', numero_tour, 'tours grâce à', nom_carac(numero_point_commun), '#' + str(numero_point_commun+1), 'sur', type_alignement + '\n')

        return numero_tour, numero_joueur
    
    if AFFICHE_VICTOIRE: print('Match nul.')
    return None, None

def algo_pour_creer_super_adversaire():
    if 1 >= NOMBRE_PARTIES:
        jouer_une_partie()
    else:
        numeros_tour_victoire, nb_parties_nulles = [], 0
        for numero_partie in range(NOMBRE_PARTIES):
            numero_tour, numero_joueur = jouer_une_partie()
            if numero_tour is None:
                nb_parties_nulles += 1
            else:
                numeros_tour_victoire.append(numero_tour)

        if FAUSSE_PARTIE: print('numeros_tour_victoire', numeros_tour_victoire)
        print('Pourcentage de parties nulles (' + str(nb_parties_nulles) + '/' + str(NOMBRE_PARTIES) + '):', format(nb_parties_nulles/NOMBRE_PARTIES, '%'))
        if [] != numeros_tour_victoire:
            print('Partie gagnée en moyenne au tour :', round(sum(numeros_tour_victoire)/len(numeros_tour_victoire),2))
            print('Numéro du tour de victoire minimale:', min(numeros_tour_victoire))

def algo_tournoi_pour_tester_les_niveaux():
    matchs = [[i, j] for i in range(NOMBRE_NIVEAUX) for j in range(NOMBRE_NIVEAUX)]
    zeroList = [0 for e in range(NOMBRE_NIVEAUX)]
    ## TODO Conclure
    points = [list(zeroList) for e in range(NOMBRE_NIVEAUX)]
    for match in matchs:
        j1, j2 = match
        for k in range(NOMBRE_PARTIES):
            numero_tour, numero_joueur = jouer_une_partie(match)
            if numero_joueur is not None:
                victoire_j1 = 0 == numero_joueur
                if victoire_j1:
                    points[j1][j2] += 1    
                else:
                    points[j1][j2] -= 1
    points = np.round(np.array(points)/NOMBRE_PARTIES*100,0)

    for niveau, ligne in enumerate(points):
        print('Résultat pour', niveau, ':', ligne)

def main():
    jouer_une_partie()
    # algo_pour_creer_super_adversaire()
    # algo_tournoi_pour_tester_les_niveaux()


if AFFICHER_PROFILER:
    if __name__ == '__main__':
        import cProfile, pstats
        profiler = cProfile.Profile()
        profiler.enable()
        main()
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime') #tottime
        stats.print_stats(15)
else:
    main()
