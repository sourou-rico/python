from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4

class TodoBase(BaseModel):
    """Modèle de base pour les tâches Todo."""
    title: str = Field(..., min_length=1, max_length=100) # le ... est pour champs requis
    description: Optional[str] = Field(None, max_length=500)

class TodoCreate(TodoBase):
    """Modèle pour la création des tâches Todo."""
    pass

class TodoUpdate(BaseModel):
    """Modèle pour la mise à jour des tâches Todo."""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

# Modèle complet de tâche Todo avec UUID
class Todo(TodoBase):
    """Modèle complet de tâche Todo."""
    uuid: str = Field(default_factory=lambda: str(uuid4()))

    class Config:
        schema_extra = {
            "example": {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Faire les courses",
                "description": "Acheter du lait et des oeufs"
            }
        }
