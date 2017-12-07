Pandiculation

Projet Polyhash 2017 : Tiphaine Besnard, Clara Montagné, Alexis de Guisti, Raphaël Sanglier
Description
Répartition des tâches :
Tiphaine : Retranscription de l'énoncé, création de fonctions auxiliaires et de la structure de données, architecture de la fonction PlacerRouteurs()
Clara : Conversion du fichier ASCII en ce que l'on veut, aide sur GIT, Traitement du fichier de sortie
Alexis : Traitement du fichier de sortie, création du montage vidéo
Raphaël : Création de la fonction gérant le backbone, architecture et codage de la fonction PlacerRouteurs()

#procédure d'installation
Rien à installer pour lancer le programme à part quelque chose pour exécuter un programme en python
#procédure d'éxécution
Pour l’instant il faut changer le nom de la carte à l’intérieur du code mais cela va bientôt être changé pour que l’on passe en paramètre le nom de la carte et pouvoir exécuter directement.
#stratégies mises en œuvre et commentaire à propos des performances (temps exécuteur et place mémoire)
Parcours de la carte pour placer les routeurs en sélectionnant les cellules qui couvrent en wifi le plus de case possible. Temps d’exécution très long (plusieurs heures).
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

#autre
