import os
import time

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
template = prompt | llm
with open(os.path.join(current_dir, '../../test_llm.txt'), 'w') as file:
    for i in range(20):
        start_time = time.time()
        try:
            file_content = prompt_generator.read_raw_files(
                prompt_generator.raw_files_paths
            )
            llm_msg = template.invoke({'input': file_content[0]})
        except Exception:
            print(i, 'exception catched!')
        elapsed_time = time.time() - start_time
        print(i, llm_msg, elapsed_time)
        file.write(f'{str(elapsed_time)}, {llm_msg}')
