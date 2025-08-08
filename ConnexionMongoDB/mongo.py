from math import log
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.core.config import settings
from dotenv import load_dotenv
from app.core.logging import setup_logger
from fastapi import Request
import os
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import asyncio
logger = setup_logger(__name__)

client = None
db = None
db_instance = None
admin_db_instance = None
highfive_db_instance = None
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "voicebot")
ADMIN_DB_NAME = os.getenv("ADMIN_DB_NAME", "vdial_admin_db")
HIGHFIVE_DB_NAME = os.getenv("HIGHFIVE_DB_NAME", "vdial_HIFIVE_FIRST_test67ae6a3e42099s")

# Nombre maximum de tentatives de connexion
MAX_RETRY_ATTEMPTS = 5 
# Délai en secondes entre chaque tentative
RETRY_DELAY = 2 

async def connect_to_mongo(app):
    """
    Fonction appelée au démarrage de l'application pour initialiser
    la connexion asynchrone à MongoDB et stocker le client et la DB dans app.state.
    """
    global client, db, admin_db_instance
    client = AsyncIOMotorClient(settings.MONGO_URI)
    logger.info(f"URI de connexion MongoDB: {settings.MONGO_URI}")

    try:
        logger.info("Connexion à MongoDB en cours...")
        await client.admin.command('ping')
        logger.info("Connexion à MongoDB établie")
    except Exception as e:
        logger.error(f"Erreur connexion MongoDB: {e}")
        raise

    db = client[settings.DATABASE_NAME]
    admin_db_instance = client[settings.ADMIN_DATABASE_NAME]

    app.state.db_client = client
    app.state.db = db
    app.state.admin_db = admin_db_instance

async def close_mongo_connection():
    """
    Fonction appelée à l'arrêt de l'application pour fermer la connexion MongoDB proprement.
    """
    global client
    if client:
        logger.info("Fermeture de la connexion MongoDB...")
        client.close()
        logger.info("Connexion MongoDB fermée")
        

async def connect_to_mongo_with_retry():

    global client, db_instance, admin_db_instance, highfive_db_instance
    
    # Boucle de retry avec le nombre maximum de tentatives
    for attempt in range(MAX_RETRY_ATTEMPTS):
        try:
            # Log de la tentative en cours
            logger.info(f"Tentative de connexion MongoDB #{attempt + 1}/{MAX_RETRY_ATTEMPTS}")
            
            # Création du client MongoDB asynchrone
            client = AsyncIOMotorClient(MONGO_URI)
            
            # Test de la connexion avec un ping vers la base admin
            await client.admin.command('ping')
            
            # Initialisation des connexions aux différentes bases de données
            db_instance = client[DB_NAME]
            admin_db_instance = client[ADMIN_DB_NAME]  
            highfive_db_instance = client[HIGHFIVE_DB_NAME]
            
            # Log des connexions réussies
            logger.info(f"Connexion réussie à la base de données principale: {DB_NAME}")
            logger.info(f"Connexion réussie à la base de données admin: {ADMIN_DB_NAME}")
            logger.info(f"Connexion réussie à la base de données highfive: {HIGHFIVE_DB_NAME}")
            
            return db_instance
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            # Gestion des erreurs de connexion spécifiques à MongoDB
            error_msg = f"Erreur de connexion MongoDB (tentative {attempt + 1}/{MAX_RETRY_ATTEMPTS}): {str(e)}"
            logger.error(error_msg)
            
            # Si ce n'est pas la dernière tentative, on attend et on réessaie
            if attempt < MAX_RETRY_ATTEMPTS - 1:
                logger.info(f"Réessai dans {RETRY_DELAY} secondes...")
                await asyncio.sleep(RETRY_DELAY)
            else:
                # Si toutes les tentatives ont échoué, on lève une exception
                logger.error("Nombre maximum de tentatives atteint. Impossible de se connecter à MongoDB.")
                raise RuntimeError(f"Échec de connexion MongoDB après {MAX_RETRY_ATTEMPTS} tentatives: {str(e)}")
        
        except Exception as e:
            # Gestion des erreurs inattendues (non liées à la connexion)
            error_msg = f"Erreur inattendue lors de la connexion MongoDB: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

def get_db(request: Request):
    """
    Récupère la base de données MongoDB stockée dans app.state.
    """
    
    db = request.app.state.db
    if db is None:
        raise RuntimeError("La base de données n'est pas encore initialisée")
    return db

async def get_db_instance():
    global db_instance
    if db_instance is None:
        # Si l'instance n'existe pas, on établit la connexion avec retry
        db_instance = await connect_to_mongo_with_retry()
    return db_instance

async def get_admin_db():
    global admin_db_instance
    if admin_db_instance is None:
        # Si l'instance n'existe pas, on établit la connexion avec retry
        await connect_to_mongo_with_retry()
    return admin_db_instance

async def get_highfive_db():
    global highfive_db_instance
    if highfive_db_instance is None:
        # Si l'instance n'existe pas, on établit la connexion avec retry
        await connect_to_mongo_with_retry()
    return highfive_db_instance
