##### Vérification du type de case des routeurs et changement si besoin ####

            
def proposer_cellules_nonMur(routeur):
    liste_coordVoisins = voisins(routeur.cellule.coord) #il récupère toutes les coord des voisins.
    liste_voisines = [] #liste des cellules voisines à remplir
    for i in range (len(liste_coordVoisins)): # parcours les coordonnées des voisins du routeur
        if recherche_celluleNonMur_avecCoordonnees(liste_coordVoisins[i]): 
            liste_voisines.append(recherche_celluleNonMur_avecCoordonnees(liste_coordVoisins[i]))
            #ajoute la cellule aux voisines possibles si elle existe et n'est pas un mur

    return liste_voisines # retourne la liste des voisines dispo


def verif_MurCellule(cellule): #Permet de vérifier si une cellule est un mur ou non
    if(cellule.type=='#'):
        return True
    else :
        return False

def verif_Cellule_libre(cellule): # Permet de savoir si une cellule est prise par un routeur ou non
    for i in range (len(liste_routeurs)):
        if(liste_routeurs[i].cellule == cellule): # si la cellule est dans la liste des routeurs alors non libre
            return False #prise par routeur
        else :
            return True #libre
    
def recherche_celluleNonMur_avecCoordonnees(coordonnees): 
# Permet de retrouver une cellule grâce aux coordonees et vérifie si ce n'est pas un mur
# Retourne la cellule recherchée
    i=0                      
    cellule_parcourue = liste_map[0]
    while( (cellule_parcourue.coord != coordonnees) and (i<len(liste_map))): #parcours toute la carte
        cellule_parcourue = liste_map[i]
        if(cellule_parcourue.coord==coordonnees): #si la cellule a les bonnes coordonnées
            if (verif_MurCellule(cellule_parcourue)==False) and (verif_Cellule_libre(cellule_parcourue)==True): # si la cellule n'est pas de type mur
               return cellule_parcourue #on retourne la cellule recherchée
        else : #sinon on passe à la suivante
            i+=1
    
def verif_tous_routeurs_pasDansMur(liste_routeurs_connectes): #Pour la vérification finale
    for i in range (len(liste_routeurs_connectes)):
        routeur = liste_routeurs_connectes[i]
        if(routeur.cellule.type == '#'):
            choix = proposer_cellules_nonMur(routeur)
            routeur.cellule = choix[0] #prend une nouvelle cellule pour le routeur
    print("nouvelle liste")
    for i in range (len(liste_routeurs_connectes)):
        print (liste_routeurs_connectes[i].cellule.coord)


###### Classes #######

class Cellule :
    def __init__(self, coordonnees , Type, etat_couverture = False):
        self.coord= coordonnees # entiers
        self.type = Type # Mur, cible, vide (#, ., -)
        self.etat_wifi = etat_couverture #True ou false

class Routeur :
    def __init__(self, cellule, liste_cellules_couvertes ):
        self.cellule = cellule
        self.rayon = rayon
        self.liste_cellules_couvertes = liste_cellules_couvertes  #liste des cellules couvertes par le wifi

    def ajout_cellules_dansListeCouverture(cellule):
        self.liste_cellules_couvertes.append(cellule) #Ajoute une cellule à la liste


##### Celles de Raph #####   

def voisins(case):            #retourne la liste des coordonnées des cases voisines d'une CASE entrée
    x=case[0]
    y=case[1]
    return([[x,y+1],[x,y-1],[x-1,y],[x-1,y+1],[x-1,y-1],[x+1,y+1],[x+1,y],[x+1,y-1]])

###### Vérification du budget et calcul du score #####
# récupéré les valeurs Pb, B et Pr dès le début

def verif_budget():
    if( ((len(backbone))*Pb + (len(liste_routeurs))*Pr) > B): #nbre cellules cablées et nbre routeurs
        return "Hors budget !!!!!!"

def score (liste_routeurs):
    nbre_celluleWifi = 0
    for i in range (len(liste_routeurs)):
        nbre_celluleWifi += len(liste_routeurs[i].liste_cellules_couvertes)
    return (1000*nbre_celluleWifi + (B-(N * Pb + M * Pr)))


######################
#valeurs données à titre indicatif
Pb = 12
Pr = 1
B = 55
backbone=[]
r=6
