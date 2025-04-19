# Architecture des Agents pour Athly

## Vue d'Ensemble

L'architecture backend d'Athly est construite autour d'un système d'agents LangChain qui collaborent pour générer des programmes d'entraînement personnalisés. Cette approche modulaire permet une grande flexibilité et une capacité à évoluer selon les besoins.

```
┌─────────────────────────────────────┐
│           Agent Orchestrateur       │
└───────────────┬─────────────────────┘
                │
    ┌───────────┴───────────────┐
    │                           │
┌───▼───────────┐      ┌────────▼────────┐
│ Agent Expert   │      │  Agent Codeur   │
│ en Sport      │      │  de Tables      │
└───┬───────────┘      └────────┬────────┘
    │                           │
    │       ┌───────────┐       │
    └───────► Base de   ◄───────┘
            │ Connaissances│
            └───────────┘
```

## Agents et Leurs Rôles

### 1. Agent Orchestrateur

**Rôle principal**: Coordonner le flux de travail entre les différents agents spécialisés.

**Fonctionnalités**:
- Interprète les requêtes initiales des utilisateurs
- Détermine quels agents spécialisés appeler
- Gère la séquence des opérations
- Assemble les résultats finaux
- Maintient le contexte de la conversation

**Implémentation**:
```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool

class OrchestratorAgent:
    def __init__(self, llm, tools, memory=None):
        self.llm = llm
        self.tools = [
            Tool(name="expert_sport", func=self.call_sport_expert, description="..."),
            Tool(name="table_generator", func=self.call_table_generator, description="..."),
            # Autres outils
        ]
        self.memory = memory
        self.agent = create_openai_tools_agent(llm, self.tools, base_prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, memory=self.memory)
        
    def process_query(self, query):
        return self.executor.invoke({"input": query})
```

### 2. Agent Expert en Sport

**Rôle principal**: Fournir les connaissances spécialisées en programmation d'entraînement.

**Fonctionnalités**:
- Génère les structures de programmation adaptées à chaque discipline
- Adapte les recommandations au niveau de l'utilisateur
- Fournit des conseils techniques sur les exercices
- Définit la progression optimale sur la durée sélectionnée

**Implémentation**:
```python
class SportExpertAgent:
    def __init__(self, llm, knowledge_base):
        self.llm = llm
        self.knowledge_base = knowledge_base
        self.prompt_template = self._load_sport_expert_prompt()
        
    def generate_program_structure(self, discipline, duration, level, goals):
        context = self.knowledge_base.query(f"programming {discipline} {level}")
        prompt = self.prompt_template.format(
            discipline=discipline,
            duration=duration,
            level=level,
            goals=goals,
            context=context
        )
        return self.llm.invoke(prompt)
```

### 3. Agent Codeur de Tables

**Rôle principal**: Structurer les données d'entraînement en formats visuellement exploitables.

**Fonctionnalités**:
- Génère des tableaux pour les programmes d'entraînement
- Formate les données pour l'affichage frontend
- Crée des visualisations de la progression
- Produit des templates pour export PDF/calendrier

**Implémentation**:
```python
class TableGeneratorAgent:
    def __init__(self, llm):
        self.llm = llm
        self.templates = self._load_table_templates()
        
    def generate_training_table(self, program_data, format_type="markdown"):
        template = self.templates[format_type]
        prompt = f"""
        Utilise les données suivantes pour générer un tableau {format_type} bien structuré:
        {program_data}
        
        Format attendu:
        {template}
        """
        return self.llm.invoke(prompt)
```

## Base de Connaissances

La base de connaissances sert de référentiel pour les informations spécialisées sur:
- Les méthodologies d'entraînement par discipline
- Les exercices et leurs variantes
- Les principes de périodisation
- Les techniques de progression

**Implémentation**:
```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

class KnowledgeBase:
    def __init__(self, embedding_model=None):
        self.embedding_model = embedding_model or OpenAIEmbeddings()
        self.vector_db = self._initialize_db()
        
    def query(self, query_text, n_results=5):
        return self.vector_db.similarity_search(query_text, k=n_results)
        
    def _initialize_db(self):
        # Charge les données d'exercices, méthodologies, etc.
        return Chroma(embedding_function=self.embedding_model)
```

## Intégration avec l'API

L'architecture des agents est exposée via une API FastAPI qui gère:
- L'authentification des utilisateurs
- La validation des requêtes
- La mise en cache des réponses fréquentes
- Le suivi des utilisateurs et leurs programmes

```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

class ProgramRequest(BaseModel):
    disciplines: list[str]
    duration: int
    level: str
    goals: str
    constraints: str = ""
    equipment: str = ""
    frequency: int
    time_per_session: int

@app.post("/api/generate-program")
async def generate_program(request: ProgramRequest):
    orchestrator = get_orchestrator()
    program = orchestrator.process_query(request.dict())
    return {"program": program}
```

## Pipeline de Traitement

1. L'utilisateur saisit ses préférences via l'interface frontend
2. L'Agent Orchestrateur reçoit la requête et détermine la stratégie
3. L'Agent Expert en Sport élabore la structure du programme
4. L'Agent Codeur de Tables formate les données pour l'affichage
5. Le résultat est renvoyé à l'utilisateur via l'API
6. Les interactions sont enregistrées pour améliorer les recommandations futures 