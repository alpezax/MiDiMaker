from pydantic import BaseModel, Field
from typing import List

class ChordRequest(BaseModel):
    key: str = Field(default="C")
    scale: str = Field(default="major")
    progression: List[str] = Field(..., min_length=1)
    chord_types: List[str] = Field(default_factory=lambda: ["triad"])
    tempo: int = Field(default=120, ge=20, le=400)
    duration: float = Field(default=1.0, gt=0)
    octave: int = Field(default=4, ge=0, le=9)

