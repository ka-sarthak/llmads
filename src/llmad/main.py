from llmad.utils import get_input_data
from llmad.config import CHUNKING, MODEL, SCHEMA


input_data = get_input_data(CHUNKING)

model = MODEL(schema=SCHEMA)

chunk = 1
for response in model.generate_response(input_data, history=True):
    print(
        f'Chunk {chunk} processed. LLM response of type {type(response)}:\n{response}'
    )
    chunk += 1
