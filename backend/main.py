from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import logging
import traceback
import json
from dotenv import load_dotenv

from agents.orchestrator import OrchestratorAgent
from agents.expert import SportExpertAgent
from agents.table_generator import TableGeneratorAgent
from models.knowledge_base import KnowledgeBase

# Création du répertoire de logs s'il n'existe pas
os.makedirs("logs", exist_ok=True)

# Configuration des logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("athly")

# Chargement des variables d'environnement
load_dotenv()
logger.info("Variables d'environnement chargées")

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Athly API",
    description="API pour l'application de coaching sportif Athly",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les origines exactes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("Configuration CORS appliquée")

# Modèles de données pour les requêtes et réponses
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    message: str

class ProgramRequest(BaseModel):
    disciplines: List[str]
    duration: int
    level: str
    goals: str
    constraints: Optional[str] = ""
    equipment: Optional[str] = ""
    frequency: int
    time_per_session: int

class ProgramResponse(BaseModel):
    program: str

# Dépendances pour l'injection
def get_orchestrator():
    # Initialisation du LLM
    from langchain.chat_models import ChatMistralAI
    
    try:
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            logger.error("MISTRAL_API_KEY non définie dans les variables d'environnement")
            raise ValueError("MISTRAL_API_KEY non définie dans les variables d'environnement")
        
        logger.debug(f"Initialisation de ChatMistralAI avec la clé API: {api_key[:5]}...")
        
        llm = ChatMistralAI(
            temperature=0.4,
            model_name="mistral-large-latest", 
            mistral_api_key=api_key,
            max_tokens=1024
        )
        
        # Initialisation des composants
        logger.info("Initialisation de la base de connaissances")
        knowledge_base = KnowledgeBase()
        
        logger.info("Initialisation de l'agent expert sportif")
        sport_expert = SportExpertAgent(llm, knowledge_base)
        
        logger.info("Initialisation du générateur de tableaux")
        table_generator = TableGeneratorAgent(llm)
        
        # Création de l'orchestrateur
        logger.info("Création de l'agent orchestrateur")
        orchestrator = OrchestratorAgent(
            llm=llm, 
            sport_expert=sport_expert, 
            table_generator=table_generator
        )
        
        return orchestrator
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de l'orchestrateur: {str(e)}")
        logger.error(traceback.format_exc())
        raise

# Routes API
@app.get("/")
def read_root():
    logger.info("Accès à la route racine")
    return {"message": "Bienvenue sur l'API Athly - Votre coach sportif IA personnel"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, orchestrator: OrchestratorAgent = Depends(get_orchestrator)):
    try:
        logger.info(f"Requête de chat reçue: {message.message[:50]}...")
        
        # Log du message complet en debug
        logger.debug(f"Message complet: {message.message}")
        
        # Traitement du message par l'orchestrateur
        logger.info("Transmission du message à l'orchestrateur")
        response = orchestrator.process_chat(message.message)
        
        logger.info(f"Réponse générée: {response[:50]}...")
        logger.debug(f"Réponse complète: {response}")
        
        return ChatResponse(message=response)
    except Exception as e:
        error_msg = f"Erreur de traitement du chat: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/api/generate-program", response_model=ProgramResponse)
async def generate_program(request: ProgramRequest, orchestrator: OrchestratorAgent = Depends(get_orchestrator)):
    try:
        # Validation des entrées
        if len(request.disciplines) == 0:
            logger.warning("Tentative de génération de programme sans discipline sélectionnée")
            raise HTTPException(status_code=400, detail="Au moins une discipline doit être sélectionnée")
        
        if request.duration < 8 or request.duration > 16:
            logger.warning(f"Durée de programme invalide: {request.duration} semaines")
            raise HTTPException(status_code=400, detail="La durée doit être entre 8 et 16 semaines")
        
        # Log des données de la requête
        logger.info(f"Demande de génération de programme: {request.disciplines}, niveau {request.level}, {request.duration} semaines")
        logger.debug(f"Données complètes de la requête: {json.dumps(request.dict(), ensure_ascii=False)}")
        
        # Génération du programme d'entraînement
        logger.info("Transmission de la demande à l'orchestrateur")
        program = orchestrator.generate_training_program(
            disciplines=request.disciplines,
            duration=request.duration,
            level=request.level,
            goals=request.goals,
            constraints=request.constraints,
            equipment=request.equipment,
            frequency=request.frequency,
            time_per_session=request.time_per_session
        )
        
        logger.info(f"Programme généré: {len(program)} caractères")
        logger.debug(f"Début du programme généré: {program[:200]}...")
        
        return ProgramResponse(program=program)
    except HTTPException as he:
        # Relancer les exceptions HTTP
        logger.error(f"Erreur HTTP: {he.detail}")
        raise
    except Exception as e:
        error_msg = f"Erreur de génération de programme: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)

# Gestionnaire d'erreurs pour l'application
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Exception non gérée: {str(exc)}")
    logger.error(traceback.format_exc())
    return {"detail": f"Une erreur interne s'est produite: {str(exc)}"}

# Point d'entrée pour exécuter l'application directement
if __name__ == "__main__":
    logger.info("Démarrage du serveur Athly API")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 