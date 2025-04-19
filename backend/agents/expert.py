from langchain.prompts import PromptTemplate
import logging
import traceback
import time

# Configuration du logger
logger = logging.getLogger("athly.expert")

class SportExpertAgent:
    """
    Agent Expert en Sport qui fournit des connaissances spécialisées en programmation d'entraînement.
    """
    
    def __init__(self, llm, knowledge_base):
        """
        Initialise l'Agent Expert en Sport.
        
        Args:
            llm: Le modèle de langage à utiliser
            knowledge_base: La base de connaissances sportives
        """
        logger.info("Initialisation de l'agent expert en sport")
        self.llm = llm
        self.knowledge_base = knowledge_base
        
        logger.debug("Chargement des prompts pour l'agent expert")
        self.advice_prompt = self._load_advice_prompt()
        self.structure_prompt = self._load_structure_prompt()
        self.detailed_prompt = self._load_detailed_prompt()
        logger.info("Agent expert en sport initialisé avec succès")
    
    def _load_advice_prompt(self):
        """
        Charge le prompt pour générer des conseils généraux.
        """
        logger.debug("Chargement du prompt pour les conseils")
        template = """
        Tu es un expert en sciences du sport et en programmation d'entraînement. Utilise tes connaissances 
        pour répondre à la question suivante de manière détaillée et précise. Base tes réponses sur les 
        données scientifiques actuelles et les meilleures pratiques en matière d'entraînement sportif.
        
        Si tu as besoin de données spécifiques à certaines disciplines, base-toi sur les informations suivantes:
        {context}
        
        Question: {query}
        """
        return PromptTemplate.from_template(template)
    
    def _load_structure_prompt(self):
        """
        Charge le prompt pour générer la structure d'un programme d'entraînement.
        """
        logger.debug("Chargement du prompt pour la structure du programme")
        template = """
        Tu es un coach sportif spécialisé en programmation d'entraînement. Ton objectif est de créer une 
        structure de programme d'entraînement pour les paramètres suivants:
        
        DISCIPLINES: {disciplines}
        DURÉE: {duration} semaines
        NIVEAU: {level}
        OBJECTIFS: {goals}
        
        En te basant sur les principes de périodisation et de progression, génère une structure de 
        programme qui couvre toute la durée spécifiée. Inclus les éléments suivants:
        
        1. Une vue d'ensemble du programme avec les phases principales (préparation, développement, spécifique, etc.)
        2. Les objectifs de chaque phase ou bloc de semaines
        3. La répartition générale des types d'entraînement sur la durée totale
        4. L'évolution de l'intensité et du volume pendant la durée du programme
        
        Utilise les informations suivantes pour t'aider dans ta programmation:
        {context}
        
        Format ta réponse de manière structurée et claire, en séparant bien les différentes phases du programme.
        """
        return PromptTemplate.from_template(template)
    
    def _load_detailed_prompt(self):
        """
        Charge le prompt pour générer les détails d'un programme d'entraînement.
        """
        logger.debug("Chargement du prompt pour les détails du programme")
        template = """
        Tu es un coach sportif expert en programmation d'entraînement. Ton objectif est de détailler le 
        programme d'entraînement suivant avec des exercices spécifiques, des séries/répétitions, des durées 
        et des intensités précises.

        STRUCTURE GÉNÉRALE DU PROGRAMME:
        {structure}
        
        CONTRAINTES ET INFORMATIONS SUPPLÉMENTAIRES:
        - Contraintes physiques/médicales: {constraints}
        - Équipement disponible: {equipment}
        - Fréquence d'entraînement: {frequency} jours par semaine
        - Temps disponible par séance: {time_per_session} minutes
        
        Pour chaque semaine du programme, détaille:
        1. Les séances d'entraînement jour par jour
        2. Les exercices précis pour chaque séance
        3. Les séries, répétitions, récupérations pour la musculation
        4. Les durées, distances, intensités pour les exercices cardio
        5. Des variantes pour les exercices en fonction de l'équipement disponible
        6. Des conseils techniques pour l'exécution des exercices

        Assure-toi que la progression est logique et adapte les exercices au niveau indiqué dans la structure.
        Format ton programme de manière structurée avec des tableaux pour faciliter la lecture.
        """
        return PromptTemplate.from_template(template)
    
    def generate_advice(self, query):
        """
        Génère des conseils sportifs en réponse à une question.
        
        Args:
            query: La question posée par l'utilisateur
            
        Returns:
            Les conseils générés
        """
        logger.info(f"Génération de conseils pour la requête: {query[:50]}...")
        start_time = time.time()
        
        try:
            # Récupération des informations pertinentes depuis la base de connaissances
            logger.debug("Requête à la base de connaissances")
            context_docs = self.knowledge_base.query(query)
            context = "\n".join([doc.page_content for doc in context_docs])
            logger.debug(f"Contexte récupéré: {len(context)} caractères, {len(context_docs)} documents")
            
            # Formatage du prompt avec le contexte et la question
            logger.debug("Formatage du prompt de conseil")
            prompt = self.advice_prompt.format(context=context, query=query)
            
            # Génération de la réponse
            logger.info("Invocation du LLM pour générer des conseils")
            response = self.llm.invoke(prompt)
            
            logger.info(f"Conseils générés en {time.time() - start_time:.2f} secondes")
            return response
        except Exception as e:
            logger.error(f"Erreur lors de la génération de conseils: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def generate_program_structure(self, disciplines, duration, level, goals):
        """
        Génère la structure d'un programme d'entraînement.
        
        Args:
            disciplines: Liste des disciplines choisies
            duration: Durée du programme en semaines
            level: Niveau de l'utilisateur
            goals: Objectifs principaux
            
        Returns:
            La structure du programme
        """
        logger.info(f"Génération de la structure du programme: {', '.join(disciplines)}, niveau {level}")
        start_time = time.time()
        
        try:
            # Conversion de la liste de disciplines en chaîne de caractères
            disciplines_str = ", ".join(disciplines)
            
            # Construction de la requête pour la base de connaissances
            query = f"programming {disciplines_str} {level} {goals} {duration} weeks"
            logger.debug(f"Requête à la base de connaissances: {query}")
            
            # Récupération des informations pertinentes depuis la base de connaissances
            context_docs = self.knowledge_base.query(query)
            context = "\n".join([doc.page_content for doc in context_docs])
            logger.debug(f"Contexte récupéré: {len(context)} caractères, {len(context_docs)} documents")
            
            # Formatage du prompt avec les paramètres et le contexte
            logger.debug("Formatage du prompt de structure")
            prompt = self.structure_prompt.format(
                disciplines=disciplines_str,
                duration=duration,
                level=level,
                goals=goals,
                context=context
            )
            
            # Génération de la structure
            logger.info("Invocation du LLM pour générer la structure du programme")
            response = self.llm.invoke(prompt)
            
            logger.info(f"Structure du programme générée en {time.time() - start_time:.2f} secondes")
            return response
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la structure du programme: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def generate_detailed_program(self, structure, constraints="", equipment="", frequency=3, time_per_session=60):
        """
        Génère les détails d'un programme d'entraînement à partir de sa structure.
        
        Args:
            structure: La structure générale du programme
            constraints: Contraintes physiques ou médicales
            equipment: Équipement disponible
            frequency: Fréquence d'entraînement par semaine
            time_per_session: Temps disponible par séance en minutes
            
        Returns:
            Le programme détaillé
        """
        logger.info(f"Génération des détails du programme: freq={frequency}/semaine, {time_per_session}min/séance")
        start_time = time.time()
        
        try:
            # Formatage du prompt avec les paramètres
            logger.debug("Formatage du prompt de détails")
            prompt = self.detailed_prompt.format(
                structure=structure,
                constraints=constraints,
                equipment=equipment,
                frequency=frequency,
                time_per_session=time_per_session
            )
            
            # Génération des détails du programme
            logger.info("Invocation du LLM pour générer les détails du programme")
            response = self.llm.invoke(prompt)
            
            logger.info(f"Détails du programme générés en {time.time() - start_time:.2f} secondes")
            return response
        except Exception as e:
            logger.error(f"Erreur lors de la génération des détails du programme: {str(e)}")
            logger.error(traceback.format_exc())
            raise 