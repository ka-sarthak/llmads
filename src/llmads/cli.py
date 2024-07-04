import click
from llmads.utils import get_input_data
from llmads.config import Config
from llmads.data_model import XRDSettings, XRDResult, XRayDiffraction
from llmads.llm_model import ChatGroqLlamaStructured, HULlama


@click.command()
@click.option(
    '--config',
    'config_path',
    default='llmad.yaml',
    help='Path of the YAML config file.',
)
@click.argument('subcommand', type=click.Choice(['run']))
def run_cli(subcommand, config_path):
    try:
        if subcommand == 'run':
            click.echo(run(config_path))
    except Exception as e:
        click.echo(f'ERROR: {e}')


def run(config_path):
    config = Config(config_path)
    print(config.__dict__)

    if config.schema == 'XRDSettings':
        schema = XRDSettings
    elif config.schema == 'XRDResult':
        schema = XRDResult
    elif config.schema == 'XRayDiffraction':
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
    input_data = get_input_data(
        config.test_file_path,
        config.chunking,
        config.chunk_size,
        config.chunk_overlap,
    )
    for response in model.generate_response(input_data):
        print(
            f'Chunk {chunk} processed. LLM response of type {type(response)}:\n{response}\n'
        )
        chunk += 1
