"""
This module contains classes and methods for generating prompts based on the file type.
"""

from typing import List
from pydantic import BaseModel
from llmad.utils import identify_mime_type


class PromptGeneratorInput(BaseModel):
    """
    This class contains the input parameters for the prompt generator.
    """

    nomad_schema_paths: List[str]
    data_file_paths: List[str]


class PromptGenerator:
    """
    This class contains methods for generating prompts based on the file type.
    """

    @staticmethod
    def yield_prompt(prompt_input: PromptGeneratorInput):
        """
        This method yeilds one prompt for each quantity.
        """
        data_content = PromptGenerator.read_and_transform_data(
            prompt_input.data_file_paths
        )
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
    def prompts_from_nomad_schema(file_paths):
        """
        This method reads and transforms a NOMAD file.
        """
        nomad_prompts = []

        for file_path in file_paths:
            nomad_prompts.extend(
                PromptGenerator.read_and_transform_nomad_schema(file_path)
            )

        return nomad_prompts

    @staticmethod
    def read_and_transform_data(file_paths):
        """
        This method prepares `str` from raw data files. Based on the file type, the
        file is read, transformed, and appended to the `data_content`.
        """
        data_content = ''

        for file_path in file_paths:
            file_type = identify_file_type(file_path)
            if not file_type:
                continue
            if identify_file_type(file_path) == 'xml':
                data_content += '\n' + PromptGenerator.read_and_transform_xml(file_path)

        return data_content

    @staticmethod
    def read_and_transform_nomad_schema(file_path):
        """
        This method reads and transforms a NOMAD schema file. For each quantity in the
        schema, a prompt is generated, and appended to `prompt_list`.
        """
        # TODO

    @staticmethod
    def read_and_transform_xml(file_path):
        """
        This method reads and transforms an XML file.
        """
        # TODO directly pass as a string
