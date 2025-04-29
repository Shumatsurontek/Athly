from huggingface_hub import InferenceClient
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, List, Optional, Dict
import os
from dotenv import load_dotenv
import logging
from pydantic import Field, PrivateAttr
import requests
import re

logger = logging.getLogger(__name__)

load_dotenv()

class QwenLLM(LLM):
    """
    LangChain wrapper for LLMs via Hugging Face Inference API.
    """
    
    # Champs publics Pydantic
    model_name: str = Field(default="Qwen/QwQ-32B", description="The name of the model to use")
    max_tokens: int = Field(default=1500, description="Maximum number of tokens to generate")
    temperature: float = Field(default=0.3, description="Sampling temperature")
    timeout: int = Field(default=120, description="Timeout in seconds for API calls")
    
    # Attributs privés (non inclus dans le schéma)
    _client: Any = PrivateAttr(default=None)
    _api_key: str = PrivateAttr(default="")
    
    def __init__(self, **kwargs):
        """
        Initialise LLM avec Hugging Face
        """
        # Extraire l'API key des kwargs avant l'initialisation Pydantic
        api_key = kwargs.pop("api_key", None) or os.environ.get("HUGGINGFACE_API_KEY")
        if not api_key:
            raise ValueError("No Hugging Face API key provided")
        
        # Initialisation parent avec les paramètres Pydantic
        super().__init__(**kwargs)
        
        # Configurer les attributs privés après l'initialisation Pydantic
        self._api_key = api_key
        
        # Créer le client
        self._client = InferenceClient(
            provider="hf-inference",
            api_key=api_key
        )
        
        logger.info(f"Initialized HF LLM with model: {self.model_name} (timeout: {self.timeout}s)")
    
    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "huggingface_inference"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs
    ) -> str:
        """
        Call the model with the given prompt.
        
        Args:
            prompt: The prompt to send to the model
            stop: List of strings to stop generation when encountered
            run_manager: CallbackManager for LLM run
            
        Returns:
            Generated text
        """
        # Log first part of prompt
        logger.debug(f"Calling Qwen model with prompt: {prompt[:100]}...")
        
        try:
            # Add instruction to respond directly
            enhanced_prompt = f"{prompt}\n\nRÉPONDS DIRECTEMENT À L'UTILISATEUR SANS MONTRER TON RAISONNEMENT INTERNE."
            
            # Prepare message for chat completion
            messages = [
                {
                    "role": "user",
                    "content": enhanced_prompt
                }
            ]
            
            # Make API call
            completion = self._client.chat_completion(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Extract response text
            response = completion.choices[0].message.content
            
            # Filter out thinking process just in case
            response = self._filter_thinking(response)
            
            # Log first part of response
            logger.debug(f"Qwen model response: {response[:100]}...")
            
            return response
        
        except Exception as e:
            logger.error(f"Error calling HF Inference API: {e}")
            raise
    
    def _filter_thinking(self, text: str) -> str:
        """
        Filter out the thinking process from the model's response.
        
        Args:
            text: The original response text
        
        Returns:
            Filtered text without the thinking parts
        """
        # Check if there's any indication of internal thinking
        if "Wait," in text or "Hmm," in text or "Let me" in text:
            # Try to find the actual response after the thinking process
            # Common patterns that indicate the end of thinking
            patterns = [
                r"^(.*?Wait,.*?)(So,\s*)(.*?)$",
                r"^(.*?Let me.*?)(Here's\s*)(.*?)$",
                r"^(.*?Hmm,.*?)(To summarize,\s*)(.*?)$",
                r"^(.*?I need to.*?)(In conclusion,\s*)(.*?)$"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.DOTALL)
                if match and match.group(3):
                    # Return the part after the thinking
                    return match.group(3).strip()
            
            # If we couldn't extract a clear response, use a simpler approach:
            # Split by sentences and skip the ones with thinking patterns
            sentences = re.split(r'(?<=[.!?])\s+', text)
            filtered_sentences = []
            
            skip_patterns = ["Wait,", "Hmm,", "Let me", "I should", "I need to", 
                            "Maybe", "The user mentioned", "I'll", "Also,"]
            
            for sentence in sentences:
                if not any(pattern in sentence for pattern in skip_patterns):
                    filtered_sentences.append(sentence)
            
            # Join the filtered sentences
            if filtered_sentences:
                return " ".join(filtered_sentences)
        
        # Format the response for better readability
        # Add line breaks before numbered list items
        text = re.sub(r'(\d+\. )', r'\n\n\1', text)
        
        # Add line breaks before bullet points
        text = re.sub(r'(- )', r'\n\n\1', text)
        
        # Add double line breaks before headers
        text = re.sub(r'(#+\s+)', r'\n\n\1', text)
        
        # Ensure proper spacing around strong/bold text
        text = re.sub(r'(\*\*[^*]+\*\*)', r' \1 ', text)
        
        # Improve table formatting
        text = re.sub(r'\n\|\s*', r'\n| ', text)
        
        # If no thinking patterns detected, return the formatted text
        return text
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout
        } 