import os

from nomad_simulations import Program

from llmad.prompt_generator import PromptGenerator
from llmad.utils import extract_json
from llmad.llm_model import llm


current_dir = os.path.dirname(os.path.abspath(__file__))
test_file = '../../tests/data/example.out'
test_file_path = os.path.join(current_dir, test_file)

prompt_generator = PromptGenerator(
    nomad_schema=Program.m_def,
    raw_files_paths=[test_file_path],
)
prompt = prompt_generator.generate()
template = prompt | llm | extract_json  # extract output in JSON format
llm_msg = template.invoke({'input': prompt_generator.raw_files_paths[0]})
