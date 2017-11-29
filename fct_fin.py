def fichier_de_fin(backbone,liste_routeur):
	la_fin =open("bilan.text","a") # Ouvre/crée un fichier texte, utilise 'la_fin' afin de le traiter en python, écris en append, sans écraser mais en complétant :)
	cellules_co_BN=fonction_backbone()
	la_fin.write(cellules_co_BN,"cellules sont connectées au backbone \n")
	for x in backbone:
		la_fin.write("Cellule","[",x,"]","je sais pas quoi mettre, on trouvera plus tard \n")
	la_fin.write(len(liste_routeur),"routeurs \n")
	for y in liste_routeur:
		la_fin.write("[",y,"]","est connecté au backbone et ce n'est pas un mur du coup, on met là voilà, donc ça nous met à l'aise =D \n")#Vous avez vraiment besoin de lire un commentaire après une ligne comme ça ?
	la_fin.write(verif_budget(),"\n")
	la_fin.write(score(liste_routeur))
	la_fin.close()
b = [(23,24),(458,89),(45,3216),(7854,481)]
r = [(12,447),(4,652),(5698745)]
	
fichier_de_fin(b,r)
