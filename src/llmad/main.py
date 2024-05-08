import os
import time

from nomad_simulations import Simulation, Program

from llmad.prompt_generator import PromptGenerator, PromptGeneratorInput
from langchain.output_parsers.json import SimpleJsonOutputParser
from llmad.llm_model import llm


current_dir = os.path.dirname(os.path.abspath(__file__))
test_file = '../../tests/data/example.out'
test_file = '../../tests/data/Si2_crystal_VASP/OUTCAR'
test_file_path = os.path.join(current_dir, test_file)

data = PromptGeneratorInput(
    nomad_schema=Program.m_def, raw_files_paths=[test_file_path], content=[]
)
prompt_generator = PromptGenerator(data=data)
prompt_generator.read_raw_files_with_chunking()
prompt = prompt_generator.generate()
json_parser = SimpleJsonOutputParser()

counter = 0
archive = None
for prompt in prompt_generator.generate():
    template = prompt | llm | json_parser
    print('chunk')
    archive = template.invoke({'previous_archive': archive})
    print(archive)

print(archive)
