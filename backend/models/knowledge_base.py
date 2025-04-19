from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader, DirectoryLoader
import os
import json
from typing import List, Dict, Any

class KnowledgeBase:
    """
    Base de connaissances qui sert de référentiel pour les informations spécialisées sur l'entraînement sportif.
    """
    
    def __init__(self, embedding_model=None, data_path="./data"):
        """
        Initialise la base de connaissances.
        
        Args:
            embedding_model: Le modèle d'embedding à utiliser
            data_path: Le chemin vers les données d'entraînement
        """
        self.embedding_model = embedding_model or HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.data_path = data_path
        self.vector_db = self._initialize_db()
        
        # Si la base de données vectorielle est vide, chargez les données
        if not self._db_exists():
            self._load_data()
    
    def _db_exists(self):
        """
        Vérifie si la base de données vectorielle existe déjà.
        
        Returns:
            True si la base existe, False sinon
        """
        chroma_dir = os.path.join(self.data_path, "chroma")
        return os.path.exists(chroma_dir) and len(os.listdir(chroma_dir)) > 0
    
    def _initialize_db(self):
        """
        Initialise la base de données vectorielle.
        
        Returns:
            L'instance de la base de données vectorielle
        """
        # Création du répertoire de données si nécessaire
        os.makedirs(self.data_path, exist_ok=True)
        
        # Initialisation de la base de données vectorielle
        return Chroma(
            persist_directory=os.path.join(self.data_path, "chroma"),
            embedding_function=self.embedding_model
        )
    
    def _load_data(self):
        """
        Charge les données d'entraînement dans la base de connaissances.
        """
        # Création de données d'exemple si le répertoire est vide
        if not os.listdir(self.data_path) or len(os.listdir(self.data_path)) <= 1:  # Compte le répertoire chroma s'il existe
            self._create_sample_data()
        
        # Chargement des documents
        documents = []
        
        # Chargement des fichiers texte
        for discipline in ["running", "bodyweight", "strength"]:
            discipline_path = os.path.join(self.data_path, discipline)
            if os.path.exists(discipline_path):
                loaders = DirectoryLoader(discipline_path, glob="**/*.txt", loader_cls=TextLoader)
                documents.extend(loaders.load())
        
        # Chargement des fichiers JSON
        exercises_path = os.path.join(self.data_path, "exercises")
        if os.path.exists(exercises_path):
            for filename in os.listdir(exercises_path):
                if filename.endswith(".json"):
                    with open(os.path.join(exercises_path, filename), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        for exercise in data:
                            content = f"Exercice: {exercise['name']}\n"
                            content += f"Type: {exercise['type']}\n"
                            content += f"Muscles ciblés: {', '.join(exercise['muscles'])}\n"
                            content += f"Niveau: {exercise['level']}\n"
                            content += f"Description: {exercise['description']}\n"
                            content += f"Instructions: {exercise['instructions']}\n"
                            
                            from langchain.schema import Document
                            doc = Document(
                                page_content=content,
                                metadata={"source": filename, "type": "exercise", "name": exercise["name"]}
                            )
                            documents.append(doc)
        
        # Division des documents en chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        splits = text_splitter.split_documents(documents)
        
        # Ajout des documents à la base vectorielle
        self.vector_db.add_documents(documents=splits)
        self.vector_db.persist()
    
    def _create_sample_data(self):
        """
        Crée des données d'exemple pour la base de connaissances.
        """
        # Création des répertoires nécessaires
        for directory in ["running", "bodyweight", "strength", "exercises"]:
            os.makedirs(os.path.join(self.data_path, directory), exist_ok=True)
        
        # Création d'exemples de données pour la course à pied
        running_beginner = """
        # Programmation d'Entraînement Course à Pied - Niveau Débutant

        ## Principes généraux
        Pour les débutants en course à pied, l'objectif principal est de construire progressivement l'endurance aérobie
        et de permettre au corps de s'adapter aux impacts de la course. La progression doit être graduelle pour éviter
        les blessures et permettre aux muscles, tendons et articulations de s'adapter.

        ## Structure de base (8-12 semaines)
        - Semaines 1-3: Phase d'introduction - Alternance marche/course
        - Semaines 4-6: Phase de développement - Augmentation progressive du temps de course
        - Semaines 7-10: Phase de consolidation - Courses continues de plus longue durée
        - Semaines 11-12: Phase de test - Évaluation des progrès

        ## Exemples d'exercices
        - Alternance marche (2 min) / course (1 min)
        - Course lente continue (60-70% FCMax)
        - Légers fartleks (accélérations courtes et spontanées)
        - Technique de course (skipping, talons-fesses)

        ## Progression du volume
        - Semaine 1: 3 séances de 20 minutes
        - Semaine 4: 3 séances de 30 minutes
        - Semaine 8: 3-4 séances de 30-40 minutes
        - Semaine 12: 3-4 séances dont une de 45-60 minutes
        """
        
        with open(os.path.join(self.data_path, "running", "beginner_program.txt"), "w", encoding="utf-8") as f:
            f.write(running_beginner)
        
        # Création d'exemples de données pour le poids de corps
        bodyweight_intermediate = """
        # Programmation d'Entraînement Poids de Corps - Niveau Intermédiaire

        ## Principes généraux
        À un niveau intermédiaire en entraînement au poids de corps, l'accent est mis sur la progression en difficulté
        des exercices, l'augmentation du volume et l'introduction de variations plus complexes. Les pratiquants
        intermédiaires possèdent déjà une bonne base de force et de contrôle corporel.

        ## Structure de base (12-16 semaines)
        - Semaines 1-3: Phase d'évaluation et reprise
        - Semaines 4-8: Phase de développement de la force
        - Semaines 9-12: Phase d'endurance musculaire et explosivité
        - Semaines 13-16: Phase avancée avec mouvements complexes

        ## Exemples d'exercices
        - Pompes avec variations (diamant, déclinées, archer)
        - Squats sur une jambe ou pistols partiels
        - Tractions avec variations de prise
        - Dips complets
        - Mountain climbers rapides
        - Burpees avec saut
        - L-sit progressions

        ## Progression du volume
        - Semaine 1: 3 séances, 3 séries par exercice, RPE 7/10
        - Semaine 6: 4 séances, 4 séries par exercice, RPE 8/10
        - Semaine 12: 4-5 séances, avec supersets et circuits, RPE 8-9/10
        - Semaine 16: Circuits complets, introduction d'exercices statiques avancés
        """
        
        with open(os.path.join(self.data_path, "bodyweight", "intermediate_program.txt"), "w", encoding="utf-8") as f:
            f.write(bodyweight_intermediate)
        
        # Création d'exemples de données pour la musculation
        strength_advanced = """
        # Programmation d'Entraînement Musculation - Niveau Avancé

        ## Principes généraux
        Les pratiquants avancés en musculation nécessitent une programmation plus sophistiquée avec périodisation,
        variation des volumes et intensités, et méthodes d'intensification spécifiques. À ce niveau, la progression
        est plus lente et nécessite des stratégies plus complexes.

        ## Structure de base (16 semaines)
        - Semaines 1-4: Phase de volume (hypertrophie)
        - Semaines 5-8: Phase de force
        - Semaines 9-12: Phase de puissance
        - Semaines 13-14: Phase de pic (intensité maximale)
        - Semaines 15-16: Phase de décharge active

        ## Exemples d'exercices
        - Squat, Deadlift, Bench Press avec variations
        - Techniques avancées: rest-pause, drop sets, clusters
        - Exercices olympiques et dérivés
        - Méthodes d'intensification: supersets antagonistes, tri-sets, géants sets
        - Exercices d'isolation pour points faibles spécifiques

        ## Progression du volume/intensité
        - Phase volume: 4-5 séances/semaine, 4-5 exos/séance, 4-5 séries, 8-12 reps, 60-75% 1RM
        - Phase force: 4 séances/semaine, 3-4 exos/séance, 5-6 séries, 3-6 reps, 80-90% 1RM
        - Phase puissance: 4 séances/semaine, 6-8 exos/séance, 3-4 séries, 2-5 reps, 85-95% 1RM
        - Phase pic: 3 séances/semaine, 3-4 exos/séance, 2-3 séries, 1-3 reps, 90-100% 1RM
        - Phase décharge: 2-3 séances/semaine, 4 exos/séance, 2-3 séries, 8-10 reps, 50-60% 1RM
        """
        
        with open(os.path.join(self.data_path, "strength", "advanced_program.txt"), "w", encoding="utf-8") as f:
            f.write(strength_advanced)
        
        # Création d'exemples d'exercices en JSON
        exercises_sample = [
            {
                "name": "Squat",
                "type": "compound",
                "muscles": ["quadriceps", "ischio-jambiers", "fessiers"],
                "level": "tous niveaux",
                "description": "Exercice polyarticulaire ciblant principalement le bas du corps",
                "instructions": "Debout, pieds écartés largeur d'épaules, descendre en pliant les genoux comme pour s'asseoir, en gardant le dos droit et la poitrine haute. Descendre jusqu'à ce que les cuisses soient parallèles au sol, puis remonter."
            },
            {
                "name": "Pompes",
                "type": "compound",
                "muscles": ["pectoraux", "triceps", "épaules", "core"],
                "level": "tous niveaux",
                "description": "Exercice fondamental de poids de corps pour le haut du corps",
                "instructions": "En position de planche, mains légèrement plus écartées que la largeur des épaules, abaisser le corps en pliant les coudes jusqu'à ce que la poitrine frôle le sol, puis pousser pour revenir à la position initiale."
            },
            {
                "name": "Foulées",
                "type": "technique",
                "muscles": ["quadriceps", "ischio-jambiers", "fessiers", "mollets"],
                "level": "débutant",
                "description": "Exercice de technique de course à pied",
                "instructions": "Courir en se concentrant sur une foulée médio-pied, avec une cadence de 170-180 pas par minute, en gardant les épaules relâchées et les bras à un angle de 90 degrés."
            }
        ]
        
        with open(os.path.join(self.data_path, "exercises", "basic_exercises.json"), "w", encoding="utf-8") as f:
            json.dump(exercises_sample, f, indent=2, ensure_ascii=False)
    
    def query(self, query_text, n_results=5):
        """
        Interroge la base de connaissances avec une requête textuelle.
        
        Args:
            query_text: Le texte de la requête
            n_results: Le nombre de résultats à retourner
            
        Returns:
            Les documents les plus pertinents
        """
        return self.vector_db.similarity_search(query_text, k=n_results)
    
    def query_with_metadata_filter(self, query_text, filter_dict, n_results=5):
        """
        Interroge la base de connaissances avec une requête textuelle et un filtre sur les métadonnées.
        
        Args:
            query_text: Le texte de la requête
            filter_dict: Dictionnaire de filtres à appliquer sur les métadonnées
            n_results: Le nombre de résultats à retourner
            
        Returns:
            Les documents les plus pertinents qui correspondent aux filtres
        """
        return self.vector_db.similarity_search(
            query_text,
            k=n_results,
            filter=filter_dict
        )
    
    def get_exercise_by_name(self, exercise_name):
        """
        Récupère les informations sur un exercice par son nom.
        
        Args:
            exercise_name: Le nom de l'exercice
            
        Returns:
            Les informations sur l'exercice
        """
        results = self.query_with_metadata_filter(
            exercise_name,
            {"type": "exercise"},
            n_results=1
        )
        
        if results:
            return results[0]
        return None
    
    def get_discipline_programs(self, discipline, level="all"):
        """
        Récupère les programmes d'entraînement pour une discipline et un niveau donnés.
        
        Args:
            discipline: La discipline (running, bodyweight, strength)
            level: Le niveau (beginner, intermediate, advanced, all)
            
        Returns:
            Les programmes correspondants
        """
        filter_dict = {}
        if level != "all":
            filter_dict["level"] = level
        
        query = f"{discipline} training program {level}"
        return self.query(query)
    
    def add_custom_document(self, content, metadata=None):
        """
        Ajoute un document personnalisé à la base de connaissances.
        
        Args:
            content: Le contenu du document
            metadata: Les métadonnées associées au document
        """
        from langchain.schema import Document
        
        document = Document(page_content=content, metadata=metadata or {})
        
        # Division du document en chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        splits = text_splitter.split_documents([document])
        
        # Ajout des chunks à la base vectorielle
        self.vector_db.add_documents(documents=splits)
        self.vector_db.persist() 