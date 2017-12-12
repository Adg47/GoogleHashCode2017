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
    def __init__(self, cellule, liste_cellules_couvertes = []):
        self.cellule = cellule
        self.rayon = rayon
        self.count = None # nb cellules couvertes par le wifi
        self.liste_cellules_couvertes = liste_cellules_couvertes # Liste des cellules couvertes par le wifi
  
    # Retourne la liste des cellules couvertes
    def liste_couvertes(self):
        liste_murs = []
        x = 0
        y = 0
        liste_cell = []
        larg_portee = 1 + rayon * 2 # Calcul de la largeur de la portée wifi en fct du rayon
        for i in range(larg_portee):
            for j in range(larg_portee):
                x = self.cellule.coord[0] - rayon + j
                y = self.cellule.coord[1] - rayon + i
                if( 0 < x < colonne and 0 < y < ligne and (x != self.cellule.coord[0] or y != self.cellule.coord[1])): # Si x et y pas négatif donc pas hors de la carte
                    cell = return_cellule([x,y])
                    if( cell != None):
                        if( cell.type == '.' and self.elimination(cell.coord) == False):
                            liste_cell.append(cell)

        self.liste_cellules_couvertes = liste_cell
        self.count = len(self.liste_cellules_couvertes)
        return self.liste_cellules_couvertes
    
    # Elimine couverture d'une case s'il y a un mur entre celle-ci et le routeur
    # --------------------------------
    def elimination(self, coordonnees):
        res = False
        cellule = return_cellule(coordonnees)
        x = abs(coordonnees[0] - self.cellule.coord[0]) +1 # Largeur rectangle
        y = abs(coordonnees[1] - self.cellule.coord[1]) +1 # Hauteur rectangle
        for i in range (x) :
            for j in range (y) :
                cellule_a_verifier = return_cellule([coordonnees[0]-i,coordonnees[1]-j])
                if cellule_a_verifier != None : # On vérifie qu'il y a bien une cellule
                    if cellule_a_verifier.type =='#'  : # Présence d'un mur
                        res = True 
        return res # Si ça élimine alors True sinon False car on la garde
    # --------------------------------
                    
# --------------------------------

# ================================
#       Fichier => Données
# ================================

# Récupère fichier et le transforme en données et liste de cellules
# --------------------------------
def recuperer_fichier(chemin_fichier):
    global rayon
    global liste_map
    global liste_pas_mur
    global ligne
    global colonne
    
    fichier = []
    fichier_str = ''
    donnees = []
    liste_map = []
    liste_pas_mur = []

    # Transformation fichier en string pour le schéma et en tableau pour les données
    with open(chemin_fichier,"r") as source:
        for line in source:
            element = line.strip()
            fichier.append(element)
            
    # Séparation des données
    for i in range(3):
        donnees.extend(fichier[0].split())
        del fichier[0]

    rayon = int(donnees[2])
    ligne = int(donnees[0])
    colonne = int(donnees[1])
    
    # Création string
    for tab in fichier:
        fichier_str = fichier_str + tab
    
    # On parcourt chaque element( = ligne ) du tableau et chaque caractère de ces éléments
    # puis on crée une Cellule pour chacun de ces caractères
    x = 1
    y = 1
    for car in fichier_str:
        if(car == "-"):
            liste_map.append(None)
        else:
            element = Cellule([int(x),int(y)],car)
            liste_map.append(element)
            
            # on crée directement une liste avec des routeurs possibles
            if (car == '.'):
                routeur = Routeur(element)
                liste_pas_mur.append(routeur)
                
        if(x == int(donnees[1])):
            x = 1
            if(y != int(donnees[0])):
                y = y + 1
        else:
            x = x + 1

    for routeur in liste_pas_mur:
            routeur.liste_couvertes()
        
    # Retourne liste avec les cellules, les données de la map et la liste des routeurs possibles
    return donnees
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
    nb_tab = (int(coord[1]) - 1) * colonne + (int(coord[0]) - 1)
    return liste_map[nb_tab]
# --------------------------------

