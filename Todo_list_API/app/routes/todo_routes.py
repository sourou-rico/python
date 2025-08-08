# app/routes/todo_routes.py

from fastapi import APIRouter, HTTPException
from typing import List
from app.models.todo_model import Todo, TodoCreate, TodoUpdate
from app.services import todo_service

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

@router.get("/", response_model=List[Todo])
def get_todos():
    """Récupérer toutes les tâches"""
    return todo_service.get_all_todos()

@router.post("/", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate):
    """Créer une nouvelle tâche"""
    return todo_service.create_todo(todo)

@router.put("/{todo_uuid}", response_model=Todo)
def update_todo(todo_uuid: str, todo_update: TodoUpdate):
    """Mettre à jour une tâche"""
    updated = todo_service.update_todo(todo_uuid, todo_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return updated

@router.delete("/{todo_uuid}", response_model=dict)
def delete_todo(todo_uuid: str):
    """Supprimer une tâche"""
    deleted = todo_service.delete_todo(todo_uuid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return {"message": "Tâche supprimée avec succès"}
