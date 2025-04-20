import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import logging

# Ajout du chemin du projet au path pour permettre les importations
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import OrchestratorAgent
from agents.expert import SportExpertAgent
from agents.table_generator import TableGeneratorAgent
from models.knowledge_base import KnowledgeBase

# Configuration du logging pour les tests
logging.basicConfig(level=logging.ERROR)

class TestOrchestratorAgent(unittest.TestCase):
    """Tests pour l'agent orchestrateur."""
    
    def setUp(self):
        """Configuration des mocks et de l'agent pour les tests."""
        # Créer des mocks pour les dépendances
        self.mock_llm = MagicMock()
        self.mock_llm.invoke = MagicMock(return_value="Réponse simulée du LLM")
        
        self.mock_knowledge_base = MagicMock(spec=KnowledgeBase)
        self.mock_knowledge_base.query = MagicMock(return_value=[MagicMock(page_content="Contenu de test")])
        
        # Créer des mocks pour les agents spécialisés
        self.mock_sport_expert = MagicMock(spec=SportExpertAgent)
        self.mock_sport_expert.generate_advice = MagicMock(return_value="Conseil d'expert simulé")
        self.mock_sport_expert.generate_program_structure = MagicMock(return_value="Structure de programme simulée")
        self.mock_sport_expert.generate_detailed_program = MagicMock(return_value="Programme détaillé simulé")
        
        self.mock_table_generator = MagicMock(spec=TableGeneratorAgent)
        self.mock_table_generator.generate_training_table = MagicMock(return_value="Tableau formaté simulé")
        
        # Patcher la méthode initialize_agent
        self.agent_patcher = patch('agents.orchestrator.initialize_agent')
        self.mock_initialize_agent = self.agent_patcher.start()
        
        # Créer un mock pour l'agent_executor retourné par initialize_agent
        self.mock_agent_executor = MagicMock()
        self.mock_agent_executor.run = MagicMock(return_value="Réponse de l'agent")
        
        # Configurer initialize_agent pour retourner notre mock
        self.mock_initialize_agent.return_value = self.mock_agent_executor
        
        # Créer l'instance d'OrchestratorAgent à tester
        self.orchestrator = OrchestratorAgent(
            llm=self.mock_llm,
            sport_expert=self.mock_sport_expert,
            table_generator=self.mock_table_generator
        )
    
    def tearDown(self):
        """Nettoyage après les tests."""
        self.agent_patcher.stop()
    
    def test_initialization(self):
        """Test que l'agent est correctement initialisé."""
        self.assertEqual(self.orchestrator.llm, self.mock_llm)
        self.assertEqual(self.orchestrator.sport_expert, self.mock_sport_expert)
        self.assertEqual(self.orchestrator.table_generator, self.mock_table_generator)
        self.assertIsNotNone(self.orchestrator.memory)
        self.assertEqual(len(self.orchestrator.tools), 2)
        self.assertEqual(self.orchestrator.tools[0].name, "expert_sport")
        self.assertEqual(self.orchestrator.tools[1].name, "table_generator")
    
    def test_call_sport_expert(self):
        """Test que l'appel à l'expert sport fonctionne."""
        result = self.orchestrator._call_sport_expert("Comment améliorer mon endurance?")
        self.mock_sport_expert.generate_advice.assert_called_once_with("Comment améliorer mon endurance?")
        self.assertEqual(result, "Conseil d'expert simulé")
    
    def test_call_table_generator(self):
        """Test que l'appel au générateur de tableaux fonctionne."""
        result = self.orchestrator._call_table_generator("Données du programme", "markdown")
        self.mock_table_generator.generate_training_table.assert_called_once_with("Données du programme", "markdown")
        self.assertEqual(result, "Tableau formaté simulé")
    
    def test_process_chat(self):
        """Test que le traitement de chat fonctionne."""
        result = self.orchestrator.process_chat("Je veux un programme de course à pied")
        self.mock_agent_executor.run.assert_called_once_with("Je veux un programme de course à pied")
        self.assertEqual(result, "Réponse de l'agent")
    
    def test_generate_training_program(self):
        """Test que la génération de programme d'entraînement fonctionne."""
        disciplines = ["running", "bodyweight"]
        duration = 8
        level = "débutant"
        goals = "Améliorer l'endurance"
        
        # Configuration du timeout
        self.mock_agent_executor.agent_executor = MagicMock()
        self.mock_agent_executor.agent_executor.timeout = 60
        
        result = self.orchestrator.generate_training_program(
            disciplines=disciplines,
            duration=duration,
            level=level,
            goals=goals
        )
        
        # Vérifier que run a été appelé avec la bonne requête
        self.mock_agent_executor.run.assert_called()
        call_args = self.mock_agent_executor.run.call_args[0][0]
        self.assertIn("running, bodyweight", call_args)
        self.assertIn("débutant", call_args)
        self.assertIn("8 semaines", call_args)
        
        # Vérifier que le timeout a été temporairement modifié
        self.assertEqual(self.mock_agent_executor.agent_executor.timeout, 60)
        
        # Vérifier le résultat
        self.assertEqual(result, "Réponse de l'agent")
    
    def test_error_handling_in_process_chat(self):
        """Test que les erreurs sont correctement gérées dans process_chat."""
        # Configurer le mock pour lever une exception
        self.mock_agent_executor.run.side_effect = Exception("Erreur simulée")
        
        # Appeler la méthode et vérifier qu'elle gère l'erreur
        result = self.orchestrator.process_chat("Message qui provoque une erreur")
        
        # Vérifier que la réponse contient un message d'erreur
        self.assertIn("Erreur simulée", result)
        self.assertIn("j'ai rencontré une erreur", result)

if __name__ == '__main__':
    unittest.main() 