def fichier_de_fin(backbone,routeurs):
	la_fin =open("bilan.text","a") # Ouvre/crée un fichier texte, utilise 'la_fin' afin de le traiter en python, écris en append, sans écraser mais en complétant 
	la_fin.write(str(len(backbone))+"cellules sont connectées au backbone \n")#Nombre de cellules connectées au backbone
	for x in range(len(backbone)):
		la_fin.write("Cellule"+str(backbone[x][0])+ " "+str(backbone[x][1]+"voisine de la CIB \n") #Ecrit les cellules voisines du backbone
	la_fin.write(len(liste_routeur),"routeurs \n")#Nombre de routeurs
	for y in range(len(routeurs)):
		la_fin.write(str(routeurs[y][0])+" "+str(routeurs[y][1] +"est connecté au backbone et ce n'est pas un mur du coup, on met là voilà, donc ça nous met à l'aise =D \n")#Ecrit les coordonnées de chaque routeur
	la_fin.write(score(liste_routeur))#Ecrit score
	la_fin.close()
	
fichier_de_fin(backbone, liste_routeurs) 
