# ===============================
#            Modules
# ===============================

from math import *

# ================================
#            Classes
# ================================

# --------------------------------
class Cellule :
    def __init__(self, coordonnees , Type, etat_couverture = False):
        self.coord = coordonnees # Entiers
        self.type = Type # Mur, cible, vide (#, ., -)
        self.etat_wifi = etat_couverture # True ou false
# --------------------------------

# --------------------------------
class Routeur :
    def __init__(self, cellule, liste_cellules_couvertes ):
        self.cellule = cellule
        self.rayon = rayon
        self.liste_cellules_couvertes = liste_cellules_couvertes  # Liste des cellules couvertes par le wifi

    def ajout_cellules_dansListeCouverture(cellule):
        self.liste_cellules_couvertes.append(cellule) # Ajoute une cellule à la liste
# --------------------------------

# ================================
#       Fichier => Données
# ================================

# Récupère fichier et le transforme en données et liste de cellules
# --------------------------------
def recuperer_fichier(chemin_fichier):
    fichier = []
    fichier_str = ''
    liste_map = []
    donnees = []

    # Transformation fichier en string pour le schéma et en tableau pour les données
    with open(chemin_fichier,"r") as source:
        for line in source:
            element = line.strip()
            fichier.append(element)
            
    # Séparation des données
    for i in range(3):
        donnees.extend(fichier[0].split())
        del fichier[0]

    # Création sting
    for tab in fichier:
        fichier_str = fichier_str + tab
    
    # On parcourt chaque element(=ligne) du tableau et chaque caractère de ces élèments
    # puis on crée une Cellule pour chacun de ces caractères
    x = 1
    y = 1
    for car in fichier_str:
        element = Cellule([int(x),int(y)],car)
        liste_map.append(element)
        
        if(x == int(donnees[0])):
            x = 1
            if(y != donnees[1]):
                y = y + 1
        else:
            x = x + 1
      
    return liste_map,donnees # Retourne liste avec les cellulles et les données de la map
# --------------------------------

# ================================
#      Fonction auxiliaires
# ================================

# Calcule distance entre 2 points
# --------------------------------
def dist(coord1,coord2):
    s = 0 
    for i in range (0,len(coord1)):
        s+=(coord1[i]-coord2[i])**2
        # Ajout des (xi-yi)²
    return (sqrt(s))
# --------------------------------

# Retourne le minimum (mini(liste)[0]) et l'indice de la valeur minimum (mini(liste)[1]) PAS OPTIMISE MAIS OSEF SAMER
# --------------------------------
def mini(liste):
    min = liste[0]
    for i in range(0,len(liste)):
        if liste[i] < min :
            min = liste[i]
    for i in range (0,len(liste)):
        if liste[i] == min: 
            j = i
    return(min,j)
# --------------------------------

# Retourne la liste des coordonnées des cases voisines d'une CASE entrée
# --------------------------------
def voisins(case):
    x = case[0]
    y = case[1]
    return([[x,y+1],[x,y-1],[x-1,y],[x-1,y+1],[x-1,y-1],[x+1,y+1],[x+1,y],[x+1,y-1]])
# On doit relier une case routeur [a,b] à une case centrale [x,y]
# --------------------------------

# Retourne la case du tableau avec la bonne cellule
# --------------------------------
def return_cellule(coord):
    nb_tab = (int(coord[1]) - 1) * ligne + (int(coord[0]) - 1)
    return liste_map[nb_tab]
# --------------------------------

# Retourne la liste des cellules couvertes si la case en paramètre était un routeur
# --------------------------------
def liste_couvertes(cellrouteur):
    liste = []
    coord = cellrouteur.coord
    # Coord contient juste les coordonnées de cellrouteur, la case dont nous allons retourner
    # la liste des cases qui seraient couvertes si cette case était routeur
    for a in liste_map :
        if dist(coord,a.coord) < rayon and elimination(coord,a.coord) == False and a.couv == False :
            liste.append(a)
    return liste
# --------------------------------

# Choisit le candidat routeur qui couvre le plus de nouvelles cases
# --------------------------------
def plusfort(listecandidats):
    c = 0
    for candidat in listecandidats :
        if len(liste_couvertes(candidat)) > c :
            gagnant = candidat
            c = len(liste_couvertes(candidat))
    return(gagnant,liste_couvertes(gagnant))
# --------------------------------

