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