# backend/app/services/seeder.py
from datetime import datetime, timezone
import logging
from pymongo.database import Database
import uuid
from app.utils.generate_uuid import generate_strong_uuid
import json
from app.services.deepseek import openrouter_models_seed, openai_models_seed
from app.services.stt_models_seed import stt_models_seed
from app.services.tts_models_seed import tts_models_seed
from enum import Enum

with open("app/data/countries.json", "r", encoding="utf-8") as f:
    COUNTRY_DATA = json.load(f)

with open("app/data/timezones.json", "r", encoding="utf-8") as f:
    TIMEZONE_DATA = json.load(f)

logger = logging.getLogger(__name__)


class Status(str, Enum):
    ACTIVE = "Actif"
    INACTIVE = "Inactif"



async def seed_initial_data(db: Database):
    logger.info("Seeding initial data")

    await seed_assistants(db)
    await seed_roles(db)
    await seed_users(db)
    await seed_planning(db)
    await seed_countries(db)
    await seed_timezones(db)
    await seed_openrouter_models(db)
    await seed_openai_models(db)
    await seed_stt_models(db)
    await seed_tts_models(db)
    await seed_auth_ldap(db)
    await seed_prospects(db)
    # await seed_client_datas(db)
    # await seed_system_registries(db)
    # await seed_ari_events(db)
    # await seed_call_history(db)
    # await seed_tempory_process(db)
    # await seed_calling_hours(db)

    logger.info("Seeding completed")


