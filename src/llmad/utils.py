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

    return jsonimport warnings


def identify_file_type(file_path: str) -> str:
    """
    This function identifies the file type based on the file extension.
    """
    file_extension = file_path.split('.')[-1]
    if not file_extension:
        warnings.warn(f'No file extension found for "{file_path}".')
        return ''
    if file_extension in [
        'xml',
        'json',
        'yaml',
    ]:
        return file_extension
    if file_extension in ['xrdml']:
        return 'xml'
