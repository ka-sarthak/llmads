from llmad.utils import get_input_data
from llmad.config import Config
from llmad.data_model import XRDSettings, XRDResult, XRayDiffraction
from llmad.llm_model import ChatGroqLlamaStructured, HULlama


def main():
    config = Config('llmad.yaml')

    if config.schema == "XRDSettings":
        schema = XRDSettings
    elif config.schema == "XRDResult":
        schema = XRDResult
    elif config.schema == "XRayDiffraction":
        schema = XRayDiffraction
    else:
        raise ValueError(f'Invalid schema "{config.schema}".')

    if config.llm_model == 'HULlama':
        model = HULlama(schema)
    elif config.llm_model == 'ChatGroqLlamaStructured':
        model = ChatGroqLlamaStructured(schema)
    else:
        raise ValueError(f'Invalid model "{config.llm_model}".')

    chunk = 1
    input_data = get_input_data(config.chunking)
    for response in model.generate_response(input_data):
        print(
            f'Chunk {chunk} processed. LLM response of type {type(response)}:\n{response}\n'
        )
        chunk += 1


if __name__ == '__main__':
    main()
