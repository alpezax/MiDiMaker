import yaml
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/v1/patterns")

# Modelo para listar patrones
class Pattern(BaseModel):
    name: str
    genre: str
    bpm: int
    steps: int
    instruments: dict

# Cargar la base de datos de patrones
def load_patterns():
    with open("app/resources/tr808.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data.get("patterns", [])

patterns_db = load_patterns()

# Endpoint para listar todos los patrones
@router.get("/", response_model=List[Pattern])
def list_patterns():
    return patterns_db

# Endpoint para obtener un patrón por nombre
@router.get("/{pattern_name}", response_model=Pattern)
def get_pattern(pattern_name: str):
    for pattern in patterns_db:
        if pattern["name"].lower() == pattern_name.lower():
            return pattern
    raise HTTPException(status_code=404, detail="Pattern not found")
