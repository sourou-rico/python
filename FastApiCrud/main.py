from fastapi import FastAPI
import json
import os
from typing import Optional
# Création de l'application FastAPI
app = FastAPI(
    title="FastAPI CRUD",
    description = "Application de creation, modification et suppression de taches",
    version = "1.0"

)

DATA_FILE = "data.json"
# Vérification de l'existence du fichier data.json
if not os.path.exists(DATA_FILE):
    # Création du fichier data.json s'il n'existe pas
    with open(DATA_FILE, "w") as file:
        json.dump([], file)  # Initialise le fichier avec une liste vide

# Route pour la page d'accueil de notre application
@app.get("/")
def welcome():
    """ Page d'accueil de l'API """
    return {"message": "Bienvenue sur mon API FastAPI CRUD"}

# Route pour la création d'une tâche enregistrée dans data.json
@app.post("/taches/")
def create_task(task: str):
    """ Méthode pour créer une nouvelle tâche """
    with open("data.json", "r") as file:
        tasks = json.load(file)
        # Genération d'un nouvel ID pour la tâche
        new_id = 1 if not tasks else tasks[-1]["id"] + 1
        # Création de la nouvelle tâche
        new_task = {"id": new_id, "task": task}
        tasks.append(new_task)
    with open("data.json", "w") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

    return {"message": f"Tâche '{task}' créée avec succès!"}

# Route pour la récupération de toutes les tâches
@app.get("/taches/")
def get_tasks():
    """ Méthode pour récupérer toutes les tâches """
    with open("data.json", "r") as file:
        tasks = json.load(file)
    return {"tasks": tasks}

# Route  pour le modification d'une tâche
@app.put("/taches/{task_id}")
def update_task(task_id: int, task : str):
    """ Méthode pour modifier une tâche existante """
    with open("data.json", "r") as file:
        tasks = json.load(file )
    # Recherche de la tâche à modifier et mise à jour
    for t in tasks:
        if t["id"] == task_id:
            t["task"] = task
            break
    else:
        return {"message": "Tâche non trouvée"}

    with open("data.json", "w") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

    return {"message": f"Tâche {task_id} mise à jour avec succès!"}

# Route pour la suppression d'une tâche
@app.delete("/taches/{task_id}")
def delete_task(task_id: int):
    """ Méthode pour supprimer une tâche """
    with open("data.json", "r") as file:
        tasks = json.load(file)
    # Filtrage des tâches pour exclure celle à supprimer
    tasks = [t for t in tasks if t["id"] != task_id]
    
    with open("data.json", "w") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

    return {"message": f"Tâche {task_id} supprimée avec succès!"}