# ================================
#          Vérifications
#        placement routeur
# ================================

# Permet de vérifier si une cellule est un mur ou non
# --------------------------------
def verif_MurCellule(cellule): 
    if(cellule.type == '#'):
        return True
    else :
        return False
# --------------------------------

# Permet de savoir si une cellule est prise par un routeur ou non
# --------------------------------
def verif_Cellule_libre(cellule): 
    for i in range (len(liste_routeur)):
        if(liste_routeur[i].cellule == cellule): # Si la cellule est dans la liste des routeurs alors non libre
            return False # Prise par routeur
        else :
            return True # Libre
# --------------------------------

# Elimine couverture d'une case s'il y a un mur entre celle-ci et le routeur
# --------------------------------
def elimination(coordonnees, routeur):
    res = False
    cellule = return_cellule(coordonnees)
    x = abs(coordonnees[0] - routeur.cellule.coord[0]) +1 # Largeur rectangle
    y = abs(coordonnees[1] - routeur.cellule.coord[1]) +1 # Hauteur rectangle
    for i in range (x) :
        for j in range (y) :
            cellule_a_verifier = return_cellule([coordonnees[0]-i,coordonnees[1]-j])
            if cellule_a_verifier != None : # On vérifie qu'il y a bien une cellule
                if (verif_MurCellule(cellule_a_verifier)== True) : # Présence d'un mur
                    res = True 
    return res # Si ça élimine alors True sinon False car on la garde
# --------------------------------

# ================================
#        Placer Routeur
# ================================

# --------------------------------
def Placer_routeur():
    for case in liste_map :
        # On parcourt la carte jusqu'à une case non couverte
        if (case.etat_wifi == False) :
            # On crée une liste vide qui accueillera la liste des candidats à devenir routeurs
            listcandidrout = []
            
            for cellule in liste_map :
                if dist(cellule.coord,case.coord) < rayon and verif_MurCellule(cellule) == False :
                    listcandidrout.append(cellule)
            (coord,l)=(plusfort(listcandidrout))
            # Coord est la paire de coordonnées du routeur choisi, celui qui couvre le plus de nouvelles cases,
            # l est la liste des cases nouvellement couvertes
            
            if budget - prix_routeur > 0 :
                # Si ça rentre dans le budget
                budget -= prix_routeur
                r1 = Routeur(return_cellule(coord),l) # On crée le routeur r1
                liste_routeur.append(r1)
                for case in r1.liste_cellules_couvertes :
                    case.etat_wifi = True
                backbone = Relier(cord,backbone)[0]           
                # ON FAIT LA SUPPOSITION QUE LE PRIX POUR RELIER UN ROUTEUR AU BACKBONE
                # NE SERA PAS DETERMINANT POUR FRANCHIR LA BARRE DU BUDGET : optimisable
                budget -= Relier(coord,backbone)[1] * prix_backbone # Budget s'autodécrémente
# --------------------------------

# ================================
#    Relier Routeur-Backbone
# ================================

# --------------------------------
def Relier(routeur,backbone):
    # Prend en compte seulement les coordonnées du routeur et la liste des coordonnées des cases par lesquels passent le backbone 
    listdist = [] # Liste des distances des points du backbone au routeur
    for a in backbone :
        listdist.append(dist(a,routeur)) # Remplie avec les distances des points du backbone au routeur dans le MÊME ordre
    if mini(listdist)[0] < 1.4 : 
        print("le routeur est déjà relié à la backbone")
    else :
        nb = 1 # Compteur du nombre de cases rajoutées au backbone (commence à 1 pour compter la case routeur)
        while mini(listdist)[0] > 1.4:
            nb += 1
            extremite = backbone[mini(listdist)[1]] # L'extremité est la case du backbone la plus proche du routeur
            candidats = voisins(extremite)
            distcand = []
            for a in candidats :
                distcand.append(dist(routeur,a))
            backbone.append(candidats[mini(distcand)[1]]) # On rajoute la nouvelle case à backbone
            listdist.append(mini(distcand)[0])
        backbone.append(routeur) # On finit enfin par cabler le routeur
    return(backbone,nb)
# --------------------------------

