from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import logging
import traceback
import json
from fastapi import Request
from datetime import datetime
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

# Monter le répertoire static pour servir les fichiers statiques (comme test.html)
os.makedirs("static", exist_ok=True)  # Crée le répertoire s'il n'existe pas
app.mount("/static", StaticFiles(directory="static"), name="static")

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

class ProgramQuery(BaseModel):
    discipline: Optional[str] = None
    level: Optional[str] = None
    duration: Optional[int] = None

class ProgramListResponse(BaseModel):
    programs: List[str]

class ProgramDetailResponse(BaseModel):
    title: str
    content: str

# Programme Data Manager
program_data_manager = None

def get_program_manager():
    global program_data_manager
    if program_data_manager is None:
        from models.program_data import ProgramDataManager
        logger.info("Initialisation du gestionnaire de programmes")
        program_data_manager = ProgramDataManager()
    return program_data_manager

# Dépendances pour l'injection
def get_orchestrator():
    # Initialisation du LLM
    from langchain_mistralai import ChatMistralAI
    
    try:
        print("INITIALISATION DE L'ORCHESTRATEUR")
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            logger.error("MISTRAL_API_KEY non définie dans les variables d'environnement")
            raise ValueError("MISTRAL_API_KEY non définie dans les variables d'environnement")
        
        logger.debug(f"Initialisation de ChatMistralAI avec la clé API: {api_key[:5]}...")
        
        llm = ChatMistralAI(
            temperature=0.3,  # Température réduite pour moins d'hallucinations
            model_name="mistral-large-latest", 
            mistral_api_key=api_key,
            max_tokens=1024,
            timeout=300       # 5 minutes de timeout pour l'API
        )
        
        # Testez directement le LLM avant de l'utiliser dans les agents
        try:
            test_response = llm.invoke("Ceci est un test. Réponds simplement par 'OK'.")
            print(f"TEST LLM: {test_response}")
        except Exception as e:
            logger.error(f"Test du LLM échoué: {str(e)}")
            # Continuer même si le test échoue

        # Initialisation des composants avec cache pour la base de connaissances
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

# Dépendances pour l'injection avec Hugging Face
def get_qwen_orchestrator():
    # Initialisation du LLM avec Hugging Face Inference
    from models.qwen_model import QwenLLM
    
    try:
        print("INITIALISATION DE L'ORCHESTRATEUR AVEC QWEN")
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            logger.error("HUGGINGFACE_API_KEY non définie dans les variables d'environnement")
            raise ValueError("HUGGINGFACE_API_KEY non définie dans les variables d'environnement")
        
        logger.debug(f"Initialisation de QwenLLM avec la clé API HF: {api_key[:5]}...")
        
        # Initialiser QwenLLM avec les paramètres appropriés
        llm = QwenLLM(
            model_name="Qwen/QwQ-32B",
            api_key=api_key,
            temperature=0.3,
            max_tokens=1500,
            timeout=120
        )
        
        # Test du modèle
        try:
            test_response = llm.invoke("Ceci est un test. Réponds simplement par 'OK'.")
            print(f"TEST QWEN LLM: {test_response}")
        except Exception as e:
            logger.error(f"Test du modèle Qwen échoué: {str(e)}")
            # Continuer même si le test échoue

        # Initialisation des composants avec cache pour la base de connaissances
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
        logger.error(f"Erreur lors de l'initialisation de l'orchestrateur Qwen: {str(e)}")
        logger.error(traceback.format_exc())
        raise

# Vérifier quel modèle utiliser
USE_QWEN = os.getenv("USE_QWEN", "false").lower() == "true"
logger.info(f"Utilisation du modèle Qwen: {USE_QWEN}")

# Routes API
@app.get("/")
def read_root():
    logger.info("Accès à la route racine")
    return {"message": "Bienvenue sur l'API Athly - Votre coach sportif IA personnel"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, orchestrator: OrchestratorAgent = Depends(get_qwen_orchestrator if USE_QWEN else get_orchestrator)):
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

@app.post("/api/test-chat")
async def test_chat(message: ChatMessage):
    """
    Route de test qui utilise directement l'API Mistral sans passer par les agents.
    """
    try:
        # Log avec print pour s'assurer que c'est visible
        print(f"TEST-CHAT: Message reçu: {message.message}")
        
        # Charger la clé API
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            print("TEST-CHAT: ERREUR - Clé API Mistral non trouvée")
            return {"message": "Erreur: Clé API Mistral non configurée"}
        
        # Initialiser directement le modèle
        from langchain_mistralai import ChatMistralAI
        llm = ChatMistralAI(
            temperature=0.4,
            model_name="mistral-large-latest", 
            mistral_api_key=api_key,
            max_tokens=1024
        )
        
        # Appel simple au LLM
        print("TEST-CHAT: Appel à l'API Mistral...")
        response = llm.invoke(f"Réponds très brièvement à cette question: {message.message}")
        print(f"TEST-CHAT: Réponse reçue: {response}")
        
        return {"message": str(response)}
    except Exception as e:
        print(f"TEST-CHAT: ERREUR - {type(e).__name__}: {str(e)}")
        import traceback
        print(f"TEST-CHAT: Traceback:\n{traceback.format_exc()}")
        return {"message": f"Erreur de test: {str(e)}"}

