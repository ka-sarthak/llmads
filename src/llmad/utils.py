import warnings
import magic


def msection_to_json(section):
    dct = section.m_to_dict()
    json = {}
    for quantity in dct.get('quantities', []):
        name = quantity.get('name')
        json.setdefault(name, {})
        json[name]['type'] = quantity.get('type', {}).get('type_data')
        json[name]['description'] = quantity.get('description')

    for name, sub_section in section.all_sub_sections.items():
        if name in json or section == sub_section.sub_section:
            # prevent inf recursion
            continue
        d = msection_to_json(sub_section.sub_section)
        json[name] = [d] if sub_section.repeats else d

    return json


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
