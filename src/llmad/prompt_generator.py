from typing import List, Optional, Any
import yaml
from pathlib import Path
import warnings

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from nomad.metainfo import Section

from llmad.utils import identify_mime_type, extract_json
from llmad.llm_model import llm
from llmad.nomad_instructions import NOMAD_FORMAT_INSTRUCTIONS


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
            d = self.msection_to_json(sub_section.sub_section)
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


class PromptGenerator(PromptGeneratorInput):
    """
    This class contains methods for generating prompts based on the file type.
    """

    # def __init__(self, *args, **kwargs) -> None:
    #     self.archive = '{{"data":}}'

    @staticmethod
    def read_raw_files(filepath: List[str]) -> List[str]:
        """
        Read the raw files and return their content as a list of strings.

        Args:
            filepath (List[str]): The list of paths to the raw files.

        Returns:
            (List[str]): The list of strings containing the content of the raw files.
        """

        HANDLER = {
            'text/plain': TextLoader,
        }

        content = []
        for file in filepath:
            mime_type = identify_mime_type(file)
            if mime_type is None:
                continue
            loader = HANDLER.get(mime_type)
            if loader is None:
                continue
            document_list = loader(file).load()
            content.append(document_list[0].page_content)

        return content

    def generate(self) -> Optional[ChatPromptTemplate]:
        # Get the schema from 2 formats: Python section or YAML file
        schema = {}
        if isinstance(self.nomad_schema, Section):
            schema = self.msection_to_dict(self.nomad_schema)
        elif isinstance(self.nomad_schema, str):
            schema = self.yaml_file_to_dict(self.nomad_schema)
        if not schema:
            warnings.warn('The schema is empty. Please provide a valid schema.')
            return None

        # Prepares the prompt from LangChain templates. We want to differentiate:
        # 1. The `system` message that tells the LLM how to behave. It includes the `schema` to be filled in the JSON snippet.
        # 2. The `human` message that contains the message input from the human (i.e., the input text to be processed, `self.raw_files_paths`).
        # 3. The `examples` message that contains the examples to be filled to help the LLM to recognize proper parsing.
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    'You are an expert extraction algorithm. Only extract the relevant information from the text. '
                    'If you do not know the value of an attribute asked to extract, just skip it and do not store it. '
                    'You will be passed a schema template (called NOMAD schema from now on) that you must fill with the information extracted from the text. '
                    'Here you have some instructions to follow when writing your output: \n{instructions}\n'
                    'Once you have the information extracted, give back your answer wrap as a JSON snippet in between ```json and ``` tags.'
                    # 'Take into account that the schema always starts at the level of the `data` key. Thus, the JSON '
                    # 'snippet should maintain this structure. For example, if the data only populates `program` and its `name`, then the '
                    # 'output JSON should be: ```json\n{{"data": {{"program": {{"name": "VASP"}}}}}}\n```. If now the data is recognized to populate '
                    # 'the `version` as well, then the output JSON snipped must be: ```json\n{{"data": {{"program": {{"name": "VASP", "version": "5.4"}}}}}}\n```.\n '
                    'Output your answer as JSON that matches the given schema: ```json\n{schema}\n```'
                    # 'Bear in mind that the schema is a Python object whose attributes names (keys in the JSON structure) cannot be changed. For example, the schema ```json\n{{"data": {{"program": {{"name": "VASP"}}}}}}\n``` '
                    # 'is correct as the attributes are those for a schema defined as ```json\n{{"data": {{"program": {{"name": {{"type":}}}}}}}}\n```. The example '
                    # '```json\n{{"data2": {{"program": {{"name": "VASP"}}}}}}\n``` is not valid because `data2` is not a valid attribute in the schema. '
                    'Make sure to wrap the answer in ```json and ``` tags.',
                    # {{archive}},
                    # 'Based on this text, answer the following: '
                ),
                # MessagesPlaceholder('examples'),  # <-- EXAMPLES!
                (
                    'human',
                    'The input to use for filling the schema is \n{input}\n ',
                    # 'You need a memory that in the previous step you filled the schema with the information in a previous memorized chunk in '
                    # 'the previous step: {archive} (if available)',
                ),
            ]
        ).partial(instructions=NOMAD_FORMAT_INSTRUCTIONS, schema=schema)
        # we extract output in JSON format
        prompt_template = prompt | llm | extract_json
        return prompt_template

    def update_prompt(self):
        # self.archive = ...
        pass