@app.post("/api/convert-to-excel")
async def convert_to_excel(request: Request):
    """Convertit un programme d'entraînement textuel en fichier Excel."""
    from fastapi.responses import Response
    from fastapi.responses import JSONResponse
    
    try:
        data = await request.json()
        content = data.get("content", "")
        
        if not content:
            return JSONResponse(
                status_code=400, 
                content={"error": "Contenu vide"}
            )
        
        # Import nécessaire
        import pandas as pd
        import io
        import re
        from datetime import datetime
        
        logger.info("Demande de conversion Excel reçue")
        
        # Extraction des données du programme
        lines = content.split("\n")
        
        # Extraire le titre
        title = "Programme d'entraînement"
        for line in lines:
            if "Programme Personnalisé" in line:
                title = line.strip()
                break
        
        # Chercher les tables dans le contenu
        tables = []
        current_table = []
        in_table = False
        week_title = ""
        
        for line in lines:
            # Détecter le début d'une semaine
            if line.strip().startswith("**Semaine"):
                week_title = line.strip().replace("*", "")
                in_table = False
                if current_table:
                    tables.append((week_title, current_table))
                    current_table = []
            
            # Détecter les lignes de tableau (contenant des |)
            if "|" in line and "----|" not in line:
                if not in_table:
                    in_table = True
                current_table.append(line)
            elif in_table and not line.strip():
                in_table = False
                if current_table:
                    tables.append((week_title, current_table))
                    current_table = []
        
        # Ajouter la dernière table si elle existe
        if current_table:
            tables.append((week_title, current_table))
        
        logger.debug(f"Nombre de tables trouvées: {len(tables)}")
        
        # Créer un fichier Excel en mémoire
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Feuille d'introduction
            introduction = "".join([line for line in lines if "###" in line or "Introduction" in line])
            intro_df = pd.DataFrame({"Introduction": [introduction]})
            intro_df.to_excel(writer, sheet_name="Introduction", index=False)
            
            # Formater la feuille d'introduction
            workbook = writer.book
            worksheet = writer.sheets["Introduction"]
            text_format = workbook.add_format({'text_wrap': True})
            worksheet.set_column('A:A', 80, text_format)
            
            # Ajouter chaque semaine dans une feuille séparée
            for i, (week_title, table_lines) in enumerate(tables):
                # Nettoyer les données du tableau
                headers = table_lines[0].strip().split("|")
                headers = [h.strip() for h in headers if h.strip()]
                
                rows = []
                for line in table_lines[1:]:
                    cols = line.strip().split("|")
                    cols = [c.strip() for c in cols if c.strip()]
                    if cols:
                        rows.append(cols)
                
                # Créer un DataFrame
                df = pd.DataFrame(rows, columns=headers)
                
                # Nommer la feuille (max 31 caractères pour Excel)
                sheet_name = f"Semaine {i+1}"
                if len(sheet_name) > 31:
                    sheet_name = sheet_name[:28] + "..."
                
                # Écrire dans la feuille
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Formater la feuille
                worksheet = writer.sheets[sheet_name]
                
                # Ajuster largeur des colonnes
                for idx, col in enumerate(df.columns):
                    max_len = max(
                        df[col].astype(str).map(len).max(),
                        len(col)
                    )
                    worksheet.set_column(idx, idx, max_len + 2)
                
                # Ajouter un format pour les cellules
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'fg_color': '#4F46E5',
                    'font_color': 'white',
                    'border': 1
                })
                
                cell_format = workbook.add_format({
                    'text_wrap': True,
                    'valign': 'top',
                    'border': 1
                })
                
                for row_num, (_, row) in enumerate(df.iterrows()):
                    for col_num, _ in enumerate(row):
                        worksheet.write(row_num + 1, col_num, df.iloc[row_num, col_num], cell_format)
                
                # Appliquer le format d'en-tête
                for col_num, col in enumerate(df.columns):
                    worksheet.write(0, col_num, col, header_format)
                
                # Figer la première ligne
                worksheet.freeze_panes(1, 0)
        
        # Renvoyer le fichier Excel
        output.seek(0)
        
        filename = f"programme_entrainement_{datetime.now().strftime('%Y%m%d')}.xlsx"
        logger.info(f"Fichier Excel généré: {filename}")
        
        return Response(
            content=output.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
    
    except Exception as e:
        logger.error(f"Erreur lors de la conversion en Excel: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": f"Erreur lors de la conversion: {str(e)}"}
        )

@app.post("/api/programs/list", response_model=ProgramListResponse)
async def list_programs(query: ProgramQuery = None):
    """
    Liste les programmes d'entraînement disponibles, avec filtrage optionnel.
    """
    try:
        manager = get_program_manager()
        
        if query and (query.discipline or query.level or query.duration):
            # Recherche avec critères
            programs_data = manager.search_program_by_criteria(
                discipline=query.discipline,
                level=query.level,
                duration=query.duration
            )
            # Extraire juste les noms de fichiers
            program_names = [p.get("filename") for p in programs_data]
        else:
            # Liste complète
            program_names = manager.get_available_programs()
        
        return ProgramListResponse(programs=program_names)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des programmes: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/api/programs/{program_name}", response_model=ProgramDetailResponse)
async def get_program_detail(program_name: str):
    """
    Récupère les détails d'un programme spécifique.
    """
    try:
        manager = get_program_manager()
        
        # Vérifier si le fichier existe
        available_programs = manager.get_available_programs()
        if program_name not in available_programs:
            raise HTTPException(status_code=404, detail=f"Programme '{program_name}' non trouvé")
        
        # Générer le résumé du programme
        summary = manager.get_program_summary(program_name)
        title = os.path.splitext(program_name)[0]
        
        return ProgramDetailResponse(title=title, content=summary)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des détails du programme: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

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