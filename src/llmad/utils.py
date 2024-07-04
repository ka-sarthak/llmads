import os
import warnings
import magic

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from llmad.config import CHUNK_SIZE, CHUNK_OVERLAP, TEST_FILES_PATH, CURRENT_DIR


def identify_mime_type(file_path: str) -> str:
    """
    This function identifies the mime type based on file header.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The mime type of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        file_header = f.read(100)

    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(file_header)
    if mime_type is None:
        warnings.warn(f'No file extension found for "{file_path}".')

    return mime_type


def read_raw_files(raw_files_paths) -> list[str]:
    """
    Read the raw files and convert them into strings.

    Args:
        raw_files_paths (List[str]): The list of paths to the raw files.

    Returns:
        List[str]: The list of strings containing the data.
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
        document_str = document_list[0].page_content[:10000]

        # replace tabs and newlines with spaces
        document_str = document_str.translate(str.maketrans('\t\n', '  '))

        content.append(document_str)

    return content


def read_raw_files_with_chunking(raw_files_paths):
    """
    Read the raw files and split them into chunks. The raw files converted to strings
    and combined into one string. The combined string is then split into chunks.

    Args:
        raw_files_paths (List[str]): The list of paths to the raw files.

    Returns:
        List[str]: The list of strings containing the data chunks.
    """

    content = read_raw_files(raw_files_paths=raw_files_paths)
    content_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    content_chunks = content_splitter.create_documents(content)

    content_chunks_list = [chunk.page_content for chunk in content_chunks]

    return content_chunks_list


def get_input_data(chunking: bool = False):
    """
    Get the input data from the test file.

    Args:
        chunking (bool): Whether to split the content into chunks.

    Returns:
        List[str]: The list of strings containing the data.
    """
    abs_file_paths = []
    for file in os.listdir(os.path.join(CURRENT_DIR, TEST_FILES_PATH)):
        abs_file_paths.append(os.path.join(CURRENT_DIR, TEST_FILES_PATH, file))
    if chunking:
        return read_raw_files_with_chunking(abs_file_paths)
    return read_raw_files(abs_file_paths)
