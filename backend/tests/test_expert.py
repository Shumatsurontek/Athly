import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import logging

# Ajout du chemin du projet au path pour permettre les importations
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.expert import SportExpertAgent
from models.knowledge_base import KnowledgeBase

# Configuration du logging pour les tests
logging.basicConfig(level=logging.ERROR)

class TestSportExpertAgent(unittest.TestCase):
    """Tests pour l'agent expert en sport."""
    
    def setUp(self):
        """Configuration des mocks et de l'agent pour les tests."""
        # Créer des mocks pour les dépendances
        self.mock_llm = MagicMock()
        self.mock_llm.invoke = MagicMock(return_value="Réponse simulée du LLM")
        
        self.mock_knowledge_base = MagicMock(spec=KnowledgeBase)
        self.mock_knowledge_base.query = MagicMock(return_value=[
            MagicMock(page_content="Contenu de test sur l'endurance"),
            MagicMock(page_content="Contenu de test sur la musculation")
        ])
        
        # Créer l'instance de SportExpertAgent à tester
        self.sport_expert = SportExpertAgent(
            llm=self.mock_llm,
            knowledge_base=self.mock_knowledge_base
        )
    
    def test_initialization(self):
        """Test que l'agent est correctement initialisé."""
        self.assertEqual(self.sport_expert.llm, self.mock_llm)
        self.assertEqual(self.sport_expert.knowledge_base, self.mock_knowledge_base)
        self.assertIsNotNone(self.sport_expert.advice_prompt)
        self.assertIsNotNone(self.sport_expert.structure_prompt)
        self.assertIsNotNone(self.sport_expert.detailed_prompt)
    
    def test_generate_advice(self):
        """Test que la génération de conseils fonctionne."""
        query = "Comment améliorer mon endurance en course à pied?"
        result = self.sport_expert.generate_advice(query)
        
        # Vérifier que la base de connaissances a été consultée
        self.mock_knowledge_base.query.assert_called_once_with(query)
        
        # Vérifier que le LLM a été appelé avec un prompt
        self.mock_llm.invoke.assert_called_once()
        args = self.mock_llm.invoke.call_args[0]
        self.assertIsNotNone(args[0])  # Le prompt passé au LLM
        
        # Vérifier le résultat
        self.assertEqual(result, "Réponse simulée du LLM")
    
    def test_generate_program_structure(self):
        """Test que la génération de structure de programme fonctionne."""
        disciplines = ["running", "bodyweight"]
        duration = 8
        level = "débutant"
        goals = "Améliorer l'endurance"
        
        result = self.sport_expert.generate_program_structure(
            disciplines=disciplines,
            duration=duration,
            level=level,
            goals=goals
        )
        
        # Vérifier que la base de connaissances a été consultée
        self.mock_knowledge_base.query.assert_called_once()
        query_arg = self.mock_knowledge_base.query.call_args[0][0]
        self.assertIn("running", query_arg)
        self.assertIn("bodyweight", query_arg)
        self.assertIn("débutant", query_arg)
        
        # Vérifier que le LLM a été appelé avec un prompt
        self.mock_llm.invoke.assert_called_once()
        
        # Vérifier le résultat
        self.assertEqual(result, "Réponse simulée du LLM")
    
    def test_generate_detailed_program(self):
        """Test que la génération de programme détaillé fonctionne."""
        structure = "Structure simulée du programme"
        constraints = "Douleur genou droit"
        equipment = "Haltères, bandes élastiques"
        frequency = (4)
        time_per_session = 45
        
        result = self.sport_expert.generate_detailed_program(
            structure=structure,
            constraints=constraints,
            equipment=equipment,
            frequency=frequency,
            time_per_session=time_per_session
        )
        
        # Vérifier que le LLM a été appelé avec un prompt
        self.mock_llm.invoke.assert_called_once()
        args = self.mock_llm.invoke.call_args[0]
        prompt = args[0]
        
        # Vérifier que les paramètres sont inclus dans le prompt
        # Dans les nouvelles versions de LangChain, convertir le prompt en string pour vérifier son contenu
        prompt_str = str(prompt)
        self.assertIn(structure, prompt_str)
        
        # Vérifier le résultat
        self.assertEqual(result, "Réponse simulée du LLM")
    
    @patch('agents.expert.SportExpertAgent._load_advice_prompt')
    @patch('agents.expert.SportExpertAgent._load_structure_prompt')
    @patch('agents.expert.SportExpertAgent._load_detailed_prompt')
    def test_prompt_loading(self, mock_detailed, mock_structure, mock_advice):
        """Test que les prompts sont correctement chargés."""
        mock_advice.return_value = "Advice Prompt"
        mock_structure.return_value = "Structure Prompt"
        mock_detailed.return_value = "Detailed Prompt"
        
        expert = SportExpertAgent(self.mock_llm, self.mock_knowledge_base)
        
        mock_advice.assert_called_once()
        mock_structure.assert_called_once()
        mock_detailed.assert_called_once()
        
        self.assertEqual(expert.advice_prompt, "Advice Prompt")
        self.assertEqual(expert.structure_prompt, "Structure Prompt")
        self.assertEqual(expert.detailed_prompt, "Detailed Prompt")
    
    def test_error_handling(self):
        """Test que les erreurs sont correctement gérées."""
        # Configurer le mock pour lever une exception
        self.mock_llm.invoke.side_effect = Exception("Erreur LLM simulée")
        
        # Essayer de générer des conseils et vérifier que l'exception est propagée
        with self.assertRaises(Exception) as context:
            self.sport_expert.generate_advice("Une question")
        
        # Vérifier le message d'erreur
        self.assertIn("Erreur LLM simulée", str(context.exception))

if __name__ == '__main__':
    unittest.main() 