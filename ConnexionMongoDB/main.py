import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.mongo import connect_to_mongo, close_mongo_connection, get_db
from app.api.v1.routes.__init__ import include_routers
from app.services.seeder_service import seed_initial_data
from app.core.settings import (
    APP_NAME, APP_DESCRIPTION, API_VERSION,
    OPENAPI_URL, DOCS_URL, REDOC_URL
)
from app.services.audio_text_service import audio_text_service
from app.core.logging import setup_logger


load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


logger = setup_logger("main")

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=API_VERSION,
    openapi_url=OPENAPI_URL,
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

include_routers(app)

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API VoiceBot"}

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo(app)
    db = app.state.db
    # await audio_text_service.initialize()
    await seed_initial_data(db)

# Événement déclenché automatiquement à l’arrêt de l’application
@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

if __name__ == "__main__":
    import uvicorn
    print("📚 Docs: http://localhost:8000/api/docs/v1_0_0")
    print("📬 Redoc: http://localhost:8000/api/redoc/v1_0_0")
    print("🔌 OpenAPI: http://localhost:8000/api/openapi.json")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )

