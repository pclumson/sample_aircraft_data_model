from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MaterialType(str, Enum):
    ALUMINUM = "aluminum"
    CARBON_FIBER = "carbon_fiber"
    TITANIUM = "titanium"
    STEEL = "steel"


class LoadCaseType(str, Enum):
    STATIC = "static"
    FATIGUE = "fatigue"
    IMPACT = "impact"
    THERMAL = "thermal"


class DimensionSchema(BaseModel):
    length: float = Field(..., gt=0, description="Length in meters")
    width: float = Field(..., gt=0, description="Width in meters")
    height: float = Field(..., gt=0, description="Height in meters")
    tolerance: float = Field(default=0.001, ge=0, description="Tolerance in meters")


class LoadDataSchema(BaseModel):
    case_type: LoadCaseType
    force_vector: List[float] = Field(..., min_length=3, max_length=3)
    moment_vector: List[float] = Field(..., min_length=3, max_length=3)
    temperature: float = Field(default=293.15)


class ComponentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    material: MaterialType
    dimensions: DimensionSchema
    mass: float = Field(..., gt=0)
    version: str = Field(default="1.0.0")
    metadata: Optional[Dict[str, Any]] = {}


class ComponentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    material: Optional[MaterialType] = None
    mass: Optional[float] = Field(None, gt=0)
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ComponentResponse(BaseModel):
    id: int
    component_id: str
    name: str
    material: str
    mass: float
    version: str
    created_at: datetime
    updated_at: Optional[datetime]
    dimensions: Optional[DimensionSchema]
    load_cases: List[LoadDataSchema] = []

    class Config:
        from_attributes = True


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None
