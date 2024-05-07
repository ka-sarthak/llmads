from nomad_simulations import Program

from llmad.prompt_generator import PromptGenerator


prompt_generator = PromptGenerator(
    nomad_schema=Program.m_def,
    raw_files_paths=['/home/josepizarro/LLM-Hackathon-2024/tests/data/example.out'],
)
template = prompt_generator.generate()
llm_msg = template.invoke({'input': prompt_generator.raw_files_paths[0], 'archive': {}})
