from pydantic import BaseModel

from .main import generate


# class Site(BaseModel):
#     atom: str
#     coordinates: list[float]


# class System(BaseModel):
#     system_id: int
#     sites: list[Site]
#     lattice: list[list[float]]
#     energy: float


# schema_dict = {'type': 'array', 'items': System.model_json_schema()}

print(generate(prompt='Why the sky is blue?'))
