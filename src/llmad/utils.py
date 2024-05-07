from typing import List
import re
import json
import warnings
import magic


def identify_mime_type(file_path: str) -> str:
    """
    This function identifies the mime type based on file header.
    """
    with open(file_path, 'r') as f:
        file_header = f.read(100)

    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(file_header)
    if mime_type is None:
        warnings.warn(f'No file extension found for "{file_path}".')

    return mime_type


def extract_json(message: str = '') -> List[dict]:
    """Extracts JSON content from a string where JSON is embedded between ```json and ``` tags.

    Parameters:
        message (str): The text containing the JSON content.

    Returns:
        (list): A list of extracted JSON strings.
    """
    # Define the regular expression pattern to match JSON blocks
    pattern = r'```\njson(.*?)```'

    # Find all non-overlapping matches of the pattern in the string
    matches = re.findall(pattern, message, re.DOTALL)

    # Return the list of matched JSON strings, stripping any leading or trailing whitespace
    try:
        return [json.loads(match.strip()) for match in matches]
    except Exception:
        raise ValueError(f'Failed to parse: {message}')
