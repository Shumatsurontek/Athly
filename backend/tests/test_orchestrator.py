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
        
        # Patcher la méthode create_structured_chat_agent
        self.agent_patcher = patch('agents.orchestrator.create_structured_chat_agent')
        self.mock_create_agent = self.agent_patcher.start()
        self.mock_create_agent.return_value = MagicMock()
        
        # Patcher la classe AgentExecutor
        self.executor_patcher = patch('agents.orchestrator.AgentExecutor')
        self.mock_executor_class = self.executor_patcher.start()
        self.mock_executor = MagicMock()
        self.mock_executor.invoke = MagicMock(return_value={"output": "Réponse de l'agent"})
        self.mock_executor_class.return_value = self.mock_executor
        
        # Créer l'instance d'OrchestratorAgent à tester
        self.orchestrator = OrchestratorAgent(
            llm=self.mock_llm,
            sport_expert=self.mock_sport_expert,
            table_generator=self.mock_table_generator
        )
    
    def tearDown(self):
        """Nettoyage après les tests."""
        self.agent_patcher.stop()
        self.executor_patcher.stop()
    
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
        self.mock_executor.invoke.assert_called_once()
        self.assertEqual(result, "Réponse de l'agent")
    
    def test_generate_training_program(self):
        """Test que la génération de programme d'entraînement fonctionne."""
        disciplines = ["running", "bodyweight"]
        duration = 8
        level = "débutant"
        goals = "Améliorer l'endurance"
        
        result = self.orchestrator.generate_training_program(
            disciplines=disciplines,
            duration=duration,
            level=level,
            goals=goals
        )
        
        # Vérifier que les méthodes de l'expert sport ont été appelées
        self.mock_sport_expert.generate_program_structure.assert_called_once_with(
            disciplines=disciplines,
            duration=duration,
            level=level,
            goals=goals
        )
        
        self.mock_sport_expert.generate_detailed_program.assert_called_once()
        
        # Vérifier que le générateur de tableaux a été appelé
        self.mock_table_generator.generate_training_table.assert_called_once()
        
        # Vérifier le résultat
        self.assertEqual(result, "Tableau formaté simulé")
    
    def test_error_handling_in_process_chat(self):
        """Test que les erreurs sont correctement gérées dans process_chat."""
        # Configurer le mock pour lever une exception
        self.mock_executor.invoke.side_effect = Exception("Erreur simulée")
        
        # Appeler la méthode et vérifier qu'elle gère l'erreur
        result = self.orchestrator.process_chat("Message qui provoque une erreur")
        
        # Vérifier que la réponse contient un message d'erreur
        self.assertIn("Erreur simulée", result)
        self.assertIn("j'ai rencontré une erreur", result)

if __name__ == '__main__':
    unittest.main() 