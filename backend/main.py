from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv

from agents.orchestrator import OrchestratorAgent
from agents.expert import SportExpertAgent
from agents.table_generator import TableGeneratorAgent
from models.knowledge_base import KnowledgeBase

# Chargement des variables d'environnement
load_dotenv()

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
    
    llm = ChatMistralAI(
        temperature=0.7,
        model_name="mistral-large-latest", 
        mistral_api_key=os.getenv("MISTRAL_API_KEY")
    )
    
    # Initialisation des composants
    knowledge_base = KnowledgeBase()
    sport_expert = SportExpertAgent(llm, knowledge_base)
    table_generator = TableGeneratorAgent(llm)
    
    # Création de l'orchestrateur
    orchestrator = OrchestratorAgent(
        llm=llm, 
        sport_expert=sport_expert, 
        table_generator=table_generator
    )
    
    return orchestrator

# Routes API
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Athly - Votre coach sportif IA personnel"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, orchestrator: OrchestratorAgent = Depends(get_orchestrator)):
    try:
        # Traitement du message par l'orchestrateur
        response = orchestrator.process_chat(message.message)
        return ChatResponse(message=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de traitement: {str(e)}")

@app.post("/api/generate-program", response_model=ProgramResponse)
async def generate_program(request: ProgramRequest, orchestrator: OrchestratorAgent = Depends(get_orchestrator)):
    try:
        # Validation des entrées
        if len(request.disciplines) == 0:
            raise HTTPException(status_code=400, detail="Au moins une discipline doit être sélectionnée")
        
        if request.duration < 8 or request.duration > 16:
            raise HTTPException(status_code=400, detail="La durée doit être entre 8 et 16 semaines")
        
        # Génération du programme d'entraînement
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
        
        return ProgramResponse(program=program)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de génération: {str(e)}")

# Point d'entrée pour exécuter l'application directement
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 