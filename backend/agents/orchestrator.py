from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain.prompts import PromptTemplate

from .expert import SportExpertAgent
from .table_generator import TableGeneratorAgent

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
        self.llm = llm
        self.sport_expert = sport_expert
        self.table_generator = table_generator
        
        # Initialisation de la mémoire de conversation
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Définition des outils disponibles pour l'agent
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
        self.prompt = self._create_orchestrator_prompt()
        
        # Création de l'agent
        self.agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)
        
        # Création de l'exécuteur d'agent
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def _create_orchestrator_prompt(self):
        """
        Crée le prompt de base pour l'Agent Orchestrateur.
        """
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
        return self.sport_expert.generate_advice(query)
    
    def _call_table_generator(self, program_data, format_type="markdown"):
        """
        Appelle l'agent générateur de tableaux pour formater les données d'entraînement.
        
        Args:
            program_data: Les données du programme d'entraînement
            format_type: Le format de sortie souhaité (markdown, html, etc.)
            
        Returns:
            Le tableau formaté
        """
        return self.table_generator.generate_training_table(program_data, format_type)
    
    def process_chat(self, message):
        """
        Traite un message chat de l'utilisateur et génère une réponse.
        
        Args:
            message: Le message de l'utilisateur
            
        Returns:
            La réponse générée
        """
        response = self.executor.invoke({"input": message})
        return response.get("output", "Je n'ai pas pu générer de réponse.")
    
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
        # Construction de la requête pour l'expert sport
        disciplines_str = ", ".join(disciplines)
        query = f"""
        Générer un programme d'entraînement avec les paramètres suivants:
        - Disciplines: {disciplines_str}
        - Durée: {duration} semaines
        - Niveau: {level}
        - Objectifs: {goals}
        - Contraintes: {constraints}
        - Équipement: {equipment}
        - Fréquence: {frequency} jours/semaine
        - Temps par séance: {time_per_session} minutes
        """
        
        # Obtention de la structure du programme
        program_structure = self.sport_expert.generate_program_structure(
            disciplines=disciplines,
            duration=duration,
            level=level,
            goals=goals
        )
        
        # Génération des détails du programme
        program_details = self.sport_expert.generate_detailed_program(
            structure=program_structure,
            constraints=constraints,
            equipment=equipment,
            frequency=frequency,
            time_per_session=time_per_session
        )
        
        # Formatage du programme avec des tableaux
        formatted_program = self.table_generator.generate_training_table(program_details)
        
        return formatted_program 