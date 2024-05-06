from pydantic import BaseModel
from langchain_community.llms.ollama import Ollama


class Site(BaseModel):
    atom: str
    coordinates: list[float]


class System(BaseModel):
    system_id: int
    sites: list[Site]
    lattice: list[list[float]]
    energy: float


schema_dict = {'type': 'array', 'items': System.model_json_schema()}
