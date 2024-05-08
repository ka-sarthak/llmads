NOMAD_FORMAT_INSTRUCTIONS = """Here you have some instructions to help you prepare the output:

The first key of the JSON snippet must be labeled as "data", and the schema must be appearing as a nested dictionary under "data". Examples:
    1. ```json{"data": {}}``` is a valid output. No information is recognized in the input text.
    2. ```json{"data": {"program": {"name": "VASP"}}}``` is a valid output. Only the program name is recognized in the input text.
    3. ```json{"data": {"program": {"name": "VASP", "version": "5.4"}}}``` is an valid output. Both the program name and version are recognized in the input text.
    4. ```json{"name": "VASP"}``` is an invalid output. The first key must be labeled as "data".
    5. ```json{"data": {"program": {"name": "VASP"}, "version": "5.4"}}}``` is an invalid output. The schema must be appearing as a nested dictionary under "data".

The attributes of the schema are immutable, because they are Python class attributes. Examples:
    1. ```json{"data2": {}}``` is an invalid output. "data2" is not a valid attribute in the schema, but "data" is.
    3. ```json{"data": {"program": {"name": "VASP", "version": "5.4"}}}``` is an valid output if all attributes ("program", "name", "version") are defined like this in the schema.
    3. ```json{"data": {"program_vasp": {"name": "VASP"}}}``` is an invalid output if "program_vasp" is not defined in the schema.

You only use the schema as a cheatsheet. Do not use other resources to name attributes if these do not exist in the schema passed. Examples:
    1. ```json{"data": {"program": {"name": "VASP"}}}``` is a valid output if "program_vasp" is defined in the schema.
    2. ```json{"ENTRY": {"Program_name": "VASP"}}``` is an invalid output if "ENTRY" or "Program_name" are not defined the schema.

Ask for help (with text) if you think you found a key but you are unsure where to put it in the schema."""

NOMAD_FORMAT_INSTRUCTIONS2 = """Here you have some instructions to help you prepare the output:

1. Once you have the information extracted, give back your answer wrap as a JSON snippet in between ```json and ``` tags.'.
2. The first key of the JSON snippet must be labeled as "data", and the schema must be appearing as a nested dictionary under "data".
3. The attributes of the schema are immutable, because they are Python class attributes.
4. You only use the schema as a cheatsheet. Do not use other resources to name attributes if these do not exist in the schema passed.
5. Ask for help (with text) if you think you found a key but you are unsure where to put it in the schema."""
