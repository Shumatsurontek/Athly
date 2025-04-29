from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
import logging
import traceback
import time
import json
import os
from typing import List, Dict, Any, Optional
import re

from .expert import SportExpertAgent
from .table_generator import TableGeneratorAgent

# Imports LangChain
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts.chat import ChatPromptTemplate

# Import LangGraph
from langgraph.graph import StateGraph
try:
    from agents.agent_graph import AgentGraph
except ImportError:
    from .agent_graph import AgentGraph

# Obtention du logger
logger = logging.getLogger("athly.orchestrator")

class OrchestratorAgent:
    """
    Agent Orchestrateur qui coordonne le flux de travail entre les différents agents spécialisés.
    """
    
    def __init__(self, llm, sport_expert=None, table_generator=None):
        """
        Initialise l'agent orchestrateur.
        
        Args:
            llm: Le modèle de langage à utiliser
            sport_expert: L'agent expert en sport
            table_generator: L'agent générateur de tableaux
        """
        self.logger = logging.getLogger("athly.orchestrator")
        self.logger.info("Initialisation de l'agent orchestrateur")
        
        self.llm = llm
        self.sport_expert = sport_expert
        self.table_generator = table_generator
        self.chat_history = []
        
        # Initialisation du gestionnaire de programmes
        try:
            from models.program_data import ProgramDataManager
            self.program_manager = ProgramDataManager()
            print("Gestionnaire de programmes initialisé avec succès")
        except Exception as e:
            print(f"Erreur lors de l'initialisation du gestionnaire de programmes: {str(e)}")
            self.program_manager = None
        
        # Initialisation de la mémoire de conversation
        self.logger.debug("Initialisation de la mémoire de conversation")
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Définition des outils disponibles pour l'agent
        self.logger.debug("Configuration des outils pour l'agent")
        self.tools = [
            Tool(
                name="expert_sport",
                func=self._call_sport_expert,
                description="Utile pour obtenir des conseils d'expert en programmation d'entraînement sportif. "
                           "Fournit des recommandations sur les exercices, la périodisation et la progression."
            ),
            Tool(
                name="table_generator",
                func=self._call_table_generator,
                description="Utile pour générer des tableaux de programmation d'entraînement et formater les données."
            )
        ]
        
        # Création du prompt pour l'agent
        self.logger.debug("Création du prompt pour l'agent orchestrateur")
        template_str = self._create_orchestrator_prompt()
        
        # Création du template de prompt
        self.logger.debug("Création du template de prompt")
        self.prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(template_str),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
        
        try:
            # Création de l'agent avec initialize_agent
            self.logger.debug("Création de l'agent avec les outils et le prompt")
            self.agent_executor = initialize_agent(
                self.tools,
                self.llm,
                agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                memory=self.memory,
                verbose=True,
                handle_parsing_errors=True,
                prompt=self.prompt_template
            )
            
            # Initialisation du graph d'agent avec LangGraph
            self.logger.info("Initialisation du graph d'agent avec LangGraph")
            self.agent_graph = AgentGraph(
                llm=self.llm,
                tools=self.tools,
                logger=self.logger
            )
            self.has_graph = True
            self.logger.info("Graph d'agent initialisé avec succès")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'initialisation de l'agent orchestrateur: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.has_graph = False
        
        self.logger.info("Agent orchestrateur initialisé avec succès")
    
    def _create_orchestrator_prompt(self):
        """
        Crée le prompt de base pour l'Agent Orchestrateur.
        
        Returns:
            La chaîne de caractères du template
        """
        self.logger.debug("Création du template de prompt")
        template = """Tu es Athly, un coach sportif IA expert en programmation d'entraînement multisport.

Tu aides les utilisateurs à générer des programmes d'entraînement personnalisés dans 
différentes disciplines comme la course à pied, la musculation et les exercices au poids du corps.

Tu dois comprendre les besoins de l'utilisateur et utiliser les outils à ta disposition 
pour créer un programme adapté et détaillé.

Pour générer un programme complet, tu dois:
1. Identifier les disciplines concernées et les objectifs de l'utilisateur
2. Déterminer le niveau et les contraintes de l'utilisateur
3. Utiliser l'outil Expert Sport pour obtenir une structure de programme adaptée
4. Utiliser l'outil Générateur de Tableaux pour présenter clairement le programme

Tu dois suivre les principes de périodisation et adapter la programmation au niveau de l'utilisateur.

Utilise un formatage simple et efficace pour tes réponses:
- Préfère les listes à puces (- item) pour les conseils et exercices
- Place chaque point sur une nouvelle ligne
- Mets en gras les termes importants avec **terme**
- Utilise des titres avec ### pour les sections principales
- Évite les formatages trop complexes
- Préfère les bullet points aux listes numérotées quand c'est possible
"""
        
        return template
    
    def _call_sport_expert(self, query):
        """
        Appelle l'agent expert en sport pour obtenir des conseils spécialisés.
        
        Args:
            query: La requête à transmettre à l'expert
            
        Returns:
            Les recommandations de l'expert en sport
        """
        logger.info(f"Appel à l'expert sport avec la requête: {query[:50]}...")
        start_time = time.time()
        try:
            result = self.sport_expert.generate_advice(query)
            logger.debug(f"Réponse de l'expert sport: {result[:100]}...")
            logger.info(f"Expert sport consulté en {time.time() - start_time:.2f} secondes")
            return result
        except Exception as e:
            logger.error(f"Erreur lors de la consultation de l'expert sport: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _call_table_generator(self, query):
        """
        Appelle l'agent générateur de tableaux pour créer un tableau à partir d'une requête.
        
        Args:
            query: La requête pour générer un tableau
            
        Returns:
            Le tableau généré
        """
        if not self.table_generator:
            raise ValueError("Aucun générateur de tableaux n'a été fourni à l'orchestrateur")
        
        try:
            return self.table_generator.generate_table(query)
        except Exception as e:
            logger.error(f"Erreur lors de l'appel au générateur de tableaux: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _can_use_direct_mode(self, message: str) -> bool:
        """
        Détermine si le message peut être traité en mode direct.
        
        Args:
            message: Le message de l'utilisateur
            
        Returns:
            True si le message peut être traité en mode direct, False sinon
        """
        # Analyse simple pour déterminer si on peut utiliser le mode direct
        # Nous privilégions le mode direct pour la plupart des requêtes
        
        # Mots clés indiquant une demande complexe nécessitant les agents
        complex_keywords = [
            "compare",
            "analyse",
            "planifie",
            "explique en détail",
            "développe un plan",
            "crée un programme personnalisé"
        ]
        
        # Si le message contient des mots clés complexes, utiliser les agents
        if any(keyword in message.lower() for keyword in complex_keywords):
            self.logger.debug(f"Mode normal détecté pour le message: {message[:50]}...")
            return False
        
        # Par défaut, utiliser le mode direct pour plus de rapidité
        self.logger.debug(f"Mode direct détecté pour le message: {message[:50]}...")
        return True
    
    def _format_response(self, text):
        """
        Améliore le formatage du texte de réponse pour une meilleure lisibilité.
        
        Args:
            text: Le texte à formater
            
        Returns:
            Le texte formaté
        """
        # Si le texte est vide, retourner tel quel
        if not text:
            return text
            
        # Détecter si nous utilisons USE_QWEN ou non
        using_qwen = os.getenv("USE_QWEN", "false").lower() == "true"
        
        # Formatage de base pour tous les modèles
        
        # Ajouter des sauts de ligne avant les éléments de liste numérotée
        text = re.sub(r'(\d+\.\s+)', r'\n\n\1', text)
        
        # Ajouter des sauts de ligne avant les puces
        text = re.sub(r'(-\s+)', r'\n\n\1', text)
        
        # Ajouter des sauts de ligne avant les titres
        text = re.sub(r'(#+\s+)', r'\n\n\1', text)
        
        # Assurer que les tableaux sont bien formatés
        text = re.sub(r'\n\|\s*', r'\n| ', text)
        
        # Espacer après les points
        text = re.sub(r'\.(\S)', r'. \1', text)
        
        # Espacer après les virgules
        text = re.sub(r',(\S)', r', \1', text)
        
        # Formatage simple pour les listes à puces
        text = re.sub(r'(\n\s*-\s*\*\*)', r'\n- **', text)
        
        # S'assurer que les titres sont bien séparés
        text = re.sub(r'(\n#+.*?\n)(\S)', r'\1\n\2', text)
        
        return text
    
    def process_chat(self, message: str) -> str:
        """
        Traite un message de chat et génère une réponse.
        
        Args:
            message: Message de l'utilisateur
            
        Returns:
            Réponse générée
        """
        print(f"DÉBUT TRAITEMENT MESSAGE: {message}")
        
        # Vérifier si on peut utiliser le mode direct (contournement des agents)
        if self._can_use_direct_mode(message):
            print("APPEL DIRECT AU LLM (contournement des agents)")
            
            try:
                # Recherche de programmes existants
                print("Recherche de programmes existants...")
                if "programme" in message.lower() and any(keyword in message.lower() for keyword in ["course", "running", "courir", "jogging"]):
                    print("Détection de demande de programme de course")
                    
                    # TODO: Implémenter la logique de recherche de programmes existants
                    # Pour l'instant, on utilise les agents normaux
                    
                # Si aucun programme trouvé, utiliser le LLM directement
                if self.has_graph:
                    start_time = time.time()
                    self.logger.info(f"UTILISATION DU GRAPH D'AGENT - Message: {message[:50]}...")
                    
                    # Ajouter des informations contextuelles
                    context = {
                        "timestamp": time.time(),
                        "direct_mode": True
                    }
                    
                    response = self.agent_graph.process_message(message, context)
                    
                    elapsed = time.time() - start_time
                    self.logger.info(f"TEMPS D'EXÉCUTION GRAPH: {elapsed:.2f} secondes")
                    
                    print(f"RÉPONSE OBTENUE (graph): {response[:50]}...")
                    return self._format_response(response)
                else:
                    # Utiliser directement le LLM avec un prompt simple
                    prompt = f"""Tu es Athly, un coach sportif virtuel spécialisé en sciences du sport.

Réponds à la question suivante de façon claire et concise, en utilisant un formatage simple et efficace :
- Utilise des listes à puces (- item) pour présenter les points clés 
- Place chaque point sur une nouvelle ligne
- Met en gras les termes importants avec **terme**
- Utilise des titres avec ### pour les sections principales
- Évite les formatages trop complexes
- Préfère les bullet points aux listes numérotées quand c'est possible

Question : {message}
"""
                    
                    start_time = time.time()
                    try:
                        response = self.llm.invoke(prompt)
                        elapsed = time.time() - start_time
                        self.logger.info(f"TEMPS D'EXÉCUTION LLM DIRECT: {elapsed:.2f} secondes")
                        
                        print(f"RÉPONSE OBTENUE (format alternatif): {str(response)[:50]}...")
                        return self._format_response(str(response))
                    except Exception as e:
                        self.logger.error(f"ERREUR RENCONTRÉE: {str(e)}")
                        self.logger.error(f"TYPE D'ERREUR: {type(e).__name__}")
                        import traceback
                        self.logger.error(f"TRACEBACK:\n{traceback.format_exc()}")
                        
                        # Fallback vers le processus normal si erreur
                        print("ERREUR AVEC LE MODE DIRECT, UTILISATION DU MODE NORMAL")
            
            except Exception as e:
                self.logger.error(f"Erreur dans le mode direct: {str(e)}")
                print(f"ERREUR DANS LE MODE DIRECT: {str(e)}")
        
        # Si on est arrivé ici, utiliser le processus normal
        try:
            # Pour le mode normal, essayer d'abord avec le graph si disponible
            if self.has_graph:
                start_time = time.time()
                self.logger.info(f"UTILISATION DU GRAPH D'AGENT - Message: {message[:50]}...")
                
                # Ajouter des informations contextuelles
                context = {
                    "timestamp": time.time(),
                    "direct_mode": False
                }
                
                response = self.agent_graph.process_message(message, context)
                
                elapsed = time.time() - start_time
                self.logger.info(f"TEMPS D'EXÉCUTION GRAPH: {elapsed:.2f} secondes")
                
                print(f"RÉPONSE OBTENUE (graph): {response[:50]}...")
                return self._format_response(response)
            
            # Si le graph n'est pas disponible, utiliser l'agent executor classique
            start_time = time.time()
            self.logger.info("Exécution de l'agent executor classique")
            response = self.agent_executor.run(input=message)
            elapsed = time.time() - start_time
            self.logger.info(f"TEMPS D'EXÉCUTION AGENT: {elapsed:.2f} secondes")
            
            print(f"RÉPONSE OBTENUE: {response[:50]}...")
            return self._format_response(response)
            
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement du message: {str(e)}")
            error_message = f"Désolé, j'ai rencontré une erreur. Pouvez-vous réessayer?"
            return error_message
    
    def generate_training_program(self, disciplines, duration, level, goals, constraints="", equipment="", frequency=3, time_per_session=60):
        """
        Génère un programme d'entraînement complet en fonction des paramètres fournis.
        
        Args:
            disciplines: Liste des disciplines choisies
            duration: Durée du programme en semaines
            level: Niveau de l'utilisateur
            goals: Objectifs principaux
            constraints: Contraintes physiques ou médicales
            equipment: Équipement disponible
            frequency: Fréquence d'entraînement par semaine
            time_per_session: Temps disponible par séance en minutes
            
        Returns:
            Le programme d'entraînement complet formaté
        """
        logger.info(f"Génération d'un programme pour disciplines: {disciplines}, niveau: {level}, durée: {duration} semaines")
        print(f"GÉNÉRATION PROGRAMME: disciplines={disciplines}, durée={duration}, niveau={level}")
        start_time = time.time()
        
        try:
            # Contournement des agents: appel direct au LLM avec un prompt bien formaté
            disciplines_str = ", ".join(disciplines)
            
            # Création d'un prompt détaillé pour générer directement un programme de qualité
            prompt = f"""Tu es Athly, un coach sportif IA expert en sciences du sport et en programmation d'entraînement.
            
            Génère un programme d'entraînement complet basé sur ces paramètres:
            
            PARAMÈTRES:
            - Disciplines: {disciplines_str}
            - Durée: {duration} semaines
            - Niveau: {level}
            - Objectifs: {goals}
            - Contraintes physiques/médicales: {constraints}
            - Équipement disponible: {equipment}
            - Fréquence: {frequency} jours/semaine
            - Temps par séance: {time_per_session} minutes
            
            FORMAT DE RÉPONSE:
            1. Présente d'abord une introduction avec les objectifs du programme
            2. Organise le programme semaine par semaine
            3. Pour chaque semaine, détaille les séances jour par jour
            4. Pour chaque séance, utilise un format tabulaire markdown pour présenter:
               - Exercice/activité
               - Séries/répétitions/durée
               - Intensité/charge
               - Récupération
               - Notes techniques
            5. Conclus avec des conseils de progression et d'adaptation
            
            Assure-toi que la progression est logique et que les exercices sont adaptés au niveau indiqué.
            """
            
            print(f"APPEL DIRECT AU LLM POUR LE PROGRAMME")
            
            # Appel direct au LLM
            response = self.llm.invoke(prompt)
            
            # Extraire le contenu de la réponse (format LangChain)
            if hasattr(response, 'content'):
                print(f"PROGRAMME GÉNÉRÉ (via attribut content): {len(response.content)} caractères")
                formatted_program = response.content
            else:
                print(f"PROGRAMME GÉNÉRÉ (format alternatif): {len(str(response))} caractères")
                formatted_program = str(response)
            
            logger.info(f"Programme généré en {time.time() - start_time:.2f} secondes")
            return formatted_program
        except Exception as e:
            logger.error(f"Erreur lors de la génération du programme: {str(e)}")
            logger.error(traceback.format_exc())
            print(f"ERREUR GÉNÉRATION PROGRAMME: {str(e)}")
            print(traceback.format_exc())
            raise 