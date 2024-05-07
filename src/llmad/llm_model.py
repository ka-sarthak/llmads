from nomad_simulations import Simulation, Program


def msection_to_json(section):
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
        d = msection_to_json(sub_section.sub_section)
        msection_dict[name] = [d] if sub_section.repeats else d

    return msection_dict


nomad_schema = msection_to_json(Simulation.m_def)
