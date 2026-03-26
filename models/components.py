from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class MaterialType(Enum):
    ALUMINUM = "aluminum"
    CARBON_FIBER = "carbon_fiber"
    TITANIUM = "titanium"
    STEEL = "steel"


class LoadCase(Enum):
    STATIC = "static"
    FATIGUE = "fatigue"
    IMPACT = "impact"
    THERMAL = "thermal"


@dataclass
class Dimension:
    """Represents physical dimensions of a component."""
    length: float  # meters
    width: float   # meters
    height: float  # meters
    tolerance: float = 0.001  # meters
    
    def volume(self) -> float:
        return self.length * self.width * self.height
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "length": self.length,
            "width": self.width,
            "height": self.height,
            "tolerance": self.tolerance
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'Dimension':
        return cls(**data)


@dataclass
class LoadData:
    """Represents load case data for dynamics analysis."""
    case_type: LoadCase
    force_vector: List[float]  # [Fx, Fy, Fz] in Newtons
    moment_vector: List[float]  # [Mx, My, Mz] in N·m
    temperature: float  # Kelvin
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def magnitude(self) -> float:
        return sum(f**2 for f in self.force_vector) ** 0.5
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_type": self.case_type.value,
            "force_vector": self.force_vector,
            "moment_vector": self.moment_vector,
            "temperature": self.temperature,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LoadData':
        return cls(
            case_type=LoadCase(data["case_type"]),
            force_vector=data["force_vector"],
            moment_vector=data["moment_vector"],
            temperature=data["temperature"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )


@dataclass
class AircraftComponent:
    """Main data model for an aircraft component."""
    component_id: str
    name: str
    material: MaterialType
    dimensions: Dimension
    mass: float  # kg
    load_cases: List[LoadData] = field(default_factory=list)
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.component_id:
            self.component_id = str(uuid.uuid4())
    
    def add_load_case(self, load: LoadData) -> None:
        """Add a load case to the component."""
        self.load_cases.append(load)
    
    def get_total_force_magnitude(self) -> float:
        """Calculate total force magnitude across all load cases."""
        return sum(load.magnitude() for load in self.load_cases)
    
    def increment_version(self) -> str:
        """Increment semantic version and return new version string."""
        parts = self.version.split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        self.version = '.'.join(parts)
        return self.version
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize component to dictionary."""
        return {
            "component_id": self.component_id,
            "name": self.name,
            "material": self.material.value,
            "dimensions": self.dimensions.to_dict(),
            "mass": self.mass,
            "load_cases": [lc.to_dict() for lc in self.load_cases],
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AircraftComponent':
        """Deserialize component from dictionary."""
        return cls(
            component_id=data["component_id"],
            name=data["name"],
            material=MaterialType(data["material"]),
            dimensions=Dimension.from_dict(data["dimensions"]),
            mass=data["mass"],
            load_cases=[LoadData.from_dict(lc) for lc in data.get("load_cases", [])],
            version=data.get("version", "1.0.0"),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat())),
            metadata=data.get("metadata", {})
        )
