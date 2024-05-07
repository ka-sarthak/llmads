from typing import Optional, List

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.llms.ollama import Ollama

llm = Ollama(model='llama3:70b')
llm.base_url = 'http://172.28.105.30/backend'


class Actor(BaseModel):
    """
    Information about the actor appearing as a character in the movie.
    """

    name: Optional[str] = Field(..., description='The name of the actor.')
    role: Optional[str] = Field(
        ..., description='The name of the character that the actor interpreted.'
    )


class Casting(BaseModel):
    """
    Information about the casting of the movie.
    """

    # director: Optional[str] = Field(
    #     ..., description='The name of the director of the movie.'
    # )
    actors: List[Actor]
