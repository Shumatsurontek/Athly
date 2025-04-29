from typing import Annotated, Dict, List, Literal, TypedDict, Any, Optional
import logging
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
import json
import traceback

logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    # Messages entre l'utilisateur et l'agent
    messages: Annotated[list, add_messages]
    # État interne
    context: Dict[str, Any]

class AgentGraph:
    """
    Implémentation d'un agent avec LangGraph pour faciliter le suivi d'état
    et les logs détaillés.
    """
    
    def __init__(self, llm, tools=None, logger=None):
        """Initialise l'agent graph avec un LLM et des outils optionnels."""
        self.llm = llm
        self.tools = tools or []
        self.logger = logger or logging.getLogger(__name__)
        self.graph = self._create_graph()
        
    def _create_graph(self):
        """Crée le graphe d'état pour l'agent."""
        try:
            # Wrapping des outils pour le logging
            wrapped_tools = self._wrap_tools_with_logging(self.tools)
            
            # Création du nœud d'outils
            tool_node = ToolNode(wrapped_tools) if wrapped_tools else None
            
            # Définition du graphe d'état
            workflow = StateGraph(AgentState)
            
            # Nœud de l'agent principal
            workflow.add_node("agent", self._call_model)
            
            # Nœud pour les outils si disponibles
            if tool_node:
                workflow.add_node("tools", tool_node)
                
            # Point d'entrée
            workflow.add_edge(START, "agent")
            
            # Conditional edge pour décider si on continue avec les outils ou on termine
            if tool_node:
                workflow.add_conditional_edges(
                    "agent",
                    self._should_continue,
                )
                workflow.add_edge("tools", "agent")
            else:
                workflow.add_edge("agent", END)
            
            # Compiler le graphe
            return workflow.compile()
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du graphe: {str(e)}")
            self.logger.error(traceback.format_exc())
            raise
    
    def _wrap_tools_with_logging(self, tools):
        """Enveloppe les outils avec des logs pour suivre leur utilisation."""
        wrapped_tools = []
        
        for tool in tools:
            original_func = tool.func
            
            def wrapped_func(*args, **kwargs):
                tool_name = original_func.__name__
                self.logger.info(f"EXÉCUTION OUTIL: {tool_name} - Arguments: {json.dumps(args)} {json.dumps(kwargs)}")
                try:
                    result = original_func(*args, **kwargs)
                    self.logger.info(f"RÉSULTAT OUTIL {tool_name}: {result[:100]}..." if isinstance(result, str) else f"RÉSULTAT OUTIL {tool_name}: {result}")
                    return result
                except Exception as e:
                    self.logger.error(f"ERREUR OUTIL {tool_name}: {str(e)}")
                    raise
            
            # Copier l'outil avec la nouvelle fonction
            new_tool = tool.copy()
            new_tool.func = wrapped_func
            wrapped_tools.append(new_tool)
        
        return wrapped_tools
    
    def _should_continue(self, state: AgentState) -> Literal["tools", END]:
        """Détermine si l'exécution doit continuer avec les outils ou se terminer."""
        messages = state['messages']
        last_message = messages[-1]
        
        self.logger.debug(f"DÉCISION CONTINUITÉ: Message: {last_message}")
        
        # Si l'agent fait un appel d'outil, router vers "tools"
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            self.logger.info(f"DÉCISION: Continuer avec les outils: {last_message.tool_calls}")
            return "tools"
        
        # Sinon, terminer la conversation
        self.logger.info("DÉCISION: Fin de la conversation")
        return END
    
    def _call_model(self, state: AgentState):
        """Appelle le modèle avec l'état actuel."""
        messages = state['messages']
        context = state.get('context', {})
        
        self.logger.info(f"APPEL MODEL: Nombre de messages: {len(messages)}")
        self.logger.debug(f"CONTEXTE: {json.dumps(context)}")
        
        try:
            response = self.llm.invoke(messages)
            self.logger.info(f"RÉPONSE MODEL: {response.content[:100]}...")
            return {"messages": [response]}
        except Exception as e:
            self.logger.error(f"ERREUR APPEL MODEL: {str(e)}")
            error_message = AIMessage(content=f"Désolé, j'ai rencontré une erreur. Veuillez réessayer.")
            return {"messages": [error_message]}
    
    def process_message(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Traite un message utilisateur et retourne la réponse.
        
        Args:
            user_message: Le message de l'utilisateur
            context: Contexte supplémentaire pour le traitement
            
        Returns:
            La réponse de l'agent
        """
        self.logger.info(f"NOUVEAU MESSAGE: {user_message[:50]}...")
        
        # Initialiser l'état
        initial_state = {
            "messages": [HumanMessage(content=user_message)],
            "context": context or {}
        }
        
        # Exécuter le graphe
        self.logger.info("DÉMARRAGE EXÉCUTION AGENT")
        try:
            result = self.graph.invoke(initial_state)
            messages = result["messages"]
            
            # Récupérer la réponse finale
            if messages and len(messages) > 1:
                final_message = messages[-1]
                if isinstance(final_message, AIMessage):
                    self.logger.info(f"RÉPONSE FINALE: {final_message.content[:100]}...")
                    return final_message.content
            
            # Fallback si pas de réponse claire
            self.logger.warning("Pas de réponse claire de l'agent")
            return "Désolé, je n'ai pas pu générer une réponse."
            
        except Exception as e:
            self.logger.error(f"ERREUR TRAITEMENT: {str(e)}")
            return f"Désolé, une erreur s'est produite: {str(e)}" 