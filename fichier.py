############## Class ################

class Cellule:
    def __init__(self, coordonnees, Type, etat_couverture = False):
        self.coord = coordonnees # entiers
        self.type = Type # Mur, cible, vide (#, ., -)
        self.etat_wifi = etat_couverture #True ou false

############# Transformation fichier => données ##############
        
def recuperer_fichier(chemin_fichier):
    fichier = []
    fichier_str = ''
    liste_map = []
    donnees = []

    #transformation fichier en string pour le schema et en tableau pour les donnees
    with open(chemin_fichier,"r") as source:
        for line in source:
            element = line.strip()
            fichier.append(element)
            
    #separation des donnees
    for i in range(3):
        donnees.extend(fichier[0].split())
        del fichier[0]

    #creation sting
    for tab in fichier:
        fichier_str = fichier_str + tab
    
    #on parcourt chaque element(=ligne) du tableau et chaque caractere de ces elements
    #puis on cree une Cellule pour chacun de ces caractères
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
      
    return liste_map,donnees 

#retourne la case du tableau avec la bonne cellule
def return_cellule(x,y):
    nb_tab = (int(y)-1)*ligne+(int(x)-1)
    return liste_map[nb_tab]
    

################################

#recup fichier
fichier_infos = recuperer_fichier("/comptes/etudiant/E179037F/Documents/Polyhash/charleston_road.in")
donnees = fichier_infos[1]

# ===== Variables globales ====== #

liste_map = fichier_infos[0] #liste de toutes les cellules
ligne = int(donnees[0])
colonne = int(donnees[1])
rayon = int(donnees[2])
prix_backbone = int(donnees[3])
prix_routeur = int(donnees[4])
budget = int(donnees[5])
backbone = []

# === Variable Backbone === #

backbone.append(return_cellule(donnees[6],donnees[7]).coord)
print (backbone[0])















