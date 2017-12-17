Pandiculation

Projet Polyhash 2017 : Tiphaine Besnard, Clara Montagné, Alexis de Guisti, Raphaël Sanglier
Description
Répartition des tâches :
Tiphaine : Retranscription de l'énoncé, création de fonctions auxiliaires et de la structure de données, architecture de la fonction PlacerRouteurs()
Clara : Conversion du fichier ASCII en ce que l'on veut, aide sur GIT, Traitement du fichier de sortie
Alexis : Traitement du fichier de sortie, création du montage vidéo
Raphaël : Création de la fonction gérant le backbone, architecture et codage de la fonction PlacerRouteurs()

#procédure d'installation
Besoin d'un logiciel ou autres qui puissent exécuter un programme python

#procédure d'éxécution
Le chemin de la carte à analyser est demandé en paramètre en premier
Puis le chemin avec le nom du fichier contenant les données qui sera créé à la fin du programme

#stratégies mises en œuvre et commentaire à propos des performances (temps exécuteur et place mémoire)
Selection à répétition de cellules couvrant le plus de cases possibles à chaque fois. Mise à jour du backbone au fur et à mesure.

#organisation des codes en classes, modules, fonctions. 
Classe routeur 
Classe Cellule 
Liste des fonctions indépendantes :
Recuperer_ficher(chemin_fichier) : permet de récupérer le fichier d’entrée et de séparer les données de la carte. 
Dist(coord1, coord2) : permet de calculer la distance entre 2 points.
Mini(liste) : retourne le minimum ainsi que l’indice où il se trouve de la liste.
Voisins(case) : retourne la liste des voisins de la case.
Return_cellule(coord) : retourne la cellule du tableau avec les coordonnées rentrées en paramètre. 
Liste_couverture(cellrouteur) : retourne la liste des cellules couvertes si la case en paramètre était un routeur.
Plusfort(listecandidats) : choisit le candidat routeur qui couvre le plus de nouvelles cases.
Elimination(coordonnees, routeur) : elimine la couverture de la cellule s’il y a un mur entre elle et le routeur.
Placer_routeur() : fonction principale qui permet de placer les routeurs en utilisant les fonctions 

#bugs et limitations
La gestion du budget est très limitée. Elle ne permet pas d'avoir un score correct ou une bonne couverture pour certaines cartes. 
#autre
