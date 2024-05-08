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
