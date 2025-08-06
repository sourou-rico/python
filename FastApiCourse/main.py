from fastapi import FastAPI
from typing import Optional

## Création de l'application FastAPI
app = FastAPI(
    title="Mon Application FastAPI",
    description="Une API simple pour comprendre FastAPI.",
    version="0.1",
)

# Route pour la page d'accueil de notre application
@app.get("/")
def welcome():
    """ Page d'acceuil de l'API"""
    return {"message": "Bienvenue sur mon API"}

## Route GET avec un paramètre dans l'URL
@app.get("/bonjour/{name}")
def say_hello(name: str):
    """ Méthode qui permet de saluer un humain """
    return {"message": f"Bonjour {name}! ça va ?"}

## Route POST  pour calculer une somme
@app.post("/calculer-somme/")
def calculate_sum(number1: float, number2: float, number3: Optional[float]= None):
    """ Méthode qui permet de calculer la somme de deux nombres """
    result = number1 + number2 +  number3
    if number3 is not None:
        result = result + number3

    return {
        "nombre 1": number1,
        "nombre 2": number2,
        "nombre 3": number3,
        "resultat": result,
        }

# Route POST pour verifier un palindrome
@app.post("/verifier-palindrome/")
def check_palindrome(word: str):
    """ Méthode qui permet de vérifier si un mot est un palindrome """
    is_palindrome = word == word[::-1]
    return {
        "mot": word,
        "est_palindrome":  f"{word} est un palindrome." if is_palindrome else f"{word} n'est pas un palindrome."
    }
