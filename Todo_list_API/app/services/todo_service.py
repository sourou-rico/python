import logging
from typing import List, Optional
from app.models.todo_model import Todo, TodoCreate, TodoUpdate
from fastapi import HTTPException, status
from app.database.database import read_db, write_db, find_data

logger = logging.getLogger(__name__)

def get_all_todos() -> List[Todo]:
    """
    Récupère toutes les tâches.
    """
    try:
        todos = []
        for item in read_db():
            todos.append(Todo(**item))
        return todos

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des tâches: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erreur serveur"
            )


def create_todo(todo: TodoCreate) -> Todo:
    """ Crée une tâche"""
    try: 
        todos= read_db()
        new_todo = Todo(**todo.model_dump())
        todos.append(dict(new_todo))

        write_db(todos)

        return new_todo
    
    except Exception as e:
        logger.error(f"Erreur lors de la création de la tâche: {e}")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Erreur lors de la création d'une tâche"
        )
    
def update_todo(todo_uuid: str, todo_update: TodoUpdate) -> Optional[Todo]:
    """ Met à jour une tâche """
    try: 
        todos  = read_db()
        for index, item in enumerate(todos):
            if item['uuid'] == todo_uuid: 
                update_data = todo_update.model_dump(exclude_unset=True)
                updated_todo = {**item, **update_data}
                todos[index]= updated_todo

                write_db(todos)

                return Todo(**updated_todo)
            return None
    except Exception as e: 
        logger.error(f"Erreur lors de la mise à jour d'une tâche: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Erreur lors de la création d'une tâche"
        )
    
def delete_todo(todo_uuid: str) -> bool: 
    """ Supprimer une tâche """
    
    try:
        todos = read_db()
        new_todos = []

        for item in todos:
            if item['uuid'] != todo_uuid:
                new_todos.append(item)

            todos= new_todos
            write_db(todos)

            return True
    except Exception as e: 
        logger.error(f"Erreur lors de la suppression d'une tâche: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Erreur lors de la création d'une tâche"
        )