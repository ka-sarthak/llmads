# NOMAD_FORMAT_INSTRUCTIONS = """The output should be formatted as a JSON instance that conforms to the JSON schema below.

# As an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
# the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.

# Here is the output schema:
# ```json
# {{
# {schema}
# }}
# ```"""

# NOMAD_FORMAT_INSTRUCTIONS2 = """The output should be formatted as a JSON instance that conforms to the JSON schema below.

# As an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
# the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.

# The output schema has to contain an initial key labeled as "data" and include an extra key under it named "m_def". The content of this extra key is: `'../upload/raw/os.path.basename(nomad_schema_file)#/definitions/section_definitions/Simulation'`,
# where `os.path.basename(nomad_schema_file)` is the base name of the schema file passed as an input. For this base name, replace the last format `'.json'` to be `'.archive.yaml'`.

# Here is the output schema:
# ```json
# {{
# {schema}
# }}
# ```"""


NOMAD_FORMAT_INSTRUCTIONS = """The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.

The output schema has to contain an initial key labeled as "data" and include an extra key under it named "m_def". The content of this extra key is: `'../upload/raw/os.path.basename(nomad_schema_file)#/definitions/section_definitions/Simulation'`,
where `os.path.basename(nomad_schema_file)` is the base name of the schema file passed as an input. For this base name, replace the last format `'.json'` to be `'.archive.yaml'`."""


# 'Take into account that the schema always starts at the level of the `data` key. Thus, the JSON '
# 'snippet should maintain this structure. For example, if the data only populates `program` and its `name`, then the '
# 'output JSON should be: ```json\n{{"data": {{"program": {{"name": "VASP"}}}}}}\n```. If now the data is recognized to populate '
# 'the `version` as well, then the output JSON snipped must be: ```json\n{{"data": {{"program": {{"name": "VASP", "version": "5.4"}}}}}}\n```.\n '
# 'Bear in mind that the schema is a Python object whose attributes names (keys in the JSON structure) cannot be changed. For example, the schema ```json\n{{"data": {{"program": {{"name": "VASP"}}}}}}\n``` '
# 'is correct as the attributes are those for a schema defined as ```json\n{{"data": {{"program": {{"name": {{"type":}}}}}}}}\n```. The example '
# '```json\n{{"data2": {{"program": {{"name": "VASP"}}}}}}\n``` is not valid because `data2` is not a valid attribute in the schema. '
# {{archive}},
# 'Based on this text, answer the following: '


# 'You need a memory that in the previous step you filled the schema with the information in a previous memorized chunk in '
# 'the previous step: {archive} (if available)',
