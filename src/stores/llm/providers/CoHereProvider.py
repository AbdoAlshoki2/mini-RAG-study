from ..LLMInterface import LLMInterface
from ..LLMEnum import CoHereEnum, DocumentTypeEnum
import cohere 
import logging


class CoHereProvider(LLMInterface):
    def __init__(self, api_key: str,
                    default_input_max_input_characters: int = 1000,
                    default_generation_output_max_output_tokens: int = 1000,
                    default_generation_temperature: float = 0.1):

        self.api_key = api_key

        self.default_input_max_input_characters = default_input_max_input_characters
        self.default_generation_output_max_output_tokens = default_generation_output_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.ClientV2(
            api_key= self.api_key,
        )

        self.logger = logging.getLogger(__name__)


    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id


    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_input_characters].strip()


    def generate_text(self, prompt: str, chat_histor: list = [], max_output_tokens: int = None,
                        temperature: float = None):
        
        if not self.client:
            self.logger.error("Cohere client is not initialized")
            return None

        if not self.generation_model_id:
            self.logger.error("Cohere generation model is not set")
            return None


        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_output_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt, CoHereEnum.USER.value)
        )

        response = self.client.chat(
            model= self.generation_model_id,
            messages= chat_history,
            max_tokens= max_output_tokens,
            temperature= temperature
        )

        if not response or not response.message or not response.message.content:
            self.logger.error("Error while generating text with Cohere")
            return None

        return response.message.content



    def embed_text(self, text: str, document_type: str = None):
        
        if not self.client:
            self.logger.error("Cohere client is not initialized")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Cohere embedding model is not set")
            return None
        
        if not self.embedding_size:
            self.logger.error("Cohere embedding size is not set")
            return None

        input_type = CoHereEnum.DOCUMENT.value
        if document_type == DocumentTypeEnum.QUERY.value:
            input_type = CoHereEnum.QUERY.value

        response = self.client.embed(
            model= self.embedding_model_id,
            input_type= input_type,
            texts= [self.process_text(text)],
            embedding_type= ['float'],
            output_dimension= self.embedding_size
        )

        if not response or not response.embeddings or response.embeddings.float or not len(response.embeddings.float)==0:
            self.logger.error("Error while embedding text with Cohere")
            return None
        
        return response.embeddings.float[0]


    def construct_prompt(self, prompt:str , role:str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }

