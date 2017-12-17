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
    # --------------------------------
    def liste_couvertes(self):
        x = 0
        y = 0
        liste_cell = [] # Liste cellule couvertes par routeur
        larg_portee = 1 + rayon * 2 # Calcul de la largeur de la portée wifi en fct du rayon
        
        # On parcourt toute les cases de la portée wifi du routeur
        for i in range(larg_portee):
            for j in range(larg_portee):
                
                # Calcul des coordonnées des cases en fonction de celles du routeur
                x = self.cellule.coord[0] - rayon + i
                y = self.cellule.coord[1] - rayon + j
                
                # Si x et y pas négatif donc pas hors de la carte
                if( 0 <= x < ligne and 0 <= y < colonne):
                    cell = return_cellule([x,y])
                    # Si cellule pas None donc pas un vide '-'
                    if( cell != None):
                        if( cell.type == '.' and self.elimination(cell.coord) == False ) :
                            liste_cell.append(cell)

        self.liste_cellules_couvertes = liste_cell
        self.count = len(self.liste_cellules_couvertes)
        
        return self.liste_cellules_couvertes
    
    # Elimine couverture d'une case s'il y a un mur entre celle-ci et le routeur
    # --------------------------------
    def elimination(self, coord):
        
        res = False

        x = coord[0] - self.cellule.coord[0] # Différence ligne
        y = coord[1] - self.cellule.coord[1] # Différence colonne
        a = 0
        b = 0
        
        for i in range (0,abs(x)+1) :
            for j in range (0,abs(y)+1) :
                # Pour savoir de quel côté, le backbone se trouve et donc
                # comment on se déplace dans le rectangle
                if ( x > 0 ):
                    a = coord[0] - i
                else:
                    a = coord[0] + i
                if ( y > 0 ):
                    b = coord[1] - j
                else:
                    b = coord[1] + j

                cell_verif = return_cellule([a,b])
                if cell_verif != None : # On vérifie qu'il y a bien une cellule
                    if cell_verif.type == '#'  : # Présence d'un mur
                        res = True
                        
        return res # Si ça élimine alors True sinon False car on la garde
    # --------------------------------

    # Relier Routeur-Backbone
    # --------------------------------
    def relier(self):
        global backbone
        listdist = [] # Liste des distances des points du backbone au routeur
        
        for a in backbone :
            listdist.append(dist(a,self.cellule.coord)) # Remplie avec les distances des points du backbone au routeur dans le MÊME ordre
            
        if mini(listdist)[0] < 1.4 : 
            nb = 0
            backbone.append(self.cellule.coord)  #si le routeur est à proximité du backbone, on ne cable que lui
        else :
            
            nb = 1 # Compteur du nombre de cases rajoutées au backbone (commence à 1 pour compter la case routeur)
            
            while mini(listdist)[0] > 1.4:
                
                nb += 1
                extremite = backbone[mini(listdist)[1]] # L'extremité est la case du backbone la plus proche du routeur
                candidats = voisins(extremite)
                distcand = []
                
                for a in candidats :
                    distcand.append(dist(self.cellule.coord,a))
                    
                backbone.append(candidats[mini(distcand)[1]]) # On rajoute la nouvelle case à backbone
                listdist.append(mini(distcand)[0])
                
            backbone.append(self.cellule.coord) # On finit enfin par cabler le routeur
            
        return(backbone,nb)
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
    # puis on crée une Cellule() pour chacun de ces caractères
    x = 0 # Ligne
    y = 0 # Colonne
    for car in fichier_str:
        if(car == "-"):
            liste_map.append(None)
        else:
            element = Cellule([int(x),int(y)],car)
            liste_map.append(element)
            
            # On crée directement une liste avec des routeurs possibles
            if (car == '.'):
                routeur = Routeur(element)
                liste_pas_mur.append(routeur)

        # Incrémentation en fonction du nombre de ligne et colonne
        if ( y == colonne - 1):
            y = 0
            if (x != ligne - 1):
                x += 1   
        else:
            y += 1

    a = 0
    for routeur in liste_pas_mur:
        a += 1
        routeur.liste_couvertes()
        print(a)
    print('-----------------')
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

# Retourne le minimum (mini(liste)[0]) et l'indice de la valeur minimum (mini(liste)[1])
# --------------------------------
def mini(liste):
    min = liste[0]
    j = 0
    for i in range(0,len(liste)):
        if liste[i] < min :
            min = liste[i]
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

