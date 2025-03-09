from typing import (
    TYPE_CHECKING,
    Union,
    Generator,
)
import json
from langchain_community.llms.ollama import Ollama
from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

if TYPE_CHECKING:
    from pydantic import BaseModel


class HULlama:
    """
    Model for llama3 hosted at HU Berlin.
    """

    def __init__(self, schema: 'BaseModel'):
        llm = Ollama(model='llama3:70b')
        llm.base_url = 'http://172.28.105.30/backend'
        self.llm = llm
        self.schema = schema

    def generate_prompt(self, content: list[str]) -> Generator[str, None, None]:
        """
        Generate a prompt for the given content.

        Args:
            content (list[str]): The list of strings containing the data.

        Yields:
            str: The prompt for the given content.
        """
        output_parser = PydanticOutputParser(pydantic_object=self.schema)

        for chunk in content:
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        'system',
                        'You are a parser for X-ray diffraction data. '
                        'You read the raw data from an XRD file and fill a structured Pydantic model. '
                        'You will also get the previous response as input. '
                        'If it is not None, you should use this information to improve the quality of the output. ',
                    ),
                    (
                        'system',
                        '{format_instructions}',
                    ),
                    (
                        'human',
                        'Fill the XRD fields with based on the following data: \n{input_data}\n '
                        'The previous response is: {previous_response}',
                    ),
                    (
                        'system',
                        'Very Important: In case you do not find a value, leave the field empty.',
                    ),
                ],
            ).partial(
                input_data=chunk,
                format_instructions=output_parser.get_format_instructions(),
            )
            yield prompt

    def generate_response(self, content: list[str]) -> Generator[str, None, None]:
        """
        Generate a response for the given prompt.

        Args:
            content (list[str]): The list of strings containing the data.

        Yields:
            str: The response for the given content.
        """
        resp = None
        for prompt in self.generate_prompt(content):
            pipeline = prompt | self.llm
            resp = pipeline.invoke({'previous_response': resp})

            yield resp


class ChatGroqLlamaStructured:
    """
    Model for llama3-8b-8192 provided by ChatGroq. It is used to generate structured
    output.
    """

    def __init__(self, schema: 'BaseModel'):
        llm = ChatGroq(model='llama-3.3-70b-versatile')
        self.llm = llm.with_structured_output(schema)
        self.schema = schema

    def generate_prompt(self, content: list[str]) -> Generator[str, None, None]:
        """
        Generate a prompt for the given content.

        Args:
            content (list[str]): The list of strings containing the data.

        Yields:
            str: The prompt for the given content.
        """
        for chunk in content:
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        'system',
                        'You are a parser for X-ray diffraction data. '
                        'You read the raw data from an XRD file and fill a structured JSON. ',
                    ),
                    (
                        'system',
                        'Very Important: In case you do not find a value, leave the field empty.'
                        'Only return the JSON in your response. Do not add helper text or additional information.'
                        'Do not use linebreak or \\n in your response.',
                    ),
                    (
                        'human',
                        'Fill the XRD fields with based on the following data: \n{input_data}\n ',
                    ),
                ],
            ).partial(input_data=chunk)
            yield prompt

    def generate_prompt_with_history(
        self, content: list[str]
    ) -> Generator[str, None, None]:
        """
        Generate a prompt for the given content including the previous response.

        Args:
            content (list[str]): The list of strings containing the data.

        Yields:
            str: The prompt for the given content.
        """
        for chunk in content:
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        'system',
                        'You are a parser for X-ray diffraction data. '
                        'You read the raw data from an XRD file and fill a structured JSON. '
                        'If the previous response is available, fill it with more appropriate data.',
                    ),
                    (
                        'system',
                        'Very Important: In case you do not find a value, leave the field empty.'
                        'Only return a valid JSON in your response. Do not add helper text or additional information.'
                        'Do not use linebreak or \\n in your response.',
                    ),
                    (
                        'human',
                        'Fill the XRD fields using the following data from XRD file: \n{input_data}\n '
                        'The previous response is: {previous_response}',
                    ),
                ],
            ).partial(input_data=chunk)
            yield prompt

    def generate_response(
        self, content: list[str], history: bool = False
    ) -> Generator[Union[str, dict], None, None]:
        """
        Generate a response for the given content.

        Args:
            content (list[str]): The list of strings containing the data.
            history (bool, optional): Whether to include the previous response in the
                prompt. Defaults to False.

        Yields:
            str: The response for the given content.
        """
        response = {}

        if history:
            prompt_generator = self.generate_prompt_with_history
        else:
            prompt_generator = self.generate_prompt

        for prompt in prompt_generator(content):
            try:
                pipeline = prompt | self.llm
                if history:
                    if isinstance(response, dict):
                        response = pipeline.invoke(
                            {'previous_response': json.dumps(response)}
                        )
                else:
                    response = pipeline.invoke({})

                yield response
            except Exception as e:
                yield e
