import os
import pandas as pd
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class ProgramDataManager:
    """
    Gestionnaire pour les données de programmes d'entraînement stockés dans des fichiers Excel (XLSX).
    Cette classe permet d'extraire et d'analyser des données de programmes pour être utilisées par l'IA.
    """
    
    def __init__(self, programs_dir: str = "./data/programs"):
        """
        Initialise le gestionnaire de données de programmes.
        
        Args:
            programs_dir: Le répertoire contenant les fichiers XLSX de programmes
        """
        self.programs_dir = programs_dir
        os.makedirs(programs_dir, exist_ok=True)
        
    def get_available_programs(self) -> List[str]:
        """
        Récupère la liste des programmes disponibles dans le répertoire.
        
        Returns:
            Liste des noms de fichiers XLSX disponibles
        """
        if not os.path.exists(self.programs_dir):
            return []
            
        return [f for f in os.listdir(self.programs_dir) if f.endswith('.xlsx')]
    
    def extract_program_data(self, filename: str) -> Dict[str, Any]:
        """
        Extrait les données d'un fichier de programme spécifique.
        
        Args:
            filename: Nom du fichier XLSX à analyser
            
        Returns:
            Dictionnaire contenant les données structurées du programme
        """
        file_path = os.path.join(self.programs_dir, filename)
        if not os.path.exists(file_path):
            logger.error(f"Fichier de programme introuvable: {file_path}")
            return {}
        
        try:
            # Charger le fichier Excel
            logger.info(f"Chargement du fichier programme: {file_path}")
            xls = pd.ExcelFile(file_path)
            
            # Récupérer les noms des feuilles
            sheets = xls.sheet_names
            
            # Données du programme
            program_data = {
                "title": os.path.splitext(filename)[0],
                "weeks": {}
            }
            
            # Charger les informations de base si disponibles
            if "Introduction" in sheets:
                intro_df = pd.read_excel(file_path, sheet_name="Introduction")
                if not intro_df.empty and "Introduction" in intro_df.columns:
                    program_data["introduction"] = intro_df["Introduction"].iloc[0]
            
            # Charger chaque semaine
            for sheet in sheets:
                if sheet != "Introduction" and "Semaine" in sheet:
                    week_df = pd.read_excel(file_path, sheet_name=sheet)
                    
                    # S'assurer que le DataFrame n'est pas vide
                    if not week_df.empty:
                        # Convertir le DataFrame en dictionnaire structuré
                        week_data = []
                        for _, row in week_df.iterrows():
                            week_data.append(dict(row))
                        
                        # Ajouter les données de la semaine
                        program_data["weeks"][sheet] = week_data
            
            return program_data
        
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction des données du programme {filename}: {str(e)}")
            return {}
    
    def search_program_by_criteria(self, 
                                  discipline: Optional[str] = None, 
                                  level: Optional[str] = None, 
                                  duration: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Recherche des programmes correspondant à des critères spécifiques.
        
        Args:
            discipline: Discipline sportive (course, musculation, etc.)
            level: Niveau du pratiquant (débutant, intermédiaire, avancé)
            duration: Durée du programme en semaines
            
        Returns:
            Liste des programmes correspondant aux critères
        """
        results = []
        
        for filename in self.get_available_programs():
            # Vérifier si le nom du fichier contient les critères de recherche
            filename_lower = filename.lower()
            
            matches_criteria = True
            
            if discipline and discipline.lower() not in filename_lower:
                matches_criteria = False
                
            if level and level.lower() not in filename_lower:
                matches_criteria = False
                
            if duration:
                # Chercher le nombre de semaines dans le nom du fichier
                if str(duration) not in filename and f"{duration}sem" not in filename_lower:
                    matches_criteria = False
            
            if matches_criteria:
                program_data = self.extract_program_data(filename)
                if program_data:
                    program_data["filename"] = filename
                    results.append(program_data)
        
        return results
    
    def get_program_summary(self, filename: str) -> str:
        """
        Génère un résumé textuel du programme pour utilisation par l'IA.
        
        Args:
            filename: Nom du fichier de programme
            
        Returns:
            Résumé textuel du programme
        """
        program_data = self.extract_program_data(filename)
        if not program_data:
            return "Programme non trouvé ou invalide."
        
        summary = f"# {program_data['title']}\n\n"
        
        # Ajouter l'introduction si disponible
        if "introduction" in program_data:
            summary += f"{program_data['introduction']}\n\n"
        
        # Ajouter un résumé de chaque semaine
        for week_name, week_data in program_data.get("weeks", {}).items():
            summary += f"## {week_name}\n\n"
            
            if week_data:
                # Créer un tableau markdown
                headers = list(week_data[0].keys())
                summary += "| " + " | ".join(headers) + " |\n"
                summary += "| " + " | ".join(["---"] * len(headers)) + " |\n"
                
                for session in week_data:
                    summary += "| " + " | ".join([str(session.get(h, "")) for h in headers]) + " |\n"
                
                summary += "\n"
        
        return summary 