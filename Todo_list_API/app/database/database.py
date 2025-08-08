from typing import List, Dict, Optional
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

## Logging est le module standard de Python pour la journalisation

## logger.debug("Ceci est un message de debug")
## logger.info("Operation réussie")
## logger.warning("Attention, quelque chose est bizarre")
## logger.error("Une erreur est survenue")


## Configuration du chemin de la base de données
DB_PATH = Path(__file__).parent / "db.json" ## database/db.json


def read_db() -> List[Dict]:
    """ Fonction permettant de lire la base de données."""
    try:
        ## Vérifier si le fichier db.json existe
        if not DB_PATH.exists():
            return []
        
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Erreur de décodage JSON {e}")
        return []
    except Exception as e:
        logger.error(f"Erreur innatendue {e}")
        raise 

def write_db(data: List[Dict]):
    """ Permet d'écrire dans la base de données."""
    try:
        if not verified_db_exists():
            return []
        
        with open(DB_PATH, "w", encoding="utf-8") as f:
            return json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        logger.error(f"Erreur d'écriture {e}")
        raise
    except Exception as e:
        logger.error(f"Erreur innatendue {e}")
        raise

## Fonction pour trouver une donnée par son ID
def find_data(data_id: str) -> Optional[Dict]:
    """ Trouver une tâche par son ID."""
    try: 
        todos = read_db()
        # for todo in todos:
        #     if todo["uuid"] == data_id:
        #         return todo
        # return None
        return next((todo for todo in todos if todo["uuid"] == data_id), None)
    except Exception as e:
        logger.error(f"Erreur innatendue {e}")
        raise

## Vérifie si la base de données existe
def verified_db_exists() -> bool:
    """ Vérifie si la base de données existe."""
    if not DB_PATH.exists():
        return False
    return True

    
