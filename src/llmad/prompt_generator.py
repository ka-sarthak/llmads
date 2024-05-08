from typing import List, Optional, Any
import yaml
from pathlib import Path

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from nomad.metainfo import Section

from llmad.utils import identify_mime_type
from llmad.nomad_instructions import (
    NOMAD_FORMAT_INSTRUCTIONS,
    NOMAD_FORMAT_INSTRUCTIONS2,
)


class PromptGeneratorInput(BaseModel):
    """
    This class contains the input parameters for the prompt generator.
    """

    nomad_schema: Any = Field(
        ...,
        description="""The specification to the NOMAD schema to be used to parsed the raw files text. This can be a NOMAD schema object or a path to a YAML file.""",
    )
    raw_files_paths: List[str] = Field(
        ...,
        description="""The list of paths to the raw files.""",
    )
    archive: str = Field(
        default='{{"data": }}',
        description="""The JSON snippet to be filled with the extracted information from the raw files.""",
    )
    content: Optional[List[str]] = Field(
        None,
        description="""The content of the input files, or chunks of data based on input files.""",
    )

    def msection_to_dict(self, section: Section = None) -> Optional[dict]:
        """
        Convert a NOMAD schema section to a dictionary to be used in the prompting

        Args:
            section (Section, optional): The NOMAD section to be passed to a dictionary. Defaults to None.

        Returns:
            (Optional[dict]): The dictionary representation of the NOMAD schema.
        """
        if section is None:
            return None
        dct = section.m_to_dict()
        msection_dict = {}
        for quantity in dct.get('quantities', []):
            name = quantity.get('name')
            msection_dict.setdefault(name, {})
            msection_dict[name]['type'] = quantity.get('type', {}).get('type_data')
            msection_dict[name]['description'] = quantity.get('description')

        for name, sub_section in section.all_sub_sections.items():
            if name in msection_dict or section == sub_section.sub_section:
                # prevent inf recursion
                continue
            d = self.msection_to_dict(sub_section.sub_section)
            msection_dict[name] = [d] if sub_section.repeats else d

        return msection_dict

    def yaml_file_to_dict(self, nomad_yaml_file: str = '') -> Optional[dict]:
        """
        Read a YAML file and return its content as a dictionary  to be used in the prompting

        Args:
            nomad_yaml_file (str, optional): The path to the NOMAD schema YAML file. Defaults to ''.

        Returns:
            (Optional[dict]): The dictionary representation of the NOMAD schema.
        """
        if not nomad_yaml_file:
            return None
        yaml_object = yaml.safe_load(Path(nomad_yaml_file).read_text())
        return yaml_object


class PromptGenerator:
    """
    This class contains methods for generating prompts based on the file type.
    """

    def __init__(self, data: PromptGeneratorInput):
        self.content_index = 0
        self.data = data

    def generate(self) -> Optional[ChatPromptTemplate]:
        # Get the schema from 2 formats: Python section or YAML file
        schema = {}
        if isinstance(self.data.nomad_schema, Section):
            schema = self.data.msection_to_dict(self.data.nomad_schema)
        elif isinstance(self.data.nomad_schema, str):
            schema = self.data.yaml_file_to_dict(self.data.nomad_schema)
        if not schema:
            raise ValueError('The NOMAD schema is not valid to the covered format.')

        # Prepares the prompt from LangChain templates. We want to differentiate:
        # 1. The `system` message that tells the LLM how to behave. It includes the `schema` to be filled in the JSON snippet.
        # 2. The `human` message that contains the message input from the human (i.e., the input text to be processed, `self.raw_files_paths`).
        # 3. The `examples` message that contains the examples to be filled to help the LLM to recognize proper parsing.
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    'You are an expert extraction algorithm. Only extract the relevant information from the text. '
                    'If you do not know the value of an attribute asked to extract, skip it and do not return the value.'
                    'You will be passed a schema template in JSON format that you must fill with the information extracted from the text. '
                    'The schema to fill in is: \n```json{schema}```\n .',
                ),
                (
                    'system',
                    '\n{instructions}\n',
                ),
                (
                    'human',
                    'The input text that has to be parsed into the schema is \n{input}\n '
                    'Only share the filled schema, no yapping.',
                ),
            ]
        ).partial(
            instructions=NOMAD_FORMAT_INSTRUCTIONS,
            schema=schema,
            input=self.data.content[self.content_index],
        )
        # we extract output in JSON format
        return prompt

    def update_prompt(self, new_archive):
        self.data.archive = new_archive
        self.content_index += 1

        return self.generate()

    def read_raw_files_with_chunking(self) -> List[str]:
        """
        Read the raw files and split them into chunks. The raw files converted to strings
        and combined into one string. The combined string is then split into chunks.

        Returns:
            List[str]: The list of strings containing the data chunks.
        """
        # split the content into chunks
        CHUNK_SIZE = 5000
        CHUNK_OVERLAP = 100

        self.read_raw_files()
        content_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

        content_chunks = content_splitter.create_documents(self.data.content)

        # transform the chunk document into a list of strings
        content_chunks_list = [chunk.page_content for chunk in content_chunks]

        return content_chunks_list

    def read_raw_files(self) -> None:
        """
        Read the raw files and convert them into strings. `self.data.content` is set as a list,
        where each element is a string containing the content of one raw file.
        """

        HANDLER = {
            'text/plain': TextLoader,
        }

        content = []
        for file in self.data.raw_files_paths:
            mime_type = identify_mime_type(file)
            if mime_type is None:
                continue
            loader = HANDLER.get(mime_type)
            if loader is None:
                continue
            document_list = loader(file).load()
            content.append(document_list[0].page_content)

        self.data.content = content
