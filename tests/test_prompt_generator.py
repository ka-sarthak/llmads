from llmad.prompt_generator import PromptGeneratorInput, PromptGenerator


def test_prompt_generator():
    prompt_input = PromptGeneratorInput(
        nomad_schema_paths=['tests/data/test_schema.archive.yaml'],
        raw_data_file_paths=['tests/data/Si2_crystal_VASP/OUTCAR'],
    )
    for prompt in PromptGenerator.yield_prompt(prompt_input):
        assert isinstance(prompt, str)


# if __name__ == '__main__':
#     test_prompt_generator()
