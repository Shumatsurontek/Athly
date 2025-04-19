import unittest
import os
import sys
import logging
from unittest.mock import patch, MagicMock

# Ajout du chemin du projet au path pour permettre les importations
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import OrchestratorAgent
from agents.expert import SportExpertAgent
from agents.table_generator import TableGeneratorAgent
from models.knowledge_base import KnowledgeBase

# Configuration du logging pour les tests
logging.basicConfig(level=logging.ERROR)

class TestAgentIntegration(unittest.TestCase):
    """Tests d'intégration pour le workflow agentic complet."""
    
    @patch('langchain.chat_models.ChatMistralAI')
    def setUp(self, mock_chat_mistral):
        """Mise en place des tests avec mocks pour éviter les appels API réels."""
        # Configurer le mock pour ChatMistralAI
        self.mock_llm = mock_chat_mistral.return_value
        self.mock_llm.invoke = MagicMock(return_value="Réponse simulée du LLM")
        
        # Créer une base de connaissances mock
        self.mock_knowledge_base = MagicMock(spec=KnowledgeBase)
        self.mock_knowledge_base.query = MagicMock(return_value=[
            MagicMock(page_content="Contenu de test sur l'endurance"),
            MagicMock(page_content="Contenu de test sur la musculation")
        ])
        
        # Patcher les méthodes liées au chat Langchain pour l'orchestrateur
        self.agent_patcher = patch('agents.orchestrator.create_structured_chat_agent')
        self.executor_patcher = patch('agents.orchestrator.AgentExecutor')
        
        self.mock_create_agent = self.agent_patcher.start()
        self.mock_executor_class = self.executor_patcher.start()
        
        # Configurer les mocks
        self.mock_agent = MagicMock()
        self.mock_create_agent.return_value = self.mock_agent
        
        self.mock_executor = MagicMock()
        self.mock_executor.invoke = MagicMock(return_value={"output": "Réponse du workflow agentic"})
        self.mock_executor_class.return_value = self.mock_executor
        
        # Créer les instances d'agents réels
        self.sport_expert = SportExpertAgent(self.mock_llm, self.mock_knowledge_base)
        self.table_generator = TableGeneratorAgent(self.mock_llm)
        
        # Créer l'orchestrateur avec les agents réels
        self.orchestrator = OrchestratorAgent(
            llm=self.mock_llm,
            sport_expert=self.sport_expert,
            table_generator=self.table_generator
        )
    
    def tearDown(self):
        """Nettoyage après les tests."""
        self.agent_patcher.stop()
        self.executor_patcher.stop()
    
    def test_chat_workflow(self):
        """Test du workflow complet de chat."""
        # Simuler une demande de conseil
        user_message = "Comment puis-je améliorer ma technique de course à pied?"
        
        # Envoyer la demande à l'orchestrateur
        response = self.orchestrator.process_chat(user_message)
        
        # Vérifier que l'exécuteur a été appelé correctement
        self.mock_executor.invoke.assert_called_once()
        invoke_args = self.mock_executor.invoke.call_args[0][0]
        self.assertEqual(invoke_args["input"], user_message)
        
        # Vérifier la réponse
        self.assertEqual(response, "Réponse du workflow agentic")
    
    def test_training_program_generation_workflow(self):
        """Test du workflow complet de génération de programme d'entraînement."""
        # Configurer le sport expert pour renvoyer des réponses spécifiques
        self.sport_expert.generate_program_structure = MagicMock(return_value="Structure de programme simulée")
        self.sport_expert.generate_detailed_program = MagicMock(return_value="Programme détaillé simulé")
        
        # Configurer le générateur de tableaux
        self.table_generator.generate_training_table = MagicMock(return_value="Tableau formaté simulé")
        
        # Paramètres pour la génération du programme
        disciplines = ["running", "bodyweight"]
        duration = 8
        level = "débutant"
        goals = "Améliorer l'endurance"
        constraints = "Douleur au genou droit"
        equipment = "Haltères, bandes élastiques"
        frequency = 3
        time_per_session = 45
        
        # Générer le programme
        result = self.orchestrator.generate_training_program(
            disciplines=disciplines,
            duration=duration,
            level=level,
            goals=goals,
            constraints=constraints,
            equipment=equipment,
            frequency=frequency,
            time_per_session=time_per_session
        )
        
        # Vérifier les appels aux méthodes des agents spécialisés
        self.sport_expert.generate_program_structure.assert_called_once_with(
            disciplines=disciplines,
            duration=duration,
            level=level,
            goals=goals
        )
        
        self.sport_expert.generate_detailed_program.assert_called_once_with(
            structure="Structure de programme simulée",
            constraints=constraints,
            equipment=equipment,
            frequency=frequency,
            time_per_session=time_per_session
        )
        
        self.table_generator.generate_training_table.assert_called_once_with("Programme détaillé simulé")
        
        # Vérifier le résultat final
        self.assertEqual(result, "Tableau formaté simulé")
    
    def test_error_propagation(self):
        """Test que les erreurs dans un agent sont correctement propagées et gérées."""
        # Faire en sorte que l'agent expert lève une exception
        self.sport_expert.generate_program_structure = MagicMock(side_effect=Exception("Erreur dans la génération de structure"))
        
        # Tenter de générer un programme
        with self.assertRaises(Exception) as context:
            self.orchestrator.generate_training_program(
                disciplines=["running"],
                duration=8,
                level="débutant",
                goals="Améliorer l'endurance"
            )
        
        # Vérifier que l'erreur a été propagée
        self.assertIn("Erreur dans la génération de structure", str(context.exception))
    
    @patch('agents.expert.SportExpertAgent.generate_advice')
    def test_expert_tool_invocation(self, mock_generate_advice):
        """Test que l'outil expert_sport est correctement invoqué par l'orchestrateur."""
        # Configurer le mock
        mock_generate_advice.return_value = "Conseil d'expert spécifique"
        
        # Utiliser l'outil expert_sport via l'orchestrateur
        result = self.orchestrator._call_sport_expert("Comment améliorer ma VO2max?")
        
        # Vérifier que la méthode generate_advice a été appelée correctement
        mock_generate_advice.assert_called_once_with("Comment améliorer ma VO2max?")
        
        # Vérifier le résultat
        self.assertEqual(result, "Conseil d'expert spécifique")

if __name__ == '__main__':
    unittest.main() 