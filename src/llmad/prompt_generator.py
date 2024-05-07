"""
This module contains classes and methods for generating prompts based on the file type.
"""

from typing import List
from pydantic import BaseModel
from langchain_community.document_loaders import TextLoader
from llmad.utils import identify_mime_type


class PromptGeneratorInput(BaseModel):
    """
    This class contains the input parameters for the prompt generator.
    """

    nomad_schema_path: str
    raw_data_file_paths: List[str]


class PromptGenerator:
    """
    This class contains methods for generating prompts based on the file type.
    """

    @staticmethod
    def generate(prompt_input: PromptGeneratorInput):
        """
        This method generates one prompt for each quantity.
        """
        data_content = PromptGenerator.read_raw_data_files(
            prompt_input.raw_data_file_paths
        )
        data_content = ''.join(data_content)

        context_and_raw_data = (
            'You are a scrupulous file reader. Read the following text containing raw '
            f'data: \n\n{data_content}.\n\n Based on this text, answer the following.'
        )

        prompt_questions = []
        nomad_quantities = PromptGenerator.parse_nomad_schema(
            prompt_input.nomad_schema_path
        )
        for nomad_quantity in nomad_quantities:
            prompt = (
                f'What is the value of {nomad_quantity}. '
                'Only return the value of the quantity. '
                'If value is not found, say "None".\n\n'
            )
            prompt_questions.append(prompt)

        return {
            'context_and_raw_data': context_and_raw_data,
            'prompt_questions': prompt_questions,
        }

    @staticmethod
    def read_raw_data_files(file_paths):
        """
        This method prepares `str` from raw data files. Based on the file type, the
        file is read and the content is appended to the `data_content`.
        """

        HANDLER = {
            'text/plain': TextLoader,
        }

        data_content = []
        for file_path in file_paths:
            mime_type = identify_mime_type(file_path)
            if mime_type is None:
                continue
            loader = HANDLER.get(mime_type)
            if loader is None:
                continue
            document_list = loader(file_path).load()
            data_content.append(document_list[0].page_content)

        return data_content

    @staticmethod
    def parse_nomad_schema(file_path):
        """
        This method reads and transforms a NOMAD schema file. For each quantity in the
        schema, a prompt is generated, and appended to `prompt_list`.
        """
        prompt_list = []

        # TODO based on the schema, generate strings of the quantity names
        prompt_list.append('Program Name')

        return prompt_list
