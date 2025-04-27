from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
import logging
import traceback
import time
import json
import os

from .expert import SportExpertAgent
from .table_generator import TableGeneratorAgent

# Obtention du logger
logger = logging.getLogger("athly.orchestrator")

class OrchestratorAgent:
    """
    Agent Orchestrateur qui coordonne le flux de travail entre les différents agents spécialisés.
    """
    
    def __init__(self, llm, sport_expert, table_generator):
        """
        Initialise l'Agent Orchestrateur avec les agents spécialisés nécessaires.
        
        Args:
            llm: Le modèle de langage à utiliser
            sport_expert: L'agent expert en sport
            table_generator: L'agent générateur de tableaux
        """
        logger.info("Initialisation de l'agent orchestrateur")
        self.llm = llm
        self.sport_expert = sport_expert
        self.table_generator = table_generator
        
        # Initialisation de la mémoire de conversation
        logger.debug("Initialisation de la mémoire de conversation")
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Définition des outils disponibles pour l'agent
        logger.debug("Configuration des outils pour l'agent")
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
        logger.debug("Création du prompt pour l'agent orchestrateur")
        self.prompt = self._create_orchestrator_prompt()
        
        try:
            # Création de l'agent avec initialize_agent
            logger.debug("Création de l'agent avec les outils et le prompt")
            self.agent_executor = initialize_agent(
                tools=self.tools,
                llm=self.llm,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                memory=self.memory,
                handle_parsing_errors=True,
                max_iterations=25,
                early_stopping_method="generate"
            )
            logger.info("Agent orchestrateur initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de l'agent orchestrateur: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _create_orchestrator_prompt(self):
        """
        Crée le prompt de base pour l'Agent Orchestrateur.
        """
        logger.debug("Création du template de prompt")
        template = """
        Tu es Athly, un coach sportif IA expert en programmation d'entraînement multisport.

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
        
        Quand tu utilises un outil, tu dois TOUJOURS utiliser le format JSON suivant:
        ```
        {{"thought": "ton raisonnement",
         "action": "nom_de_l_outil",
         "action_input": "paramètres pour l'outil"}}
        ```
        
        Quand tu as suffisamment d'informations et que tu veux répondre directement, utilise:
        ```
        {{"thought": "ton raisonnement",
         "action": "Final Answer",
         "action_input": "ta réponse complète"}}
        ```
        
        Voici un exemple d'utilisation de l'outil expert_sport:
        ```
        {{"thought": "Je dois obtenir une structure de programme adaptée à un coureur débutant",
         "action": "expert_sport",
         "action_input": "Je cherche un programme pour un débutant en course à pied qui souhaite préparer un 10km en 8 semaines."}}
        ```

        Voici un exemple d'utilisation de l'outil table_generator:
        ```
        {{"thought": "Je dois présenter le programme de manière claire et structurée",
         "action": "table_generator",
         "action_input": "Programme de course à pied sur 8 semaines pour débutant: Semaine 1: 3x20min, Semaine 2: 3x25min..."}}
        ```
        
        Voici un exemple complet de génération d'un programme:
        
        Utilisateur: Je souhaite un programme de musculation pour débutant sur 8 semaines, avec 3 séances par semaine, pour prendre du muscle.
        
        ```
        {{"thought": "Je dois d'abord obtenir une structure de programme adaptée à un débutant en musculation",
         "action": "expert_sport",
         "action_input": "Programme de musculation pour débutant, 8 semaines, 3 séances par semaine, objectif: prise de muscle"}}
        ```
        
        [Réponse de l'expert_sport avec la structure du programme]
        
        ```
        {{"thought": "Maintenant que j'ai la structure, je dois la mettre en forme pour qu'elle soit facilement lisible",
         "action": "table_generator",
         "action_input": "[Détails du programme fournis par expert_sport]"}}
        ```
        
        [Réponse du table_generator avec le tableau formaté]
        
        ```
        {{"thought": "J'ai généré un programme complet et formaté pour l'utilisateur",
         "action": "Final Answer",
         "action_input": "Voici votre programme de musculation sur 8 semaines pour débutant:\n\n[Programme formaté]"}}
        ```
        
        {chat_history}
        
        Question de l'utilisateur: {input}
        """
        
        return PromptTemplate.from_template(template)
    
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
    
    def _call_table_generator(self, program_data, format_type="markdown"):
        """
        Appelle l'agent générateur de tableaux pour formater les données d'entraînement.
        
        Args:
            program_data: Les données du programme d'entraînement
            format_type: Le format de sortie souhaité (markdown, html, etc.)
            
        Returns:
            Le tableau formaté
        """
        logger.info(f"Appel au générateur de tableaux pour format: {format_type}")
        try:
            result = self.table_generator.generate_training_table(program_data, format_type)
            logger.debug(f"Tableau généré: {result[:100]}...")
            return result
        except Exception as e:
            logger.error(f"Erreur lors de la génération du tableau: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def process_chat(self, message):
        """
        Traite un message chat de l'utilisateur et génère une réponse.
        
        Args:
            message: Le message de l'utilisateur
            
        Returns:
            La réponse générée
        """
        print(f"DÉBUT TRAITEMENT MESSAGE: {message}")
        try:
            # Note: Nous contournons le système d'agents complexe qui échoue
            # et utilisons directement le LLM comme dans notre test
            print("APPEL DIRECT AU LLM (contournement des agents)")
            
            prompt = f"""Tu es Athly, un coach sportif IA expert en sciences du sport et en programmation d'entraînement.
            Tu aides les utilisateurs avec des conseils précis et basés sur la science.
            
            Réponds à cette question de manière détaillée et professionnelle:
            {message}
            """
            
            # Appel direct au LLM
            response = self.llm.invoke(prompt)
            
            # Extraire le contenu de la réponse (format LangChain)
            if hasattr(response, 'content'):
                print(f"RÉPONSE OBTENUE (via attribut content): {response.content[:50]}...")
                return response.content
            # Fallback si le format de réponse est différent
            else:
                print(f"RÉPONSE OBTENUE (format alternatif): {str(response)[:50]}...")
                return str(response)
        except Exception as e:
            print(f"ERREUR RENCONTRÉE: {str(e)}")
            print(f"TYPE D'ERREUR: {type(e).__name__}")
            import traceback
            print(f"TRACEBACK:\n{traceback.format_exc()}")
            return f"Désolé, j'ai rencontré une erreur. Pouvez-vous réessayer?"
    
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