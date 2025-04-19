from langchain.prompts import PromptTemplate

class TableGeneratorAgent:
    """
    Agent Codeur de Tables qui structure les données d'entraînement en formats visuellement exploitables.
    """
    
    def __init__(self, llm):
        """
        Initialise l'Agent Codeur de Tables.
        
        Args:
            llm: Le modèle de langage à utiliser
        """
        self.llm = llm
        self.templates = self._load_table_templates()
        self.table_prompt = self._create_table_prompt()
    
    def _load_table_templates(self):
        """
        Charge les templates pour différents formats de tableaux.
        
        Returns:
            Dictionnaire de templates par format
        """
        templates = {
            "markdown": """
            # Exemple de tableau Markdown
            
            ## Planning Hebdomadaire
            
            | Jour | Type d'entraînement | Détails | Durée |
            |------|---------------------|---------|-------|
            | Lundi | Musculation | Exercices, séries, répétitions | 60 min |
            | Mercredi | Course | Distance, intensité, intervalles | 45 min |
            | Vendredi | Poids de corps | Exercices, séries, récupération | 30 min |
            
            ## Détails des Exercices
            
            ### Lundi - Musculation
            
            | Exercice | Séries | Répétitions | Récupération | Notes |
            |----------|--------|-------------|--------------|-------|
            | Squat | 4 | 8-10 | 2 min | Technique, progression |
            | Développé couché | 3 | 10-12 | 90 sec | Variation possible |
            """,
            
            "html": """
            <table class="program-table">
              <thead>
                <tr>
                  <th>Jour</th>
                  <th>Type d'entraînement</th>
                  <th>Détails</th>
                  <th>Durée</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Lundi</td>
                  <td>Musculation</td>
                  <td>Exercices, séries, répétitions</td>
                  <td>60 min</td>
                </tr>
              </tbody>
            </table>
            """
        }
        
        return templates
    
    def _create_table_prompt(self):
        """
        Crée le prompt principal pour la génération de tableaux.
        """
        template = """
        Tu es un expert en création de tableaux et de formats visuels pour les programmes d'entraînement sportif.
        
        Ton objectif est de transformer les données brutes d'un programme d'entraînement en un tableau visuel 
        bien structuré, facile à lire et à comprendre.
        
        DONNÉES DU PROGRAMME:
        {program_data}
        
        FORMAT SOUHAITÉ:
        {format_template}
        
        Directives:
        1. Utilise le format spécifié ci-dessus pour structurer les données
        2. Organise les informations de manière logique (par semaine, par jour, par type d'exercice)
        3. Inclus tous les détails essentiels (exercices, séries, répétitions, durées, intensités, etc.)
        4. Assure-toi que la progression est clairement visible
        5. Ajoute des titres et sous-titres pour faciliter la navigation dans le programme
        6. Si nécessaire, crée plusieurs tableaux pour différentes sections du programme
        
        Génère maintenant un tableau complet et bien structuré en utilisant les données fournies.
        """
        
        return PromptTemplate.from_template(template)
    
    def generate_training_table(self, program_data, format_type="markdown"):
        """
        Génère un tableau formaté pour un programme d'entraînement.
        
        Args:
            program_data: Les données du programme d'entraînement
            format_type: Le format souhaité (markdown, html, etc.)
            
        Returns:
            Le tableau formaté
        """
        # Récupération du template de format approprié
        if format_type not in self.templates:
            format_type = "markdown"  # Format par défaut
        
        format_template = self.templates[format_type]
        
        # Formatage du prompt
        prompt = self.table_prompt.format(
            program_data=program_data,
            format_template=format_template
        )
        
        # Génération du tableau
        response = self.llm.invoke(prompt)
        
        return response
    
    def create_weekly_schedule(self, weekly_data):
        """
        Crée un tableau d'emploi du temps hebdomadaire.
        
        Args:
            weekly_data: Les données de la semaine
            
        Returns:
            Le tableau d'emploi du temps
        """
        prompt = f"""
        Crée un tableau hebdomadaire pour les données suivantes:
        
        {weekly_data}
        
        Le tableau doit inclure les jours de la semaine, le type d'entraînement pour chaque jour, 
        et un résumé des exercices clés ou de l'objectif de la séance.
        
        Format le tableau en Markdown.
        """
        
        response = self.llm.invoke(prompt)
        
        return response
    
    def create_exercise_details(self, exercise_data):
        """
        Crée un tableau détaillé pour un ensemble d'exercices.
        
        Args:
            exercise_data: Les données des exercices
            
        Returns:
            Le tableau détaillé
        """
        prompt = f"""
        Crée un tableau détaillé pour les exercices suivants:
        
        {exercise_data}
        
        Le tableau doit inclure pour chaque exercice:
        - Nom de l'exercice
        - Séries et répétitions ou durée
        - Intensité ou charge
        - Temps de récupération
        - Notes techniques ou variantes
        
        Format le tableau en Markdown.
        """
        
        response = self.llm.invoke(prompt)
        
        return response
    
    def create_program_overview(self, program_structure):
        """
        Crée un tableau récapitulatif pour l'ensemble du programme.
        
        Args:
            program_structure: La structure du programme
            
        Returns:
            Le tableau récapitulatif
        """
        prompt = f"""
        Crée un tableau récapitulatif pour l'ensemble du programme suivant:
        
        {program_structure}
        
        Le tableau doit montrer la progression semaine par semaine, avec les objectifs principaux 
        et les focus d'entraînement pour chaque semaine ou bloc.
        
        Format le tableau en Markdown.
        """
        
        response = self.llm.invoke(prompt)
        
        return response 