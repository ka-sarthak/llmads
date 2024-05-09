from typing import TYPE_CHECKING
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

    def generate_prompt(
        self,
        content: list[str],
    ):
        """
        Generate a prompt for the given content.
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

    def generate_response(self, content):
        """
        Generate a response for the given prompt.
        """
        resp = None
        for prompt in self.generate_prompt(content):
            pipeline = prompt | self.llm
            resp = pipeline.invoke({'previous_response': resp})

            yield resp


class ChatGroqLlamaStructured:
    def __init__(self, schema: 'BaseModel'):
        llm = ChatGroq(model='llama3-8b-8192', temperature=0.7)
        self.llm = llm.with_structured_output(schema)
        self.schema = schema

    def generate_prompt(self, content: list):
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

    def generate_prompt_with_history(self, content: list):
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

    def generate_response(self, content, history=False):
        resp = 'None'

        if history:
            prompt_generator = self.generate_prompt_with_history
        else:
            prompt_generator = self.generate_prompt

        for prompt in prompt_generator(content):
            try:
                pipeline = prompt | self.llm
                if history:
                    resp = pipeline.invoke({'previous_response': resp})
                else:
                    resp = pipeline.invoke({})

                yield resp
            except Exception as e:
                yield e
