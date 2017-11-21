from math import *
##fonctions auxiliaires
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

#on doit relier une case routeur [a,b] à une case centrale [x,y]

routeur = [7,3]
backbone=[[0,0],[1,0],[2,1],[3,1]]

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