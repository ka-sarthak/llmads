from nomad_simulations import Program

from llmad.prompt_generator import PromptGenerator
from langchain.output_parsers.json import SimpleJsonOutputParser
from llmad.llm_model import llm

prompt_generator = PromptGenerator(
    nomad_schema=Program.m_def,
    raw_files_paths=['/home/josepizarro/LLM-Hackathon-2024/tests/data/example.out'],
)
prompt = prompt_generator.generate()
json_parser = SimpleJsonOutputParser()
template = prompt | llm | json_parser
llm_msg = template.invoke({'input': prompt_generator.raw_files_paths[0]})
print(llm_msg)
