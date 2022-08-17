class ArbreBinaire:
    def __init__(self, etiquette = None, sag = None, sad = None):
        self.etiquette = etiquette
        self.sag = sag
        self.sad = sad
    
    def est_vide(self):
        if self.etiquette is None:
               return True
        else:
               return False 

# Définition de l'arbre :
#       1
#     /    \
#    2      3
#   / \    / \
#  4   5  6   7
#     / \
#    8   9

a = ArbreBinaire()
a.etiquette = 1
a.sag = ArbreBinaire(2)
a.sad = ArbreBinaire(3)
a.sag.sag = ArbreBinaire(4, ArbreBinaire(), ArbreBinaire())
a.sag.sad = ArbreBinaire(5)
a.sad.sag = ArbreBinaire(6, ArbreBinaire(), ArbreBinaire())
a.sad.sad = ArbreBinaire(7, ArbreBinaire(), ArbreBinaire())
a.sag.sad.sag = ArbreBinaire(8, ArbreBinaire(), ArbreBinaire())
a.sag.sad.sad = ArbreBinaire(9, ArbreBinaire(), ArbreBinaire())

 

def parcours_largeur(arbre):
    file = []
    file.append(arbre)
    parcours = []
    while len(file) > 0:
        parcours.append(file[0].etiquette)
        sous_arbre = file.pop(0)
        if not sous_arbre.sag.est_vide():
            file.append(sous_arbre.sag)
        if not sous_arbre.sad.est_vide():
            file.append(sous_arbre.sad)
    return parcours


print("parcours largeur :")
print(parcours_largeur(a))
