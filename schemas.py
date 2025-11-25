from pydantic import BaseModel
from typing import List, Optional


class OperatorCreate(BaseModel):
    name: str
    active: int
    max_load: int
    weights: str


class Operator(OperatorCreate):
    id: int
    active: int
    max_load: int
    weights: str

class SourceSchema(BaseModel):
    id: int
    name: str

class Lead(BaseModel):
    id: int
    external_id: str
    name: str

class ContactSchema(BaseModel):
    id: int
    lead_id: int
    source_id: int
    operator_id: Optional[int]
