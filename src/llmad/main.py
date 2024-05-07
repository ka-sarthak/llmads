import json
import re
from typing import Optional, List

from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate

from llmad.llm_model import llm
from llmad.schemas import nomad_schema
from llmad.utils import extract_json

import yaml

yaml_object = yaml.safe_load(
    '/home/josepizarro/LLM-Hackathon-2024/tests/data/original_data_NOMADschema.archive.yaml'
)


f = open('/home/josepizarro/LLM-Hackathon-2024/tests/data/example.out', 'r')
# query = f.read()
# llm_data = prompt_query(query=query, schema=nomad_schema)
# print(llm_data)
