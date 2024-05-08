import os

from nomad_simulations import Program

from llmad.prompt_generator import PromptGenerator
from langchain.output_parsers.json import SimpleJsonOutputParser
from llmad.llm_model import llm


current_dir = os.path.dirname(os.path.abspath(__file__))
test_file = '../../tests/data/example.out'
test_file_path = os.path.join(current_dir, test_file)

prompt_generator = PromptGenerator(
    nomad_schema=Program.m_def,
    raw_files_paths=[test_file_path],
)
prompt = prompt_generator.generate()
json_parser = SimpleJsonOutputParser()
template = prompt | llm | json_parser
for i in range(10):
    try:
        llm_msg = template.invoke({'input': prompt_generator.raw_files_paths[0]})
        print(i, llm_msg)
    except Exception:
        print(i, 'exception catched!')
