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
    
    # On parcourt chaque element(=ligne) du tableau et chaque caractère de ces éléments
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
      
    return liste_map,donnees # Retourne liste avec les cellules et les données de la map
# --------------------------------

# ================================
#      Fonction auxiliaires
# ================================

# Calcule distance entre 2 points
# --------------------------------
def dist(coord1,coord2):
    s = 0 
    for i in range (0,2):
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

# Retourne la cellule du tableau avec les coordonnées rentrées en paramètre
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
        if dist(coord,a.coord) < rayon and elimination(a.coord,cellrouteur) == False and a.etat_wifi == False :  # a est la case évaluée, cellrouteur est le routeur considéré
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

# Elimine couverture d'une case s'il y a un mur entre celle-ci et le routeur
# --------------------------------
def elimination(coordonnees, routeur):   #ici le "routeur"  un Routeur
    res = False
    cellule = return_cellule(coordonnees)
    x = abs(coordonnees[0] - routeur.coord[0]) +1 # Largeur rectangle
    y = abs(coordonnees[1] - routeur.coord[1]) +1 # Hauteur rectangle
    for i in range (x) :
        for j in range (y) :
            cellule_a_verifier = return_cellule([coordonnees[0]-i,coordonnees[1]-j])
            if cellule_a_verifier != None :                        # On vérifie qu'il y a bien une cellule
                if cellule_a_verifier.type =='#'  : # Présence d'un mur
                    res = True 
    return res # Si ça élimine alors True sinon False car on la garde
# --------------------------------

# ================================
#        Placer Routeur
# ================================

# --------------------------------
def Placer_routeur():
    global budget
    global backbone
    global liste_routeurs
    for case in liste_map :
        # On parcourt la carte jusqu'à une case non couverte
        if (case.etat_wifi == False and case.type=='.') :
            # On crée une liste vide qui accueillera la liste des candidats à devenir routeurs
            listcandidrout = []
            for cellule in liste_map :
                if dist(cellule.coord,case.coord) < rayon and cellule.type !='#' :
                    listcandidrout.append(cellule)
            (cell,l)=(plusfort(listcandidrout))
            # Coord est la paire de coordonnées du routeur choisi, celui qui couvre le plus de nouvelles cases,
            # l est la liste des cases nouvellement couvertes
            
            if budget - prix_routeur > 0 :
                # Si ça rentre dans le budget
                budget -= prix_routeur
                r1 = Routeur(cell,l) # On crée le routeur r1
                liste_routeurs.append(r1)
                print(r1.cellule.coord )
                for case in r1.liste_cellules_couvertes :
                    case.etat_wifi = True
                backbone = Relier(r1.cellule.coord,backbone)[0]           
                # ON FAIT LA SUPPOSITION QUE LE PRIX POUR RELIER UN ROUTEUR AU BACKBONE
                # NE SERA PAS DETERMINANT POUR FRANCHIR LA BARRE DU BUDGET : optimisable
                budget -= Relier(cell.coord,backbone)[1] * prix_backbone # Budget s'autodécrémente
            else :
                break
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
        nb = 0
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


# ================================
#      Vérifications finales
# ================================

def verif_budget(budget_initial):
    if( ((len(backbone)) * prix_backbone + (len(liste_routeur)) * prix_routeur) > budget_initial ): # Nb cellules cablées et nb routeurs
        return True
    else:
        return False
# --------------------------------

# Retourne la liste des cases couvertes
# --------------------------------
def cases_couvertes ():
    l=[]
    for a in liste_routeurs :
        for case in a.liste_cellules_couvertes :
            l.append(case)
    return(l)
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
    with open("D:\Documents\G12_charleston_road.out","a") as fichier:
        count_cellConnect = str(len(backbone))+'# cellules connectées\n'
        fichier.write(count_cellConnect)
        for cell in backbone:
            ajout = str(cell[0])+' '+str(cell[1])+'\n'
            fichier.write(ajout)
        count_routeurs = str(len(liste_routeurs))+'# routeurs \n'
        fichier.write(count_routeurs)
        for cell in liste_routeurs:
            ajout = str(cell.cellule.coord[0])+' '+str(cell.cellule.coord[1])+'\n'
            fichier.write(ajout)
# --------------------------------

# ================================
#      Appels des fonctions
# ================================

# ===== Récupérer fichier ========
fichier_infos = recuperer_fichier("./cartes/charleston_road.in")
donnees = fichier_infos[1]

# ===== Variables globales =======

liste_map = fichier_infos[0] # Liste de toutes les cellules
ligne = int(donnees[0])
colonne = int(donnees[1])
rayon = int(donnees[2])
prix_backbone = int(donnees[3])
prix_routeur = int(donnees[4])
budget = int(donnees[5])
backbone_coord=[int(donnees[6]),int(donnees[7])]
backbone = []
liste_routeurs = []

# ========= Lancement ============

backbone.append(backbone_coord)
budget_initial=budget
Placer_routeur()
print(score(liste_routeurs))
fichier_de_fin(backbone,liste_routeurs)
