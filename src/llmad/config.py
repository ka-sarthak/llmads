import os
from llmad.llm_model import ChatGroqLlamaStructured, HULlama
from llmad.data_model import XRDSettings, XRDResult, XRayDiffraction

# data files
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILES_PATH = '../../tests/data/xrd/rasx'

# LLM preprocessing
CHUNKING = True
CHUNK_SIZE = 8000
CHUNK_OVERLAP = 10


# schema
SCHEMA = XRDResult

# model
MODEL = ChatGroqLlamaStructured
