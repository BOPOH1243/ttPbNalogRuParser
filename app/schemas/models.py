from pydantic import BaseModel
from typing import Any


class SearchRequest(BaseModel):
    search_string: str


class SearchStatus(BaseModel):
    request: dict
    response: dict


class Entity(BaseModel):
    person: dict[str, Any]
    organization: dict[str, Any]