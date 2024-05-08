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
where `os.path.basename(nomad_schema_file)` is the base name of the schema file passed as an input. For this base name, replace the last format `'.json'` to be `'.archive.yaml'`.

Here is the output schema:
```json
{{
{schema}
}}
```"""
