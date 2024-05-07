from typing import List, Union, Optional, Any

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
from nomad.metainfo import Section

from llmad.utils import identify_mime_type, extract_json
from llmad.llm_model import llm
from llmad.schemas import msection_to_json, yaml_file_to_json


class PromptGenerator(BaseModel):
    """
    This class contains methods for generating prompts based on the file type.
    """

    nomad_schema: Any = Field(
        ...,
        description="""The specification to the NOMAD schema to be used to parsed the raw files text.""",
    )
    raw_files_paths: List[str]

    @staticmethod
    def nomad_schema_dict(schema: Union[Section, str]) -> Optional[dict]:
        """
        This method reads and transforms a NOMAD schema file. For each quantity in the
        schema, a prompt is generated, and appended to `prompt_list`.
        """
        if isinstance(schema, Section):
            return msection_to_json(schema)
        elif isinstance(schema, str):
            return yaml_file_to_json(schema)

    @staticmethod
    def read_raw_files(filepath: List[str]) -> List[str]:
        """
        This method reads the contents of the raw files and returns them as a list of strings.

        Args:
            filepath (List[str]): The list of paths to the raw files.

        Returns:
            (List[str]): The list of strings content in the raw files.
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

    def template(self, schema: dict) -> ChatPromptTemplate:
        """
        This method generates one prompt for each quantity.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    'You are an expert extraction algorithm. Only extract the relevant information from the text. '
                    'If you do not know the value of an attribute asked to extract, just skip it and do not store it. '
                    'Take into account that the schema always starts at the level of the `data` key. Thus, the JSON '
                    'snippet should maintain this structure. For example, if the data only populates `program` and its `name`, then the '
                    'output JSON should be: ```json\n{{"data": {{"program": {{"name": "VASP"}}}}}}\n```. If now the data is recognized to populate '
                    'the `version as well, then the output JSON should be: ```json\n{{"data": {{"program": {{"name": "VASP", "version": "5.4"}}}}}}\n```.'
                    'Output your answer as JSON that matches the given schema: ```json\n{schema}\n```'
                    'Make sure to wrap the answer in ```json and ``` tags.',
                    # 'Based on this text, answer the following: '
                ),
                (
                    'human',
                    'The input to use for filling the schema is \n{input}\n '
                    'You need a memory that in the previous step you filled the schema with the information in a previous memorized chunk in '
                    'the previous step: {archive} (if available)',
                ),
            ]
        ).partial(schema=schema)
        prompt_template = prompt | llm | extract_json
        return prompt_template

    def generate(self) -> ChatPromptTemplate:
        """
        This method generates one prompt for each quantity.
        """
        # raw_input = PromptGenerator.read_raw_files(self.raw_files_paths)
        schema = PromptGenerator.nomad_schema_dict(self.nomad_schema)
        prompt_template = self.template(schema=schema)
        return prompt_template

    def update_prompt(self):
        pass
