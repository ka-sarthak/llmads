import os
import warnings
import magic

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


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


def read_raw_files_with_chunking(
    raw_files_paths, chunk_size: int = 1000, chunk_overlap: int = 100
):
    """
    Read the raw files and split them into chunks. The raw files converted to strings
    and combined into one string. The combined string is then split into chunks.

    Args:
        raw_files_paths (List[str]): The list of paths to the raw files.
        chunk_size (int): The size of the chunks.
        chunk_overlap (int): The overlap between the chunks.

    Returns:
        List[str]: The list of strings containing the data chunks.
    """

    content = read_raw_files(raw_files_paths=raw_files_paths)
    content_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    content_chunks = content_splitter.create_documents(content)

    content_chunks_list = [chunk.page_content for chunk in content_chunks]

    return content_chunks_list


def get_input_data(
    test_file_path,
    chunking: bool = False,
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
):
    """
    Get the input data from the test file.

    Args:
        test_file_path (str): The path to the test file.
        chunking (bool): Whether to split the content into chunks.

    Returns:
        List[str]: The list of strings containing the data.
    """
    abs_file_paths = []
    for file in os.listdir(os.path.join(test_file_path)):
        abs_file_paths.append(os.path.join(test_file_path, file))
    if chunking:
        return read_raw_files_with_chunking(abs_file_paths, chunk_size, chunk_overlap)
    return read_raw_files(abs_file_paths)
