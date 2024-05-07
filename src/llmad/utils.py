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