from typing import Optional

from langchain_core.pydantic_v1 import BaseModel
from langchain_community.llms.ollama import Ollama
from langchain.output_parsers.pydantic import PydanticOutputParser
# from langchain.output_parsers.yaml import YamlOutputParser

from langchain_core.prompts import ChatPromptTemplate

from llmad.llm_model import llm, Casting
# from llmad.simulation_model import yaml_schema


def prompt_query(
    query: str = '', schema: BaseModel = Casting, llm: Ollama = llm
) -> Optional[BaseModel]:
    """
    Prompt the user with a `query` and return the output as a Pydantic object whose Fields are populated by the `llm` parsing.

    Args:
        query (str, optional): The string to be parsed into the `pydantic_object`. Defaults to ''.
        schema (BaseModel, optional): The `BaseModel` with Fields to be populated. Defaults to None. Defined in the `llm_model.py` module.
        llm (Ollama, optional): The LLM used for parsing. Defaults to `Ollama`.

    Returns:
        (Optional[BaseModel]): The populated `BaseModel`.
    """
    if schema is None:
        raise ValueError('`schema` must be provided to be a defined `BaseModel`.')
    # improve this with our own NOMADOutputParser (and `get_format_instructions()` method)
    parser = PydanticOutputParser(pydantic_object=schema)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                'system',
                'Answer the user query. Wrap the output in ```json``` tags\n{format_instructions}',
            ),  # TODO improve this prompting to be specific for our cases
            ('human', '{query}'),
        ]
    ).partial(format_instructions=parser.get_format_instructions())
    chain = prompt | llm | parser
    try:
        return chain.invoke({'query': query})
    except Exception:
        return None


# f = open('/home/josepizarro/LLM-Hackathon-2024/tests/data/example.out', 'r')
# text = f.read()

question = 'What is the casting of Star Wars the first episode?'
query = llm.invoke(question)
print(prompt_query(query=query))
