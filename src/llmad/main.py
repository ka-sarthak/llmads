import json
import re
from typing import Optional, List

from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate

from llmad.llm_model import nomad_schema

llm = Ollama(model='llama3:70b')
llm.base_url = 'http://172.28.105.30/backend'


# Custom extraction for JSON content
def extract_json(message: str = '') -> List[dict]:
    """Extracts JSON content from a string where JSON is embedded between ```json and ``` tags.

    Parameters:
        message (str): The text containing the JSON content.

    Returns:
        (list): A list of extracted JSON strings.
    """
    # Define the regular expression pattern to match JSON blocks
    pattern = r'```\njson(.*?)```'

    # Find all non-overlapping matches of the pattern in the string
    matches = re.findall(pattern, message, re.DOTALL)

    # Return the list of matched JSON strings, stripping any leading or trailing whitespace
    try:
        return [json.loads(match.strip()) for match in matches]
    except Exception:
        raise ValueError(f'Failed to parse: {message}')


def prompt_query(
    query: str = '', schema: dict = {}, llm: Ollama = llm
) -> Optional[dict]:
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
        raise ValueError('`schema` must be provided.')
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                'system',
                'You are an expert extraction algorithm. Only extract the relevant information from the text. '
                'If you do not know the value of an attribute asked to extract, just skip it and do not store it. '
                'Take into account that the schema alsways starts at the level of the `data` key. Thus, the JSON '
                'snippet should maintain this structure. For example, if the data only populates `program` and its `name`, then the '
                'output JSON should be: ```json\n{{"data": {{"program": {{"name": "VASP"}}}}}}\n```. If now the data is recognized to populate '
                'the `version as well, then the output JSON should be: ```json\n{{"data": {{"program": {{"name": "VASP", "version": "5.4"}}}}}}\n```.'
                'Output your answer as JSON that matches the given schema: ```json\n{schema}\n```'
                'Make sure to wrap the answer in ```json and ``` tags.',
            ),
            ('human', '{query}'),
        ]
    ).partial(schema=schema)
    chain = prompt | llm | extract_json
    try:
        return chain.invoke({'query': query})
    except Exception:
        return None


f = open('/home/josepizarro/LLM-Hackathon-2024/tests/data/example.out', 'r')
query = f.read()
llm_data = prompt_query(query=query, schema=nomad_schema)
print(llm_data)