# --------------------------------     
def proposer_cellules_nonMur(routeur):
    liste_coordVoisins = voisins(routeur.cellule.coord) # Il récupère toutes les coord des voisins
    liste_voisines = [] # Liste des cellules voisines à remplir
    for i in range (len(liste_coordVoisins)): # Parcourt les coordonnées des voisins du routeur
        if recherche_celluleNonMur_avecCoordonnees(liste_coordVoisins[i]): 
            liste_voisines.append(recherche_celluleNonMur_avecCoordonnees(liste_coordVoisins[i]))
            # Ajoute la cellule aux voisines possibles si elle existe et n'est pas un mur

    return liste_voisines # Retourne la liste des voisines dispo
# --------------------------------

# Permet de retrouver une cellule grâce aux coordonees et vérifie si ce n'est pas un mur
# Retourne la cellule recherché
# --------------------------------    
def recherche_celluleNonMur_avecCoordonnees(coordonnees):
    i = 0                      
    cellule_parcourue = liste_map[0]
    while( (cellule_parcourue.coord != coordonnees) and (i < len(liste_map))): #parcours toute la carte
        cellule_parcourue = liste_map[i]
        if(cellule_parcourue.coord == coordonnees): #si la cellule a les bonnes coordonnées
            if (verif_MurCellule(cellule_parcourue ) == False) and (verif_Cellule_libre(cellule_parcourue) == True): # Si la cellule n'est pas de type mur
               return cellule_parcourue # On retourne la cellule recherchée
        else : # Sinon on passe à la suivante
            i+=1
# --------------------------------

# ================================
#      Vérifications finales
# ================================

# --------------------------------
def verif_tous_routeurs_pasDansMur(liste_routeurs_connectes): # Pour la vérification finale
    for i in range (len(liste_routeurs_connectes)):
        routeur = liste_routeurs_connectes[i]
        if(routeur.cellule.type == '#'):
            choix = proposer_cellules_nonMur(routeur)
            routeur.cellule = choix[0] # Prend une nouvelle cellule pour le routeur
    print("nouvelle liste")
    for i in range (len(liste_routeurs_connectes)):
        print (liste_routeurs_connectes[i].cellule.coord)
# --------------------------------

# --------------------------------
def verif_budget():
    if( ((len(backbone)) * prix_backbone + (len(liste_routeur)) * prix_routeur) > budget ): # Nb cellules cablées et nb routeurs
        return True
    else:
        return False
# --------------------------------

# --------------------------------
def score (liste_routeur):
    nb_celluleWifi = 0
    for i in range (len(liste_routeur)):
        nb_celluleWifi += len(liste_routeur[i].liste_cellules_couvertes)
    return (1000 * nb_celluleWifi + budget)
# --------------------------------

# ================================
#          Fichier Fin
# ================================

# --------------------------------
def fichier_de_fin(backbone,liste_routeur):
	la_fin = open("bilan.text","a")
        # Ouvre/crée un fichier texte, utilise 'la_fin' afin de le traiter en python, écris en append, sans écraser mais en complétant :)
	cellules_co_BN = fonction_backbone()
	la_fin.write(cellules_co_BN,"cellules sont connectées au backbone \n")
	for x in backbone:
		la_fin.write("Cellule","[",x,"]","je sais pas quoi mettre, on trouvera plus tard \n")
	la_fin.write(len(liste_routeur),"routeurs \n")
	for y in liste_routeur:
		la_fin.write("[",y,"]","est connecté au backbone et ce n'est pas un mur du coup, on met là voilà, donc ça nous met à l'aise =D \n")#Vous avez vraiment besoin de lire un commentaire après une ligne comme ça ?
	la_fin.write(verif_budget(),"\n")
	la_fin.write(score(liste_routeur))
	la_fin.close()
# --------------------------------

# ================================
#      Appels des fonctions
# ================================

# ===== Récupérer fichier ========
fichier_infos = recuperer_fichier("./charleston_road.in")
donnees = fichier_infos[1]

# ===== Variables globales =======

liste_map = fichier_infos[0] # Liste de toutes les cellules
ligne = int(donnees[0])
colonne = int(donnees[1])
rayon = int(donnees[2])
prix_backbone = int(donnees[3])
prix_routeur = int(donnees[4])
budget = int(donnees[5])
backbone = []
liste_routeur = []

# ===== Variable Backbone ========

backbone.append(return_cellule([donnees[6],donnees[7]]))  

Placer_routeur()
print(score(liste_routeurs))

#b = [(23,24),(458,89),(45,3216),(7854,481)]
#r = [(12,447),(4,652),(5698745)]
#fichier_de_fin(b,r)
