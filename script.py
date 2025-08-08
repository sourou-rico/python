# Tu es l'homme guido van Rossum
# print ("Hello, World!")
# print("Bonjour")

# mot = "Hello, World!"

# for x in mot:
#     print(x)
# print("Fin du script")

import random
nombre = random.randrange(1,10)
print(nombre)

import random
 
# Utilisation de print
print("Hello, word! 😎")
print("Bonjour")
 
## Déclaration de variable
 
#Types de variables en python
 
 
############### Types de texte ###############
 
## str => chaine de caractères
 
nom = "John Doe"
prenom = 'Martin pêcheur'
 
print(nom)
print(prenom)
 
print(nom + ' '+ prenom)
print(nom, prenom)
 
sentence = """ Bonjour, je suis Ishola Judicael Anthelme ACHADE et les triples quotes sont pour des texts multi-ligne
"""
print("Voici une phrase", sentence)
 
a = "Hello world!"
print(a[1])
 
mot = "Hello world!"
for x in mot: ## ['H','e','l','l','o','w','o','r','l','d','!']
    print(x)
 
print(len(mot)) ## 12 caractères
 
 
txt = "Rien n'est gratuit dans la vie 🤨."
print("Bonjour" in txt) ## false
 
if "vie" in txt:
    print("La chaine contient le mot vie.") ## Affiche ceci
else:
    print("Désolé, je ne retrouve pas ça.")
 
 
################ Types numériques #############
 
## int => Entier et float => Décimal
 
x = 1  # int => entier
y = 2.12 # float => nombre décimal
 
print(type(y))  ## <class 'float'>
 
a = x
print(a) ## 1
 
a = float(x)
print(a) ## 1.0
 
b = int(y)
print(b) ## 2
 
nombre = random.randrange(1, 10) ## au niveau des bornes, [1] est inclu mais [10] non
print(nombre)  ## 5
 
## triple égalité n'existe pas en python
 
print("Hello" == "Hello") ## false
print(0 == False) ## True
print(1 == True) ## True
 
 
x = 5
y = 20
print(x + y) ## 25
print(x - y) ## -15
print(x * y) ## 100
print(y%x) ## 0
print(x/y) ## 0.25
print(x//y) ## 0 returne la partie entière de la division on appelle sa la division entière
 
 
 
x = 10
print (x<5) ## False
print(x<5 and x> 8) ## False
print(x<5 or x> 8) ## True
print(not(x<5 and x> 8)) ## True
 
 
##Important je dis très important les booléens commencent toujours par une lettre majuscule en python
 
 
 
 
 
 
 
## complexe => Nombre complexe
 
 
############### Types de séquences ################
 
## list => Liste
## tuple => Tuple
 
#################### Types de mappage #############
 
## dict ==> Dictionnaire
 
#################### Types d'ensemble ###########
 
## set => Set
 
################### Types booléen ###############
 
## bool => Booléen

###############################
###############################

## Les listes
fruits = ["pomme", "banane", "cerise",2.5, "Melon"]

print(fruits)
fruits[1] = "Nouveau fruit" # la valeur a l'index 1 est modifiée
print(fruits) 

print(fruits[-1]) # Affiche le dernier élément de la liste
print(fruits[0:3]) # Affiche les 3 premiers éléments de la liste
print(fruits[1:]) # Affiche tous les éléments à partir de l'index 1
print(fruits[1:3]) # Affiche les éléments de l'index 1 à l'index 2
fruits.append("kiwi")  # Ajoute "kiwi" à la fin de la liste
fruits.insert(1, "orange")  # Insère "orange" à l'index 1 et décale les autres éléments
fruits.remove("Melon")  # Supprime "Melon" de la liste et retourne une erreur si l'élément n'existe pas
fruits.pop(2)  # Supprime l'élément à l'index 2 et le retourne
del fruits[0]  # Supprime l'élément à l'index 0 et ne le retourne pas
fruits.clear()  # Vide la liste
fruits.sort()  # Trie la liste par ordre alphabétique ou numérique et retourne une erreur si les types sont différents
fruits.sort(reverse=True)  # Trie la liste par ordre alphabétique ou numérique décroissant
fruits.sort(key=str.lower)  # Trie la liste par ordre alphabétique en ignorant la casse, le key prend une fonction qui retourne la valeur à comparer

##############################################
# FASTAPI | creer un environnement virtuel | activer l'environnement virtuel
##############################################
# FastAPI est un framework web pour créer des APIs en Python, il est basé sur Starlette et Pydantic.
# Pour l'utiliser, il faut installer un environnement virtuel avec pip, cela permet d'éviter les erreur de dependance et version
# Il est important de créer un environnement virtuel pour chaque projet, cela permet d'éviter les conflits de dépendances entre les projets.
# Pour créer un environnement virtuel, il faut utiliser la commande suivante : **pip install virtualenv** et ensuite créer l'environnement virtuel avec la commande : **virtualenv nom_de_l_environnement**
# on peut aussi utiliser la commande **python -m virtualenv nom_de_l_environnement** pour créer l'environnement virtuel.

# Pour activer l'environnement virtuel, il faut accéder au dossier de l'environnement virtuel et taper : **.\Scripts\activate**  

# Pour installer les dépendances du projet, il faut créer un fichier requirements.txt et y ajouter les dépendances du projet, puis utiliser la commande **pip install -r requirements.txt** pour installer les dépendances.

# le fichier requirements.txt contient:
# fastapi ## Dépendence pour installer FastAPI
# uvicorn ## Serveur ASGI pour exécuter l'application FastAPI ou lancer le serveur de développement du projet

# Pour lancer le serveur de développement du projet, il faut utiliser la commande **uvicorn nom_du_fichier(ici main):app --reload**. Le paramètre --reload permet de recharger le serveur à chaque modification du code.