async def seed_roles(db: Database):
    roles = [
        {
            "uuid": "role-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
            "name": "Admin",
            "description": "Administrateur système",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
    ]
    for role in roles:
        existent = await db.roles.find_one({"name": role["name"]})
        if not existent:
            await db.roles.insert_one(role)


async def seed_users(db: Database):
    users = [
        {
            "uuid": generate_strong_uuid("user"),
            "auth_type": "ldap",
            "ldap_login": "admin.admin",
            "role": "role-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
            "email": None,
            "is_active": True,
            "is_verified": True,
            "firstName": "Admin",
            "lastName": "System",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
    ]
    for user in users:
        if not await db.users.find_one({"email": user["email"]}):
            await db.users.insert_one(user)


async def seed_auth_ldap(db: Database):
    AppAuth = [
        {
            "id": 1,
            "uuid": generate_strong_uuid("ldap_config"),
            "name": "CHEM_AUTHENTICATION",
            "host": "chem.loc",
            "base_dn": "DC=chem,DC=loc",
            "bind_dn": "CHEM",
            "port": 389,
            "bind_password": "gAAAAABoK0Yypfad0F_1CL0EEP32GQNpbThGKoKUXN6XR-3kLcHameYTGi13uCRvtEiEIo_o1_pno_bdFjTklAftfqgqWrr4Zqi2KIo92_rshwJuFWtGclQ=",
            "description": "serveur ldap principal",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
    ]
    for auth in AppAuth:
        if not await db.ldap_configs.find_one({"name": auth["name"]}):
            await db.ldap_configs.insert_one(auth)


async def seed_calling_hours(db):
    assistants = await db.assistants.find().to_list(length=100)

    if not assistants:
        return

    for assistant in assistants:
        existing = await db.calling_hours.find_one({"assistant_id": assistant["uuid"]})

        if not existing:
            default_schedule = [
                {
                    "day": "monday",
                    "enabled": True,
                    "ranges": [
                        {"startTime": "09:00", "endTime": "12:00"},
                        {"startTime": "14:00", "endTime": "18:00"},
                    ],
                },
                {
                    "day": "tuesday",
                    "enabled": True,
                    "ranges": [
                        {"startTime": "09:00", "endTime": "12:00"},
                        {"startTime": "14:00", "endTime": "18:00"},
                    ],
                },
                {
                    "day": "wednesday",
                    "enabled": True,
                    "ranges": [
                        {"startTime": "09:00", "endTime": "12:00"},
                        {"startTime": "14:00", "endTime": "18:00"},
                    ],
                },
                {
                    "day": "thursday",
                    "enabled": True,
                    "ranges": [
                        {"startTime": "09:00", "endTime": "12:00"},
                        {"startTime": "14:00", "endTime": "18:00"},
                    ],
                },
                {
                    "day": "friday",
                    "enabled": True,
                    "ranges": [
                        {"startTime": "09:00", "endTime": "12:00"},
                        {"startTime": "14:00", "endTime": "17:00"},
                    ],
                },
                {"day": "saturday", "enabled": False, "ranges": []},
                {"day": "sunday", "enabled": False, "ranges": []},
            ]

            calling_hours = {
                "uuid": generate_strong_uuid("calling_hour"),
                "assistant_id": assistant["uuid"],
                "callingHours": default_schedule,
                "created_at": datetime.now().astimezone(timezone.utc),
                "updated_at": datetime.now().astimezone(timezone.utc),
            }

            await db.calling_hours.insert_one(calling_hours)

async def seed_prospects(db: Database):
    Prospects = []
    statuses = [
        ("called", "Appel effectué"),
        ("confirmed", "Rendez-vous confirmé"),
        ("canceled", "Rendez-vous annulé"),
        ("pending", "En attente de confirmation"),
        ("no-answer", "Pas de réponse"),
        ("completed", "Rendez-vous terminé"),
    ]
    agences = [
        "Agence Paris Centre",
        "Agence Paris Nord",
        "Agence Paris Sud",
        "Agence Paris Est",
        "Agence Paris Ouest",
        "Agence La Défense",
    ]
    for idx, (status, desc) in enumerate(statuses):
        for i in range(2):
            Prospects.append({
                "uuid": generate_strong_uuid("prospect"),
                "assistant_id": "assistant-725ecda4afbbafd2e1fe17033ee51f13d50be59g",
                "full_name": f"Prospect {status.capitalize()} {i+1}",
                "phone_number": f"+33 6 00 00 0{idx}{i} 0{idx}{i}",
                "email": f"prospect_{status}_{i+1}@example.com",
                "identified_need": "Assurance auto",
                "source": "Landing page",
                "creation_contact": datetime(2025, 5, 1 + idx, 9, 45),
                "last_contact_date": datetime(2025, 5, 1 + idx, 9, 45),
                "appointment_date": datetime(2025, 5, 15 + idx, 10, 0),
                "duration_call": 0,
                "created_at": datetime(2025, 5, 1 + idx, 9, 45),
                "interaction_historique": [],
                "appointment_info": {
                    "name_appointment": f"Consultation {desc}",
                    "description_appointment": f"Client intéressé par une assurance ({desc.lower()})",
                    "date_appointment": datetime(2025, 5, 6 + idx, 10, 0),
                    "duration_appointment": 30,
                    "place": agences[idx % len(agences)],
                    "user_id": "user-f6c13375ff654f829e52daeeb880d741a58426ad",
                    "statut_call": status,
                }
            })
    # Ajout du prospect de test avec l'UUID imposé
    Prospects.append({
        "uuid": generate_strong_uuid("prospect"),
        "assistant_id": "assistant-725ecda4afbbafd2e1fe17033ee51f13d50be59g",
        "full_name": "Prospect Test UUID Fixe",
        "phone_number": "+33 6 12 34 56 78",
        "email": "prospect_test_uuid@example.com",
        "identified_need": "Test besoin",
        "source": "Test seed",
        "creation_contact": datetime(2025, 6, 1, 10, 0),
        "last_contact_date": datetime(2025, 6, 1, 10, 0),
        "appointment_date": datetime(2025, 6, 15, 11, 0),
        "duration_call": 0,
        "created_at": datetime(2025, 6, 1, 10, 0),
        "interaction_historique": [],
        "appointment_info": {
            "name_appointment": "Consultation Test",
            "description_appointment": "Prospect de test avec UUID fixe pour les tests.",
            "date_appointment": datetime(2025, 6, 6, 11, 0),
            "duration_appointment": 30,
            "place": "Agence Test",
            "user_id": "user-f6c13375ff654f829e52daeeb880d741a58426ad",
            "statut_call": "test",
        }
    })

    for Prospect in Prospects:
        if not await db.Prospects.find_one({"full_name": Prospect['full_name']}):
            await db.Prospects.insert_one(Prospect)
            logger.info(f"Information du prospect récupérée : {Prospect['full_name']}")



async def seed_client_datas(db: Database):
    client_datas_examples = [
        {
            "uuid": generate_strong_uuid("client_data"),
            "SheetId": "sheet-001",
            "NOM": "Dupont",
            "PRENOM": "Jean",
            "TELEPHONE": "0612345678",
            "ADRESSE_MAIL": "jean.dupont@example.com",
            "NOM_FICHIER": "injection_test_1.csv",
            "ACTIVITE": "Campagne Test Sortant",
            "ACTIVITE_ID": None,
            "ORIGINE": "Import CSV",
            "MANUEL_INJ": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "uuid": generate_strong_uuid("client_data"),
            "SheetId": "sheet-002",
            "NOM": "Martin",
            "PRENOM": "Sophie",
            "TELEPHONE": "0787654321",
            "ADRESSE_MAIL": "sophie.martin@example.com",
            "NOM_FICHIER": "injection_test_1.csv",
            "ACTIVITE": "Campagne Test Sortant",
            "ACTIVITE_ID": None,
            "ORIGINE": "Import CSV",
            "MANUEL_INJ": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
    ]
    for client_data_example in client_datas_examples:
        existing_client = await db.client_datas.find_one(
            {"TELEPHONE": client_data_example["TELEPHONE"]}
        )
        if not existing_client:
            await db.client_datas.insert_one(client_data_example)


async def seed_system_registries(db: Database):
    client_phones = ["0612345678", "0787654321"]
    clients = await db.client_datas.find({"TELEPHONE": {"$in": client_phones}}).to_list(
        None
    )

    system_registries_examples = []
    for client in clients:
        registry_data = {
            "uuid": generate_strong_uuid("system_registry"),
            "SheetId": client["SheetId"],
            "Activite_actuelle": client["ACTIVITE"],
            "Utilise_actuellement": 0,
            "Etat_fiche": "Fiche_vierge",
            "Priorite": 4,
            "Nbre_de_rappel": 0,
            "Total_Appel_Agent": 0,
            "Total_Appel": 0,
            "LimiteMaxAppel": 10,
            "Exclusion": 0,
            "Manuel_inj": client["MANUEL_INJ"],
            "Nom_fichier": client["NOM_FICHIER"],
            "Agent_indexe": "0",
            "Date_Creation": datetime.utcnow(),
        }
        system_registries_examples.append(registry_data)
    for registry_example in system_registries_examples:
        existing_registry = await db.system_registries.find_one(
            {"SheetId": registry_example["SheetId"]}
        )
        if not existing_registry:
            await db.system_registries.insert_one(registry_example)


async def seed_ari_events(db: Database):
    ari_events_examples = [
        {
            "uuid": generate_strong_uuid("ari_event"),
            "type": "ChannelCreated",
            "application": "voicebot",
            "timestamp": datetime.utcnow().isoformat(),
            "channel": {
                "id": "channel-123",
                "name": "SIP/voip-0001",
                "state": "Down",
                "caller": {"name": "0123456789", "number": "0123456789"},
                "dialplan": {"context": "from-internal", "exten": "1000"},
                "creationtime": datetime.utcnow().isoformat(),
            },
            "received_at": datetime.utcnow(),
            "event_id": str(uuid.uuid4()),
        },
        {
            "uuid": generate_strong_uuid("ari_event"),
            "type": "ChannelStateChange",
            "application": "voicebot",
            "timestamp": datetime.utcnow().isoformat(),
            "channel": {
                "id": "channel-123",
                "name": "SIP/voip-0001",
                "state": "Up",
                "caller": {"name": "0123456789", "number": "0123456789"},
            },
            "received_at": datetime.utcnow(),
            "event_id": str(uuid.uuid4()),
        },
    ]

    for event in ari_events_examples:
        existing_event = await db.ari_events.find_one({"event_id": event["event_id"]})
        if not existing_event:
            await db.ari_events.insert_one(event)


async def seed_call_history(db: Database):
    call_history_examples = [
        {
            "uuid": generate_strong_uuid("call_history"),
            "id_fiche": "fiche-001",
            "Activite_de_numerotation": "Campagne Test Sortant",
            "log_agent": "agent1",
            "Numero_appele": "0123456789",
            "Numero_appelant": "0987654321",
            "Nom_fichier": "test_campaign.csv",
            "sip_session_id": "session-123",
            "Id_de_l_appel": "call-123",
            "Duree_Appel": 120,
            "Date_d_appel": datetime.utcnow(),
            "qualification_recue": "Positive",
            "Type_qualification_recue": "Qualification_agent",
            "Heure_debut_appel": datetime.utcnow(),
            "Heure_fin_appel": datetime.utcnow(),
            "Raison_fin_appel": 1,
            "Appel_argumente": 1,
            "IncomingCallAnswered": "Decroche",
            "Appel_Type": "Out",
            "Etat_fiche": "Qualification_agent",
            "Etat_contact": "Qualification_agent",
            "temps_de_sonnerie": 5,
            "Temps_en_ligne": 115,
            "Temps_SVI_Sonnerie_Attente": 0,
            "Encodage": 1,
            "Decroche": 1,
            "Nbre_Tentatives": 1,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
    ]

    for call in call_history_examples:
        existing_call = await db.call_history.find_one(
            {"Id_de_l_appel": call["Id_de_l_appel"]}
        )
        if not existing_call:
            await db.call_history.insert_one(call)


async def seed_tempory_process(db: Database):
    tempory_process_examples = [
        {
            "uuid": generate_strong_uuid("tempory_process"),
            "SheetId": "sheet-001",
            "CIVILITE": "M",
            "NOM": "Dupont",
            "PRENOM": "Jean",
            "TELEPHONE": "0612345678",
            "CODE_POSTAL": "75001",
            "VILLE": "Paris",
            "NUMERO_DE_RUE": "1",
            "ADRESSE_1": "Rue de la Paix",
            "ADRESSE_2": None,
            "ADRESSE_MAIL": "jean.dupont@example.com",
            "NOM_FICHIER": "test_campaign.csv",
            "TAG_FICHIER": "test",
            "INFO_INJECTION": "Import test",
            "ACTIVITE": "Campagne Test Sortant",
            "ACTIVITE_ID": None,
            "AGENT_INDEXE": None,
            "ZONE": "Paris",
            "DATE_INJECTION": datetime.utcnow().isoformat(),
            "SEQUENCE_INJECTION": "1",
            "TELEPHONE_SECONDAIRE": None,
            "COMMENTAIRE": "Test commentaire",
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        }
    ]

    for process in tempory_process_examples:
        existing_process = await db.tempory_process.find_one(
            {"SheetId": process["SheetId"]}
        )
        if not existing_process:
            await db.tempory_process.insert_one(process)


async def seed_planning(db: Database):
    """
    Crée des plannings par défaut pour le système
    """
    planning_names = [
        "planning_alpha",
        "planning_beta",
        "planning_gamma",
        "planning_delta",
    ]

    default_schedule = [
        {
            "day": "monday",
            "enabled": True,
            "ranges": [
                {"startTime": "09:00", "endTime": "12:00"},
                {"startTime": "14:00", "endTime": "18:00"},
            ],
        },
        {
            "day": "tuesday",
            "enabled": True,
            "ranges": [
                {"startTime": "09:00", "endTime": "12:00"},
                {"startTime": "14:00", "endTime": "18:00"},
            ],
        },
        {
            "day": "wednesday",
            "enabled": True,
            "ranges": [
                {"startTime": "09:00", "endTime": "12:00"},
                {"startTime": "14:00", "endTime": "18:00"},
            ],
        },
        {
            "day": "thursday",
            "enabled": True,
            "ranges": [
                {"startTime": "09:00", "endTime": "12:00"},
                {"startTime": "14:00", "endTime": "18:00"},
            ],
        },
        {
            "day": "friday",
            "enabled": True,
            "ranges": [
                {"startTime": "09:00", "endTime": "12:00"},
                {"startTime": "14:00", "endTime": "17:00"},
            ],
        },
        {"day": "saturday", "enabled": False, "ranges": []},
        {"day": "sunday", "enabled": False, "ranges": []},
    ]

    for name in planning_names:
        existing = await db.plannings.find_one({"name": name})
        if not existing:
            planning = {
                "uuid": generate_strong_uuid("planning"),
                "name": name,
                "callingHours": default_schedule,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
            await db.plannings.insert_one(planning)
            logger.info(f"Planning {name} créé avec succès")


async def seed_countries(db: Database):
    try:
        for item in COUNTRY_DATA:
            item["uuid"] = generate_strong_uuid("country")
            existing = await db.countries.find_one(
                {
                    "code": item["code"],
                    "name": item["name"],
                }
            )
            if not existing:
                await db.countries.insert_one(item)

    except Exception as e:
        logger.error(f"Error during country seeding: {e}")


async def seed_timezones(db: Database):
    try:
        for item in TIMEZONE_DATA:
            cleaned_item = {
                "timezone_describ": item.get("timezone_describ"),
                "timezone_utc": item.get("timezone_utc"),
                "pays_id": item.get("pays_id"),
            }

            if "uuid" not in cleaned_item:
                cleaned_item["uuid"] = generate_strong_uuid("timezone")

            cleaned_item["created_at"] = datetime.utcnow()
            cleaned_item["updated_at"] = datetime.utcnow()

            existing = await db.timezones.find_one(
                {"timezone_describ": cleaned_item["timezone_describ"]}
            )
            if not existing:
                await db.timezones.insert_one(cleaned_item)

        logger.info("Timezone seeding completed.")
    except Exception as e:
        logger.error(f"Error during timezone seeding: {e}")


async def seed_openrouter_models(db: Database):
    logger.info("Seeding OpenRouter LLM models...")
    for model in openrouter_models_seed:
        model_to_upsert = dict(model)
        model_to_upsert["updated_at"] = datetime.utcnow()
        await db.ai_models.update_one(
            {"uuid": model["uuid"]},
            {"$set": model_to_upsert, "$setOnInsert": {"created_at": datetime.utcnow()}},
            upsert=True
        )
        logger.info(f"Upserted OpenRouter model: {model['model_name']} ({model['uuid']})")


async def seed_openai_models(db: Database):
    logger.info("Seeding OpenAI LLM models...")
    for model in openai_models_seed:
        model_to_upsert = dict(model)
        model_to_upsert["updated_at"] = datetime.utcnow()
        await db.ai_models.update_one(
            {"uuid": model["uuid"]},
            
            {"$set": model_to_upsert, "$setOnInsert": {"created_at": datetime.utcnow()}},
            upsert=True
        )
        logger.info(f"Upserted OpenAI model: {model['model_name']} ({model['uuid']})")


async def seed_stt_models(db: Database):
    logger.info("Seeding STT models (vosk, speechrecognition)...")
    for model in stt_models_seed:
        model_to_upsert = dict(model)
        model_to_upsert["updated_at"] = datetime.utcnow()
        await db.ai_models.update_one(
            {"uuid": model["uuid"]},
            {"$set": model_to_upsert, "$setOnInsert": {"created_at": datetime.utcnow()}},
            upsert=True
        )
        logger.info(f"Upserted STT model: {model['model_name']} ({model['uuid']})")


async def seed_tts_models(db: Database):
    logger.info("Seeding TTS models (ElevenLabs, etc)...")
    for model in tts_models_seed:
        model_to_upsert = dict(model)
        model_to_upsert["updated_at"] = datetime.utcnow()
        await db.ai_models.update_one(
            {"uuid": model["uuid"]},
            {"$set": model_to_upsert, "$setOnInsert": {"created_at": datetime.utcnow()}},
            upsert=True
        )
        logger.info(f"Upserted TTS model: {model['model_name']} ({model['uuid']})")


async def seed_assistants(db: Database):
    assistants = [
        {
            "uuid": generate_strong_uuid("assistant"),
            "name": "Assistant Free",
            "description": "Assistant spécialisé dans la gestion des ventes, le suivi client, et la prospection.",
            "prompt_language": "fr",
            "temperature": 0.7,
            "status": Status.ACTIVE,
            "welcomeMessage": """
                Bonjour, je suis l’agent virtuel de Free — je vous appelle pour vous faire découvrir une offre exclusive qui pourrait vraiment améliorer votre connexion et alléger votre facture.
            """,
            "systemPrompt": """
                🤖 FreeBot – Agent Virtuel de Free
                🧾 Identité et Objectifs
                Tu es FreeBot, l’agent virtuel officiel de Free, chargé de contacter des prospects par téléphone afin de :

                Proposer les offres de Free de manière proactive et personnalisée,

                Gérer et contourner les objections (clients déjà engagés, refus, manque de temps…),

                Créer un lien de confiance en posant des questions personnelles stratégiques (travail, famille, télétravail, loisirs numériques, etc.),

                Transférer l’appel à un expert humain si le client est intéressé,

                Ou proposer un rendez-vous téléphonique si le transfert n’est pas possible immédiatement.

                Ton objectif est de convertir un maximum de prospects en clients Free, tout en garantissant une expérience conversationnelle naturelle, engageante et respectueuse.

                🗣️ Ton et Personnalité
                Professionnel et rassurant : Tu inspires confiance dès les premières secondes.

                Chaleureux et engageant : Tu utilises une voix dynamique, mais calme et agréable.

                Curieux et humain : Tu poses des questions sur le quotidien du client pour mieux le comprendre.

                Stratégique et persuasif : Tu structures la discussion pour atteindre ton objectif sans forcer.

                Maîtrise du cadre : Tu ramènes la conversation à l’essentiel si elle s’égare ou traîne en longueur.

                🔄 Flux de Conversation
                1. Introduction
                "Bonjour, je suis l’agent virtuel de Free. Je vous appelle pour vous faire découvrir nos nouvelles offres très avantageuses pour votre logement. Est-ce que je vous dérange ?"

                Si oui → "Je comprends, je ne serai pas long, vous pourriez être agréablement surpris !"

                Si non → Passer à la découverte.

                2. Découverte et Création de Besoin
                "Vous êtes actuellement chez quel fournisseur d’accès à Internet ?"

                "Et vous trouvez que tout fonctionne bien chez eux, ou il y a parfois des lenteurs, coupures ?"

                "Et niveau prix, ça vous semble correct ou un peu cher pour ce que vous avez ?"

                🎯 Questions personnelles stratégiques
                "Vous travaillez depuis la maison parfois ?"

                "Il y a des enfants ou des ados à la maison ? Ils sont plutôt jeux vidéo ou streaming Netflix ?"

                "Vous êtes plutôt télétravail ou déplacements ?"

                👉 Ces questions permettent d’humaniser la conversation tout en préparant le terrain pour l’argumentaire.

                3. Proposition de l’Offre Free
                "Justement, Free propose en ce moment une offre fibre très haut débit à partir de [tarif], avec de nombreux avantages comme [Ex : box incluse, mobile + internet, sans engagement, débit garanti]."

                "Ce serait parfaitement adapté à votre usage, surtout avec [enfants / télétravail / streaming / besoin de stabilité]."

                🛑 Gestion des Objections (Barrages)
                Objection	Réponse Stratégique
                "Je suis déjà chez un autre opérateur."	"Beaucoup de clients que j’appelle le sont aussi, mais ils sont souvent surpris par les économies ou la qualité que Free peut leur offrir. Laissez-moi juste vous expliquer rapidement."
                "Je ne veux pas changer maintenant."	"C’est tout à fait compréhensible. Je ne vous demande pas de changer aujourd’hui, juste de voir si ça pourrait vous intéresser."
                "Ce n’est pas moi qui gère ça."	"Très bien. Est-ce que je peux prendre un rendez-vous avec la personne concernée ?"
                "Je n’ai pas le temps."	"Je comprends. Je peux vous rappeler plus tard dans la journée ou demain si c’est plus pratique ?"

                🎯 Relance stratégique / reformulation
                "Donc si je comprends bien, vous êtes chez [X], ça fonctionne plus ou moins, et vous êtes curieux de voir si Free peut proposer mieux. C’est bien ça ?"

                📞 Transfert ou Rendez-vous
                ✅ Si le client est intéressé :
                "Parfait ! Je vous transfère immédiatement à un expert Free pour finaliser l’échange."

                ❌ Si ce n’est pas possible :
                "Je vous propose un rendez-vous téléphonique avec l’un de nos experts Free."

                🕒 Proposition de créneaux :
                "Quel créneau vous conviendrait le mieux : demain à 10h30 ou demain à 16h ?"

                → Si aucun ne convient :

                "Pas de souci. Voici d'autres options : mercredi à 11h ou jeudi à 15h ?"

                ✅ Confirmation du Rendez-vous
                "Parfait, c’est noté pour [Jour] à [Heure]. Un expert Free vous appellera pour finaliser cela. Merci pour votre temps et à très bientôt !"

                ⚠️ Cas Particuliers à Gérer
                Situation	Réponse
                Le client veut réfléchir.	"Bien sûr. Je peux vous envoyer les infos par SMS ou email, et prévoir un rappel à un moment qui vous arrange ?"
                Le client veut reporter.	"Très bien, je vous propose un rendez-vous la semaine prochaine. Quel jour vous conviendrait ?"
                Le client est déjà chez Free.	"Super ! Et si je vous parlais des nouveautés ou évolutions de Free ? Peut-être êtes-vous éligible à une meilleure offre."

                ⚙️ Automatisations et Intégrations
                Déclenchement automatique de l’appel après qualification.

                Reconnaissance vocale avec barge-in.

                Enregistrement des réponses dans le CRM.

                Prise de rendez-vous synchronisée avec Google Calendar ou autre.

                Envoi automatique de la confirmation et du rappel du RDV.

                📊 Suivi et Reporting
                Nombre d’appels / taux de contact.

                Taux d’intérêt / taux de transfert / taux de rendez-vous.

                Statistiques sur les objections courantes.

                Taux de conversion par typologie de profil prospect.

                Raison des refus catégorisées.

                Dashboard de pilotage en temps réel.

                🎯 Mission Principale
                Transformer un maximum de prospects en clients Free, en instaurant confiance, empathie et stratégie, pour vendre intelligemment à travers une conversation naturelle et humaine.
                Finaliser chaque interaction par un transfert immédiat ou une prise de rendez-vous qualifiée.
            """,
            "created_at": datetime.now().astimezone(timezone.utc),
            "updated_at": datetime.now().astimezone(timezone.utc)
        },
        {
            "uuid": generate_strong_uuid("assistant"),
            "name": "Assistant Support Technique",
            "description": "Assistant dédié à l'assistance technique et au dépannage utilisateur",
            "prompt_language": "fr",
            "temperature": 0.5,
            "status": Status.INACTIVE,
            "welcomeMessage": "Bonjour, je suis votre assistant support technique. Décrivez-moi votre problème et je "
                              "vais vous aider pas à pas pour résoudre votre difficulté. Êtes-vous prêt à me donner "
                              "plus de détails ?",
            "systemPrompt": "Vous êtes un assistant de support technique spécialisé dans le dépannage informatique, "
                            "logiciel, et téléphonique. Votre objectif est d'aider les utilisateurs à résoudre leurs "
                            "problèmes rapidement et efficacement. Posez des questions claires pour identifier la "
                            "source du problème, proposez des solutions étape par étape, et soyez patient avec les "
                            "utilisateurs moins technophiles. Expliquez les procédures sans jargon inutile. Si le "
                            "problème dépasse vos compétences, guidez l'utilisateur vers les bonnes ressources ou "
                            "vers le service technique humain. Soyez calme, méthodique et rassurant dans vos réponses.",
            "created_at": datetime.now().astimezone(timezone.utc),
            "updated_at": datetime.now().astimezone(timezone.utc)
        }
    ]

    for assistant in assistants:
        if not await db.assistants.find_one({"name": assistant["name"]}):
            await db.assistants.insert_one(assistant)
