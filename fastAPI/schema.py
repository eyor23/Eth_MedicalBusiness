from pydantic import BaseModel, field_validator
from typing import List

class DetectionBase(BaseModel):
    bbox: List[float]
    confidence: float
    class_label: str

    @field_validator("bbox")
    def bbox_must_have_four_elements(cls, v):
        if len(v) != 4:
            raise ValueError("bbox must contain four elements: xmin, ymin, xmax, ymax")
        return v

class DetectionCreate(DetectionBase):
    pass

class DetectionUpdate(DetectionBase):
    pass

class Detection(DetectionBase):
    id: int

    class Config:
        orm_mode = True
