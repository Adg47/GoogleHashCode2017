##variables :
backbone =[]
rayon=rayon
budget=budget
prix_routeur = Pr
prix_backbone= prixuncable
liste_map=[]

def dist(coord1,coord2):
    s=0 
    for i in range (0,len(coord1)):
        s+=(coord1[i]-coord2[i])**2    #ajout des (xi-yi)²
    return (sqrt(s))

def mini(liste):
    min=liste[0]
    for i in range(0,len(liste)):
        if liste[i] < min :
            min=liste[i]
    for i in range (0,len(liste)):
        if liste[i] == min: 
            j=i
    return(min,j)             #retourne le minimum (mini(liste)[0]) et l'indice de la valeur minimum (mini(liste)[1]) PAS OPTIMISE MAIS OSEF SAMER
 
def voisins(case):            #retourne la liste des coordonnées des cases voisines d'une CASE entrée
    x=case[0]
    y=case[1]
    return([[x,y+1],[x,y-1],[x-1,y],[x-1,y+1],[x-1,y-1],[x+1,y+1],[x+1,y],[x+1,y-1]])

def relier(routeur,backbone):  #prend en compte seulement les coordonnées du routeur, et la liste des coordonnées des cases par lesquels passent la backbone 
    listdist=[] #liste des distances des points du backbone au routeur
    for a in backbone :
        listdist.append(dist(a,routeur))  #la listdist est remplie de distances des points de backbone au routeur dans le MEME ordre
    if mini(listdist)[0] < 1.4 : 
        print("le routeur est déjà relié à la backbone")
    else :
        nb=1     #compteur du nombre de cases rajoutées au backbone (commence à 1 pour compter la case routeur)
        while mini(listdist)[0] >1.4:
            nb+=1
            extremite=backbone[mini(listdist)[1]]       # l'extremité est la case du backbone la plus proche du routeur
            candidats=voisins(extremite)
            distcand=[]
            for a in candidats :
                distcand.append(dist(routeur,a))
            backbone.append(candidats[mini(distcand)[1]])  #on rajoute la nouvelle case à backbone
            listdist.append(mini(distcand)[0])
        backbone.append(routeur)                           #on finit enfin par cabler le routeur
    return(backbone,nb)

def elimination(coordonnees, routeur):
    #dans cette fonction je dois partir de ma case et regarder si dans le rectangle quelle forme avec le routeur
    #j'ai un mur ou non
    res = False
    cellule = coordtocell(coordonnees)
    x = abs(coordonnees[0] - routeur.cellule.coord[0]) +1 #largeur rectangle
    y = abs(coordonnees[1] - routeur.cellule.coord[1]) +1 #hauteur rectangle
    for i in range (x) :
        for j in range (y) :
            cellule_a_verifier = coordtocell([coordonnees[0]-i,coordonnees[1]-j])
            
            if cellule_a_verifier != None : # On vérifie qu'il y a bien une cellule
                if (verif_MurCellule(cellule_a_verifier)== True) : #Présence d'un mur
                    res = True 
    return res  # Si ça élimine alors true sinon false car on la garde


def verif_MurCellule(cellule): #Permet de vérifier si une cellule est un mur ou non
    if(cellule.type=='#'):
        return True
    else :
        return False
        
def coordtocell(coordonnees): 
# Permet de retrouver une cellule grâce aux coordonees
# Retourne la cellule recherchée
    i=0                      
    cellule_parcourue = liste_map[0]
    while( (cellule_parcourue.coord != coordonnees) and (i<len(liste_map))): #parcours toute la carte
        cellule_parcourue = liste_map[i]
        if(cellule_parcourue.coord==coordonnees): #si la cellule a les bonnes coordonnées
               return cellule_parcourue #on retourne la cellule recherchée
        i+=1


def liste_couvertes(cellrouteur):
    liste=[]
    coord=cellrouteur.coord      #coord contient juste les coordonnées de cellrouteur, la case dont nous allons retourner la liste des cases qui seraient couvertes si cette case était routeur
    for a in liste_map :
        if dist(coord,a.coord) <rayon and elimination(coord,a.coord) ==False ans a.couv==False :
            liste.append(a)
    return(liste)


def plusfort(listecandidats):  #choisit le candidat routeur qui couvre le plus de nouvelle cases
    c=0
    for candidat in listecandidats :
        if len(liste_couvertes(candidat)) > c :
            gagnant = candidat
            c=len(liste_couvertes(candidat))
    return(gagnant,liste_couvertes(gagnant))
    
    



def Placer_routeur():
    for case in liste_map :                       #on parcourt la carte jusqu'à une case non couverte
        if case.etat_wifi==False :
            listcandidrout=[]               #on crée une liste vide qui accueillera la liste des candidats à devenir routeurs
            '''pour l'instant on travaille uniquement avec des cellules, pas de coordonnées'''
            for cellule in liste_map :            
                if dist(cellule.coord,case.coord)<rayon and verif_MurCellule(cellule)==False :
                    listcandidrout.append(cellule)
            (coord,l)=(plusfort(listecandidrout))            #cord est la paire de coordonnée du routeur choisi, celui qui couvre le plus de nouvelles cases, l est la liste des cases nouvellement couvertes
            if budget -prix_routeur > 0 :                                  #si ça rentre dans le budget ,
                budget-=prix_routeur
                r1=Routeur(coordtocell(coord),l)             #on crée le routeur r1
                liste_routeur.append(r1)
                for case in r1.liste_cellules_couvertes :
                    case.etat_wifi=True
                backbone=relier(cord,backbone)[0]           
                #ON FAIT LA SUPPOSITION QUE LE PRIX POUR RELIER UN ROUTEUR AU BACKBONE NE SERA PAS DETERMINANT POUR FRANCHIR LA BARRE DU BUDGET : optimisable
                budget-=relier(coord,backbone)[1]*prix_backbone
                
                