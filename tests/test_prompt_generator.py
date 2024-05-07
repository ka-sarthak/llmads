from llmad.prompt_generator import PromptGeneratorInput, PromptGenerator


def test_prompt_generator():
    prompt_input = PromptGeneratorInput(
        nomad_schema_path='tests/data/test_schema.archive.yaml',
        raw_data_file_paths=['tests/data/Si2_crystal_VASP/OUTCAR'],
    )
    prompt_dict = PromptGenerator.generate(prompt_input)
    assert isinstance(prompt_dict['context_and_raw_data'], str)
    assert isinstance(prompt_dict['prompt_questions'], list)
