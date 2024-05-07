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

    nomad_schema_paths: List[str]
    raw_data_file_paths: List[str]


class PromptGenerator:
    """
    This class contains methods for generating prompts based on the file type.
    """

    @staticmethod
    def yield_prompt(prompt_input: PromptGeneratorInput):
        """
        This method generates one prompt for each quantity.
        """
        data_content = PromptGenerator.read_raw_data_files(
            prompt_input.raw_data_file_paths
        )
        data_content = ' '.join(data_content)
        nomad_prompts = PromptGenerator.prompts_from_nomad_schema(
            prompt_input.nomad_schema_paths
        )
        for nomad_prompt in nomad_prompts:
            prompt = (
                'You are a scrupulous file reader. Based on the following text, '
                f'return the appropriate value of {nomad_prompt}. '
                'If value is not found, say "Not Found".\n\n'
            )
            prompt += data_content
            yield prompt

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
    def prompts_from_nomad_schema(file_paths):
        """
        Create a list of prompts from multiple NOMAD schemas.
        """
        nomad_prompts = []

        for file_path in file_paths:
            nomad_prompts.extend(PromptGenerator.parse_nomad_schema(file_path))

        return nomad_prompts

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
