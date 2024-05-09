import os
from typing import TYPE_CHECKING

from langchain_community.llms.ollama import Ollama
from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from llmad.utils import identify_mime_type
from llmad.data_model import XRDSettings, XRDResult, XRayDiffraction

if TYPE_CHECKING:
    from pydantic import BaseModel

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILES = [
    '../../tests/data/xrd/m82762_rc1mm_1_16dg_src_slit_phi-101_3dg_-420_mesh_long.xrdml'
]


def read_raw_files(raw_files_paths) -> None:
    """
    Read the raw files and convert them into strings. `self.data.content` is set as a list,
    where each element is a string containing the content of one raw file.
    """

    HANDLER = {
        'text/plain': TextLoader,
        'text/xml': TextLoader,
    }

    content = []
    for file in raw_files_paths:
        mime_type = identify_mime_type(file)
        if mime_type is None:
            continue
        loader = HANDLER.get(mime_type)
        if loader is None:
            continue
        document_list = loader(file).load()
        content.append(document_list[0].page_content[:10000])

    return content


def read_raw_files_with_chunking(raw_files_paths):
    """
    Read the raw files and split them into chunks. The raw files converted to strings
    and combined into one string. The combined string is then split into chunks.

    Returns:
        List[str]: The list of strings containing the data chunks.
    """
    # split the content into chunks

    content = read_raw_files(raw_files_paths=raw_files_paths)
    content_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    content_chunks = content_splitter.create_documents(content)

    # transform the chunk document into a list of strings
    content_chunks_list = [chunk.page_content for chunk in content_chunks]

    return content_chunks_list


def get_input_data(chunking: bool = False):
    """
    Get the input data from the test file.
    """
    test_file_path = []
    for file in TEST_FILES:
        test_file_path.append(os.path.join(CURRENT_DIR, file))
    if chunking:
        return read_raw_files_with_chunking(test_file_path)
    return read_raw_files(test_file_path)


class HULlama:
    """
    Model for llama3 hosted at HU.
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
        llm = ChatGroq(model='llama3-8b-8192')
        self.llm = llm.with_structured_output(schema)
        self.schema = schema

    def generate_prompt(self, content: list):
        for chunk in content:
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        'system',
                        'You are a parser for X-ray diffraction data. '
                        'You read the raw data from an XRD file and fill a structured Pydantic model. ',
                        'You will also get the previous response as input. '
                        'If it is not None, you should use this information to improve the quality of the output. ',
                    ),
                    (
                        'human',
                        'Fill the XRD fields with based on the following data: \n{input_data}\n ',
                        'The previous response is: {previous_response}',
                    ),
                    (
                        'system',
                        'Very Important: In case you do not find a value, leave the field empty.',
                    ),
                ],
            ).partial(input_data=chunk)
            yield prompt
            return

    def generate_response(self, content):
        resp = None
        for prompt in self.generate_prompt(content):
            pipeline = prompt | self.llm
            resp = pipeline.invoke({})

            yield resp


if __name__ == '__main__':
    input_data = get_input_data(chunking=True)

    schema = XRDSettings
    model = ChatGroqLlamaStructured(schema=schema)

    for response in model.generate_response(input_data, history=True):
        print(response)
