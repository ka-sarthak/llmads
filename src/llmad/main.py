from llmad.utils import get_input_data
from llmad.config import CHUNKING, MODEL, SCHEMA


input_data = get_input_data(CHUNKING)

model = MODEL(schema=SCHEMA)

for response in model.generate_response(input_data, history=True):
    print(response)
