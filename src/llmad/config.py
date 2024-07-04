import os
import yaml
import dotenv


class Config:
    def __init__(self, config_file_path: str = None):
        self.set_defaults()

        if config_file_path:
            self.load_config(config_file_path)

        self.load_api_keys()

    def set_defaults(self):
        self.test_file_path = './tests/data/xrd/xrdml'
        self.chunking = True
        self.chunk_size = 4000
        self.chunk_overlap = 10
        self.schema = 'XRDSettings'
        self.llm_model = 'ChatGroqLlamaStructured'
        self.history = True

    def load_config(self, config_file_path: str):
        with open(config_file_path, 'r') as file:
            config = yaml.safe_load(file)

            if config.get('file', None):
                self.test_file_path = config['file'].get(
                    'test_file', self.test_file_path
                )

            if config.get('chunking', None):
                self.chunking = config['chunking'].get(
                    'perform_chunking', self.chunking
                )
                self.chunk_size = config['chunking'].get('chunk_size', self.chunk_size)
                self.chunk_overlap = config['chunking'].get(
                    'chunk_overlap', self.chunk_overlap
                )

            if config.get('model', None):
                self.schema = config['model'].get('schema', self.schema)
                self.llm_model = config['model'].get('llm', self.llm_model)
                self.history = config['model'].get('history', self.history)

    def load_api_keys(self):
        dotenv.load_dotenv()


config = Config()