# Choisit le candidat routeur qui couvre le plus de nouvelles cases dans liste_pas_mur
# --------------------------------
def plusfort():
    global liste_pas_mur
    c = 0
    i = 0
    place = 0
    gagnant = None
    for candidat in liste_pas_mur :
        if (candidat.count > c) :
            gagnant = candidat
            c = candidat.count
            place = i
        i += 1
    del liste_pas_mur[place]
    
    return gagnant
# --------------------------------

# ================================
#        Placer Routeur
# ================================

# --------------------------------
def Placer_routeur():
    global budget
    global backbone
    global prix_backbone
    global liste_routeurs
    global liste_pas_mur

    fin = False
    
    while ( fin == False):
        # Si ajouter un routeur est dans le budget
        if (budget - prix_routeur > 0) :
            # On choisit le routeur qui donne couvrent le plus de cellule
            cell = plusfort()
            if (cell != None):
                # Si le relier au backbone est dans le budget
                if (budget - Relier(cell.cellule.coord,backbone)[1] * prix_backbone >= 0):
                    liste_routeurs.append(cell) # Ajout du routeur dans la liste
                    print(cell.cellule.coord )

                    backbone = Relier(cell.cellule.coord,backbone)[0] # On met les coordonnées des cellules reliant le routeur au backbone
                    budget -= prix_routeur + Relier(cell.cellule.coord,backbone)[1] * prix_backbone # Budget s'autodécrémente

                    # On indique que les cases que couvrent le routeur sont couvertes par le wifi
                    return_cellule(cell.cellule.coord).etat_wifi = True
                    for case in cell.liste_cellules_couvertes :
                        return_cellule(case.coord).etat_wifi = True

                    # On met à jour la liste des cellules couvertes par les routeurs candidats
                    d = 0
                    for root in liste_pas_mur:
                        aide = []
                        if(root.cellule.etat_wifi == True):
                            del liste_pas_mur[d]
                            d -= 1
                        else:
                            for i in range(len(root.liste_cellules_couvertes)) :
                                if(root.liste_cellules_couvertes[i].etat_wifi == True):
                                    aide.append(i)
                            j = len(aide) - 1
                            while (j >= 0):
                                del root.liste_cellules_couvertes[j]
                                j -= 1
                            root.count = len(root.liste_cellules_couvertes)
                        d += 1
                # Si budget pas assez grand pour relier, on arrête
                else :
                    fin = True
            else:
                fin = True
        # Si budget pas assez grand pour ajouter routeur, on arrête
        else:
            fin = True
    return True
# --------------------------------

# ================================
#    Relier Routeur-Backbone
# ================================

# --------------------------------
def Relier(routeur, backbone):
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

# Vérification du budget
# --------------------------------
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

# ================================
#          Fichier Fin
# ================================

# Création du fichier final .out
# --------------------------------
def fichier_de_fin(backbone, liste_routeurs):
    with open(nom_carte,"a") as fichier:
        count_cellConnect = str(len(backbone))+'\n'
        fichier.write(count_cellConnect)
        for cell in backbone:
            ajout = str(cell[1]-1)+' '+str(cell[0]-1)+'\n'
            fichier.write(ajout)
        count_routeurs = str(len(liste_routeurs))+'\n'
        fichier.write(count_routeurs)
        for cell in liste_routeurs:
            ajout = str(cell.cellule.coord[1]-1)+' '+str(cell.cellule.coord[0]-1)+'\n'
            fichier.write(ajout)
    print('Le fichier a été créé ici: ',nom_carte)
# --------------------------------

# ================================
#      Appels des fonctions
# ================================

# ===== Récupérer fichier ========

chemin_carte = input('Chemin de la carte à analyser :')
nom_carte = input('Chemin + Nom du fichier de fin :') 
donnees = recuperer_fichier(chemin_carte)
#donnees = recuperer_fichier('D:\Documents\Polytech\Polyhash\cartes/charleston_road.in')

# ==== Variables globales ========
prix_backbone = int(donnees[3])
prix_routeur = int(donnees[4])
budget = int(donnees[5])
backbone_coord = [int(donnees[7]),int(donnees[6])]
liste_routeurs = []
backbone = []

# ========= Lancement ============

backbone.append(backbone_coord)
budget_initial = budget
Placer_routeur()
fichier_de_fin(backbone,liste_routeurs)