# Choisit le candidat routeur qui couvre le plus de nouvelles cases dans liste_pas_mur
# --------------------------------
def plusfort():
    global liste_pas_mur
    c = 0
    i = 0
    place = 0
    gagnant = None
    for candidat in liste_pas_mur :
        if(candidat != None):
            if (candidat.count > c and candidat.cellule.etat_wifi == False) :
                gagnant = candidat
                c = candidat.count
                place = i
        i += 1
    del liste_pas_mur[place]
    
    return gagnant
# --------------------------------

# Retourne la cellule du tableau avec les coordonnées rentrées en paramètres
# --------------------------------
def return_cellule(coord):
    nb_tab = int(coord[0]) * colonne + int(coord[1])
    return liste_map[nb_tab]
# --------------------------------
# ======================================
#       Fonction verification backbone
# ======================================

# --------------------------------
def verifbackbone(backbone):   #vérifie qu'une case n'est pas cablée deux fois. Retourne la version "corrigée" du backbone.
    verif=[]
    for a in backbone :
        if a not in verif :
            verif.append(a)
    return(verif) 
# --------------------------------

# ================================
#       Fonction principale
# ================================

# --------------------------------
def Placer_routeur():
    global budget
    global backbone
    global prix_backbone
    global liste_routeurs
    global liste_pas_mur

    fin = False
    
    while ( fin == False and budget > 4*prix_routeur):  
    #4*prix routeur est une estimation de ce qu'il faudrait. Normalement la condition fin devrait suffire
        cell = plusfort()    # On choisit la case où un routeur couvrirait le plus de cellule
        if (cell != None):
            # Si ajouter un routeur est dans le budget
            if (budget - (prix_routeur +(cell.relier()[1] * prix_backbone)) > 0) :
                liste_routeurs.append(cell) # Ajout du routeur dans la liste
                print(cell.cellule.coord)
                backbone = cell.relier()[0] # On met les coordonnées des cellules reliant le routeur au backbone
                budget -= prix_routeur + cell.relier()[1] * prix_backbone # Budget s'autodécrémente
                # On indique que les cases que couvrent le routeur sont couvertes par le wifi
                cell.cellule.etat_wifi = True
                for case in cell.liste_cellules_couvertes :
                    case.etat_wifi = True
                # On met à jour la liste des cellules couvertes par les routeurs candidats
                for root in liste_pas_mur:
                    aide = []
                    # Si cellule routeur est couverte on l'enlève en mettant None
                    if(root.cellule.etat_wifi == True):
                        root = None
                    else:
                        for i in range(len(root.liste_cellules_couvertes)) :
                            if(root.liste_cellules_couvertes[i].etat_wifi == True):
                                aide.append(i)
                        j = len(aide) - 1
                        while (j >= 0):
                            del root.liste_cellules_couvertes[j]
                            j -= 1
                        root.count = len(root.liste_cellules_couvertes)
                            
            # Si budget pas assez grand pour ajouter un routeur et le relier, on arrête
            else:
                fin = True
        else:
            fin = True
    return True
# --------------------------------

# ================================
#          Fichier Fin
# ================================

# Création du fichier final .out
# --------------------------------
def fichier_de_fin(backbone, liste_routeurs):
    global backbone_coord
    with open(nom_carte,"a") as fichier:
        count_cellConnect = str(len(backbone)-1)+'\n'
        fichier.write(count_cellConnect)
        for cell in backbone:
            if(cell[0] != backbone_coord[0] or cell[1] != backbone_coord[1]):
                ajout = str(cell[0])+' '+str(cell[1])+'\n'
                fichier.write(ajout)
        count_routeurs = str(len(liste_routeurs))+'\n'
        fichier.write(count_routeurs)
        for cell in liste_routeurs:
            ajout = str(cell.cellule.coord[0])+' '+str(cell.cellule.coord[1])+'\n'
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
#donnees = recuperer_fichier('charleston_road.in')

# ==== Variables globales ========

prix_backbone = int(donnees[3])
prix_routeur = int(donnees[4])
budget = int(donnees[5])
backbone_coord = [int(donnees[6]),int(donnees[7])]
liste_routeurs = []
backbone = []
backbone.append(backbone_coord)

# ========= Lancement ============

Placer_routeur()
backbone=verifbackbone(backbone)
fichier_de_fin(backbone,liste_routeurs)
